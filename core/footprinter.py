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
