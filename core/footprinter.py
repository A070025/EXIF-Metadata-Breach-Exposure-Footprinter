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

