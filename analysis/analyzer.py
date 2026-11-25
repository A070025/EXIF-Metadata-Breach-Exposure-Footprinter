from typing import Any
from core.footprinter import run_footprint_core


CONFIDENCE_MULTIPLIER = {
    "high": 1.0,
    "medium": 0.8,
    "low": 0.5,
}


def classify_severity(score: float) -> str:
    """Map normalized risk score (0.0 - 10.0) into standard severity tiers."""
    if score >= 9.0:
        return "CRITICAL"
    if score >= 7.0:
        return "HIGH"
    if score >= 4.0:
        return "MEDIUM"
    if score > 0.0:
        return "LOW"
    return "INFO"


def _format_raw_value(raw_value: Any) -> str:
    """Convert raw_value (dict, list, scalar, or None) into a clean readable string."""
    if raw_value is None:
        return "N/A"
    if isinstance(raw_value, dict):
        if not raw_value:
            return "Empty metadata"
        return ", ".join(f"{k}={v}" for k, v in raw_value.items())
    if isinstance(raw_value, list):
        return ", ".join(str(item) for item in raw_value) if raw_value else "None"
    return str(raw_value).strip() or "N/A"


def _infer_base_score(category: str, indicator: str, source: str) -> float:
    """Assign a baseline OSINT risk score (0.0 - 10.0) based on indicator sensitivity."""
    ind_lower = indicator.lower()
    src_lower = source.lower()

    if category == "exif_metadata":
        if "gps" in ind_lower or "coordinate" in ind_lower:
            return 7.5
        if "datetime" in ind_lower:
            return 4.5
        if any(tag in ind_lower for tag in ("make", "model", "software")):
            return 3.5
        return 4.0

    if category == "breach_exposure":
        if "dry_run" in src_lower:
            return 1.0
        if "local_digest" in src_lower:
            return 2.0
        return 8.0

    return 5.0


def _infer_remediation(category: str, indicator: str, source: str) -> str:
    """Generate actionable remediation guidance tailored to the OSINT indicator."""
    ind_lower = indicator.lower()
    src_lower = source.lower()

    if category == "exif_metadata":
        if "gps" in ind_lower or "coordinate" in ind_lower:
            return "Strip embedded GPS EXIF tags using exiftool before sharing images publicly."
        return "Sanitize device make, model, and timestamp metadata prior to publication."

    if category == "breach_exposure":
        if "dry_run" in src_lower or "local_digest" in src_lower:
            return "Run authorized lookup against an approved breach dataset to verify exposure."
        return "Rotate compromised credentials immediately and enforce Multi-Factor Authentication (MFA)."

    return "Review exposed artifact and restrict public access within authorized policy."


def analyze_findings(raw_records: Any) -> dict[str, Any]:
    """
    Ingest standardized records from core.footprinter.run_footprint_core():
    1. Safely handles None, non-list inputs, empty results, and missing dictionary keys.
    2. Deduplicates identical findings by category, target, indicator, and evidence.
    3. Computes weighted risk scores and detects compound EXIF + Breach exposure.
    """
    empty_summary = {
        "total_unique": 0,
        "duplicates_removed": 0,
        "overall_risk_score": 0.0,
        "overall_risk_level": "INFO",
        "compound_exposure": False,
        "severity_counts": {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0,
        },
    }

    if not isinstance(raw_records, list) or len(raw_records) == 0:
        return {"findings": [], "summary": empty_summary}

    seen_signatures: set[str] = set()
    processed_findings: list[dict[str, Any]] = []
    duplicates_removed = 0
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}

    for index, item in enumerate(raw_records, start=1):
        if not isinstance(item, dict):
            continue

        record_id = str(item.get("record_id") or f"OSINT-{index:03d}").strip()
        category = str(item.get("category") or "general_osint").lower().strip()
        source = str(item.get("source") or "unknown_source").strip()
        target = str(item.get("target") or "127.0.0.1").strip()
        indicator = str(item.get("indicator") or "Unclassified OSINT Indicator").strip()
        timestamp = str(item.get("timestamp") or "N/A").strip()
        evidence = _format_raw_value(item.get("raw_value"))

        # Deduplicate identical indicators
        signature = f"{category}|{target.lower()}|{indicator.lower()}|{evidence.lower()}"
        if signature in seen_signatures:
            duplicates_removed += 1
            continue
        seen_signatures.add(signature)

        confidence_raw = str(item.get("confidence") or "medium").lower().strip()
        multiplier = CONFIDENCE_MULTIPLIER.get(confidence_raw, 0.8)
        base_score = _infer_base_score(category, indicator, source)
        weighted_score = round(base_score * multiplier, 2)
        severity = classify_severity(weighted_score)
        severity_counts[severity] += 1

        processed_findings.append({
            "record_id": record_id,
            "category": category.upper(),
            "source": source,
            "target": target,
            "indicator": indicator,
            "evidence": evidence,
            "confidence": confidence_raw.upper(),
            "risk_score": weighted_score,
            "severity": severity,
            "remediation": _infer_remediation(category, indicator, source),
            "timestamp": timestamp,
        })

    if not processed_findings:
        empty_summary["duplicates_removed"] = duplicates_removed
        return {"findings": [], "summary": empty_summary}

    # Sort highest severity and score first
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    processed_findings.sort(
        key=lambda x: (severity_rank.get(x["severity"], 5), -x["risk_score"])
    )

    peak_score = max(f["risk_score"] for f in processed_findings)
    avg_score = sum(f["risk_score"] for f in processed_findings) / len(processed_findings)
    overall_score = round((peak_score * 0.7) + (avg_score * 0.3), 2)

    # Cross-category correlation: EXIF metadata + Breach exposure increases profiling risk
    categories_present = {f["category"] for f in processed_findings}
    compound_exposure = (
        "EXIF_METADATA" in categories_present and "BREACH_EXPOSURE" in categories_present
    )
    if compound_exposure:
        overall_score = min(10.0, round(overall_score + 0.8, 2))

    return {
        "findings": processed_findings,
        "summary": {
            "total_unique": len(processed_findings),
            "duplicates_removed": duplicates_removed,
            "overall_risk_score": overall_score,
            "overall_risk_level": classify_severity(overall_score),
            "compound_exposure": compound_exposure,
            "severity_counts": severity_counts,
        },
    }


def run_and_analyze(
    target: str,
    image_paths: list[str] | None = None,
    dry_run: bool = False,
    endpoint_url: str | None = None,
) -> dict[str, Any]:
    """Execute core footprinting module and directly return analyzed risk results."""
    raw_records = run_footprint_core(
        target=target,
        image_paths=image_paths,
        dry_run=dry_run,
        endpoint_url=endpoint_url,
    )
    return analyze_findings(raw_records)
