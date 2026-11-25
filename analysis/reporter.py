import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _truncate(text: str, max_len: int) -> str:
    """Truncate long strings cleanly to preserve terminal table alignment."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def display_terminal_report(
    report_data: dict[str, Any],
    target: str,
    dry_run: bool = False,
) -> None:
    """Render an aligned OSINT footprinting summary and findings table to stdout."""
    summary = report_data.get("summary", {})
    findings = report_data.get("findings", [])
    counts = summary.get("severity_counts", {})

    mode_label = "DRY-RUN SIMULATION" if dry_run else "ACTIVE FOOTPRINT AUDIT"
    border = "=" * 96

    print(f"\n{border}")
    print(f" EXIF & BREACH FOOTPRINTER REPORT | Target: {target} | Mode: {mode_label}")
    print(border)
    print(
        f" Overall Risk : {summary.get('overall_risk_level', 'INFO')} "
        f"({summary.get('overall_risk_score', 0.0)}/10.0)"
    )
    print(
        f" Findings     : {summary.get('total_unique', 0)} unique "
        f"({summary.get('duplicates_removed', 0)} duplicates filtered)"
    )
    print(
        f" Breakdown    : CRITICAL={counts.get('CRITICAL', 0)} | "
        f"HIGH={counts.get('HIGH', 0)} | MEDIUM={counts.get('MEDIUM', 0)} | "
        f"LOW={counts.get('LOW', 0)} | INFO={counts.get('INFO', 0)}"
    )

    if summary.get("compound_exposure"):
        print(
            " [!] ALERT    : Compound OSINT Exposure Detected "
            "(EXIF Metadata + Breach Indicator)"
        )

    print(border)

    if not findings:
        print(" [OK] No EXIF metadata leaks or breach exposures detected within scope.")
        print(f"{border}\n")
        return

    header = (
        f" {'ID':<11} | {'CATEGORY':<15} | {'SEVERITY':<8} | "
        f"{'SCORE':<5} | {'INDICATOR':<26} | {'EVIDENCE':<17}"
    )
    print(header)
    print("-" * 96)

    for item in findings:
        row = (
            f" {_truncate(item['record_id'], 11):<11} | "
            f"{_truncate(item['category'], 15):<15} | "
            f"{_truncate(item['severity'], 8):<8} | "
            f"{item['risk_score']:<5.1f} | "
            f"{_truncate(item['indicator'], 26):<26} | "
            f"{_truncate(item['evidence'], 17):<17}"
        )
        print(row)

    print(f"{border}\n")


def save_local_report(
    report_data: dict[str, Any],
    target: str,
    tool_name: str = "exif_breach_footprinter",
    output_dir: str = "output",
) -> dict[str, str]:
    """
    Save analyzed OSINT findings locally as JSON and TXT files.
    Enforces local-only storage with sanitized filenames and zero data exfiltration.
    """
    base_path = Path(output_dir).resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe_tool = re.sub(r"[^a-zA-Z0-9_-]", "_", tool_name.lower())
    safe_target = re.sub(r"[^a-zA-Z0-9._-]", "_", target)

    json_file = base_path / f"{safe_tool}_{safe_target}_{timestamp}.json"
    txt_file = base_path / f"{safe_tool}_{safe_target}_{timestamp}.txt"

    payload = {
        "metadata": {
            "tool": tool_name,
            "category": "Category 6 - Offensive OSINT",
            "target": target,
            "generated_utc": timestamp,
            "storage_policy": "LOCAL_ONLY_NO_EXFILTRATION",
        },
        "results": report_data,
    }

    with json_file.open("w", encoding="utf-8") as jf:
        json.dump(payload, jf, indent=2)

    summary = report_data.get("summary", {})
    findings = report_data.get("findings", [])

    lines = [
        f"Tool: {tool_name} (Category 6: Offensive OSINT)",
        f"Target: {target}",
        f"Generated (UTC): {timestamp}",
        f"Overall Risk: {summary.get('overall_risk_level', 'INFO')} ({summary.get('overall_risk_score', 0.0)}/10.0)",
        f"Compound Exposure (EXIF + Breach): {summary.get('compound_exposure', False)}",
        f"Total Unique Findings: {summary.get('total_unique', 0)}",
        "=" * 80,
    ]

    if not findings:
        lines.append("No EXIF metadata or breach exposure indicators detected.")
    else:
        for item in findings:
            lines.extend([
                f"[{item['severity']}] {item['record_id']} ({item['category']}) - {item['indicator']} | Score: {item['risk_score']}",
                f"  Target     : {item['target']}",
                f"  Source     : {item['source']}",
                f"  Confidence : {item['confidence']}",
                f"  Evidence   : {item['evidence']}",
                f"  Remediation: {item['remediation']}",
                f"  Timestamp  : {item['timestamp']}",
                "-" * 80,
            ])

    with txt_file.open("w", encoding="utf-8") as tf:
        tf.write("\n".join(lines) + "\n")

    return {"json_path": str(json_file), "txt_path": str(txt_file)}
