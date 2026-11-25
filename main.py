import argparse
import sys
from pathlib import Path

from analysis.analyzer import run_and_analyze
from analysis.reporter import display_terminal_report, save_local_report
from ethics.guardrails import EthicalGuardrails


def collect_image_files(directory: str) -> list[str]:
    """Collect supported image files inside the validated local directory."""
    supported_ext = {".jpg", ".jpeg", ".png", ".tiff", ".webp"}
    dir_path = Path(directory)
    return [
        str(p)
        for p in sorted(dir_path.iterdir())
        if p.is_file() and p.suffix.lower() in supported_ext
    ]


def parse_arguments() -> argparse.Namespace:
    epilog_text = """
Usage Examples:
  python main.py --dry-run
  python main.py -t 127.0.0.1 -d ./sample_targets
  python main.py -t example.com -d ./sample_targets -o ./output
    """
    parser = argparse.ArgumentParser(
        prog="exif-breach-footprinter",
        description=(
            "Offensive OSINT Tool (IKB31603): Extracts EXIF metadata from local images "
            "and evaluates anonymized breach exposure indicators."
        ),
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t", "--target",
        default="127.0.0.1",
        help="Authorized target identifier/host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "-d", "--directory",
        default="./sample_targets",
        help="Local directory containing sample images for EXIF audit (default: ./sample_targets)",
    )
    parser.add_argument(
        "-e", "--endpoint",
        default=None,
        help="Optional authorized local API endpoint for digest lookup (default: None)",
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Local output directory for JSON and TXT reports (default: output)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run simulation mode without sending network requests",
    )
    return parser.parse_args()


def main() -> None:
    guard = EthicalGuardrails()
    args = parse_arguments()

    # Step 1: Mandatory Startup Legal Disclaimer (Computer Crimes Act 1997)
    guard.display_legal_disclaimer()

    # Step 2: Enforce Safe Defaults & Target Scope Validation
    validated_dir = guard.validate_scope(
        target=args.target,
        target_dir=args.directory,
        endpoint_url=args.endpoint,
    )

    image_files = collect_image_files(validated_dir)
    print(f"[*] Target Scope      : {args.target}")
    print(f"[*] Target Directory  : {validated_dir} ({len(image_files)} image(s) found)")
    print(f"[*] Execution Mode    : {'DRY-RUN' if args.dry_run else 'ACTIVE AUDIT'}")

    # Step 3: Execute Core Footprinter (Member 1) & Risk Analyzer (Member 2)
    try:
        report_data = run_and_analyze(
            target=args.target,
            image_paths=image_files,
            dry_run=args.dry_run,
            endpoint_url=args.endpoint,
        )

        # Step 4: Display Formatted Terminal Output & Save Local-Only Reports (Member 2)
        display_terminal_report(
            report_data=report_data,
            target=args.target,
            dry_run=args.dry_run,
        )

        saved_paths = save_local_report(
            report_data=report_data,
            target=args.target,
            output_dir=args.output,
        )
        print(f"[+] JSON Report Saved : {saved_paths['json_path']}")
        print(f"[+] TXT Report Saved  : {saved_paths['txt_path']}")

    except Exception as exc:
        print(f"[!] Runtime error handled gracefully: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
