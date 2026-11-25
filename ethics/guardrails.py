import ipaddress
import os
import signal
import sys
from urllib.parse import urlparse


class EthicalGuardrails:
    """Enforces mandatory ethical controls: Kill Switch, CCA 1997 Disclaimer, and Scope Validation."""

    def __init__(self) -> None:
        # Register Ctrl+C (SIGINT) as an immediate clean Kill Switch
        signal.signal(signal.SIGINT, self._kill_switch_handler)

    def _kill_switch_handler(self, signum: int, frame: object) -> None:
        """Cleanly aborts execution when SIGINT (Ctrl+C) is triggered."""
        print("\n\n[!] EMERGENCY KILL SWITCH ACTIVATED (SIGINT / Ctrl+C).")
        print("[!] Aborting all OSINT metadata and exposure checks cleanly...")
        print("[!] Zero data exfiltrated. Exiting safely.")
        sys.exit(0)

    def display_legal_disclaimer(self) -> None:
        """Displays startup legal disclaimer referencing Malaysia Computer Crimes Act 1997."""
        banner = """
================================================================================
  LEGAL DISCLAIMER & AUTHORIZATION WARNING
  Tool: EXIF-Metadata-Breach-Exposure-Footprinter (Category 6: Offensive OSINT)
================================================================================
  This tool is developed strictly for authorized security auditing, digital
  forensics training, and educational purposes (IKB31603).

  Unauthorized extraction of metadata, profiling of individuals, or querying
  breach exposure indicators without explicit written permission from the
  asset owner is an offence under the MALAYSIA COMPUTER CRIMES ACT 1997
  (Act 563) and the Personal Data Protection Act 2010 (PDPA).

  By proceeding, you confirm that:
  1. You own the target files/assets OR hold explicit written authorization.
  2. You will adhere strictly to the Rules of Engagement (RoE).
================================================================================
        """
        print(banner)
        try:
            consent = input(
                "[?] Do you confirm you have explicit authorization? (Type 'YES' to proceed): "
            ).strip()
        except EOFError:
            print("\n[!] Input stream closed. Execution aborted.")
            sys.exit(1)

        if consent != "YES":
            print("[!] Explicit authorization not confirmed. Exiting safely.")
            sys.exit(0)

        print("[+] Authorization confirmed. Proceeding within authorized scope...\n")

    def validate_scope(
        self,
        target: str,
        target_dir: str,
        endpoint_url: str | None = None,
    ) -> str:
        """
        Validates target identifier, local directory path, and optional API endpoint
        against safe defaults and authorized lab boundaries.
        """
        # 1. Validate Target Identifier (Safe defaults: 127.0.0.1, localhost, example.com, or private IPs)
        clean_target = target.strip().lower()
        allowed_static_targets = {"127.0.0.1", "localhost", "example.com"}

        if (
            clean_target not in allowed_static_targets
            and not clean_target.endswith(".local")
            and not clean_target.endswith("@example.com")
        ):
            try:
                ip_obj = ipaddress.ip_address(clean_target)
                if not (ip_obj.is_loopback or ip_obj.is_private):
                    print(f"[!] SCOPE VIOLATION: Public IP '{target}' is outside authorized scope.")
                    print("[!] Safe Default: Use '127.0.0.1', 'localhost', or 'example.com'.")
                    sys.exit(1)
            except ValueError:
                print(f"[!] SCOPE VIOLATION: Target '{target}' is not in the authorized test scope.")
                print("[!] Allowed defaults: 127.0.0.1, localhost, example.com, or *.local")
                sys.exit(1)

        # 2. Validate Local Directory Scope (Block scanning sensitive OS directories)
        abs_dir = os.path.abspath(target_dir)
        restricted_roots = [
            "/", "/etc", "/bin", "/sbin", "/usr", "/var", "/root",
            "C:\\", "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)"
        ]
        if abs_dir in restricted_roots or any(
            abs_dir.startswith(r + os.sep) for r in ["/etc", "/bin", "/usr", "C:\\Windows"]
        ):
            print(f"[!] SCOPE VIOLATION: Scanning system directory '{abs_dir}' is prohibited.")
            sys.exit(1)

        if not os.path.exists(abs_dir):
            os.makedirs(abs_dir, exist_ok=True)
            print(f"[*] Created safe default target directory: {abs_dir}")

        if not os.path.isdir(abs_dir):
            print(f"[!] SCOPE VIOLATION: '{abs_dir}' is not a valid directory.")
            sys.exit(1)

        # 3. Validate Optional Endpoint URL (Must point to localhost / 127.0.0.1 / example.com)
        if endpoint_url:
            parsed = urlparse(endpoint_url)
            host = (parsed.hostname or "").lower()
            if host not in {"127.0.0.1", "localhost", "example.com"}:
                print(f"[!] SCOPE VIOLATION: External endpoint '{endpoint_url}' is unauthorized.")
                sys.exit(1)

        return abs_dir
