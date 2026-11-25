from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
from PIL import ExifTags, Image
import requests

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _build_record(
        record_id: str,
        category: str,
        source: str,
        target: str,
        indicator: str,
        raw_value: Any,
        confidence: str,
) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "category": category,
        "source": source,
        "target": target,
        "indicator": indicator,
        "raw_value": raw_value,
        "confidence": confidence,
        "timestamp": _utc_now_iso(),
    }

def _dms_to_decimal(dms_tuple: Any, ref: str | None) -> float | None:
    try:
        degrees = float(dms_tuple[0])
        minutes = float(dms_tuple[1])
        seconds = float(dms_tuple[2])
        decimal = round(degrees + (minutes / 60.0) + (seconds / 3600.0), 6)
        if ref in ("S", "W"):
            decimal = -decimal
        return decimal
    except (TypeError, ValueError, ZeroDivisionError, IndexError):
        return None

def extract_exif_findings(file_path: Path, target: str, start_index: int = 1) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not file_path.exists() or not file_path.is_file():
        return findings

    try: 
        with Image.open(file_path) as img:
            exif_data = img.getexif()
            if not exif_data:
                return findings

            tag_map = {ExifTags.TAGS.get(k, str(k)): v for k, v in exif_data.items()}
            gps_ifd = exif_data.get_ifd(ExifTags.IFD.GPSInfo) if hasattr(exif_data, "get_ifd") else {}

            counter = start_index
            for tag_name in ("Make", "Model", "Software", "DateTimeOriginal"):
                if tag_name in tag_map and tag_map[tag_name]:
                    findings.append(
                        _build_record(
                            record_id=f"EXIF-{counter:03d}",
                            category="exif_metadata",
                            source=str(file_path),
                            target=target,
                            indicator=f"Metadata tag present: {tag_name}",
                            raw_value=str(tag_map[tag_name]),
                            confidence="high",
                        )
                    )
                    counter += 1

            if gps_ifd:
                gps_named = {ExifTags.GPSTAGS.get(k, str(k)): v for k, v in gps_ifd.items()}
                lat = _dms_to_decimal(gps_named.get("GPS Latitude"), gps_named.get("GPS Latitude Ref"))
                lon = _dms_to_decimal(gps_named.get("GPS Longitude"), gps_named.get("GPS Longitude Ref"))
                if lat is not None and lon is not None:
                    findings.append(
                        _build_record(
                            record_id=f"EXIF-{counter:03d}",
                            category="exif_metadata",
                            source=str(file_path),
                            target=target,
                            indicator="Embedded GPS coordinates detected",
                            raw_value={"Latitude": lat, "Longitude": lon},
                            confidence="high",
                        )
                    )
    except OSError:
        return findings

    return findings

def check_exposure_indicators(
        target: str,
        dry_run: bool = False,
        endpoint_url: str | None = None,
        timeout: float = 5.0,
) -> list[dict[str, Any]]:
    normalized_target = target.strip().lower()
    if not normalized_target:
        return[]

    digest_prefix = hashlib.sha256(normalized_target.encode("utf-8")).hexdigest()[:12]

    if dry_run:
        return[
            _build_record(
                record_id="EXP-DRY-001",
                category="breach_exposure",
                source="dry_run_simulator",
                target=normalized_target,
                indicator="Simulated exposure lookup (no network request sent)",
                raw_value={"lookup_token": digest_prefix, "mode": "dry_run"},
                confidence="low",
            )
        ]

    if not endpoint_url:
        return[
            _build_record(
                record_id="EXP-001",
                category="breach_exposure",
                source="local_digest_check",
                target=normalized_target,
                indicator="Generated anonymized lookup digest for authorized scope check",
                raw_value={"sha256_prefix": digest_prefix},
                confidence="low",
            )
        ]

    try:
        response = requests.get(endpoint_url, params={"q": digest_prefix}, timeout=timeout)
        response.raise_for_status()
        payload = response.json() if response.content else {}
        matches = payload.get("matches", []) if isinstance(payload, dict) else []
        results: list[dict[str, Any]] = []
        for idx, match in enumerate(matches, start=1):
            results.append(
                _build_record(
                    record_id=f"EXP-{idx:03d}",
                    category="breach_exposure",
                    source=endpoint_url,
                    target=normalized_target,
                    indicator=str(match.get("summary", "Exposure indicator matched")),
                    raw_value=match,
                    confidence="medium",
                )
            )
        return results
    except (requests.RequestException, ValueError):
        return []

def run_footprint_core(
        target: str,
        image_paths: list[str] | None = None,
        dry_run: bool = False,
        endpoint_url: str | None = None,
) -> list[dict[str, Any]]:
    all_findings: list[dict[str, Any]] = []

    if image_paths:
        for raw_path in image_paths:
            path_obj = Path(raw_path)
            next_idx = len(all_findings) + 1
            all_findings.extend(extract_exif_findings(path_obj, target=target,start_index=next_idx))

    all_findings.extend(
        check_exposure_indicators(
            target=target,
            dry_run=dry_run,
            endpoint_url=endpoint_url,
        )
    )
    return all_findings