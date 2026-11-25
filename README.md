# EXIF-Metadata-Breach-Exposure-Footprinter
A modular cybersecurity assessment tool developed for educational and authorized security testing.


























## Limitations

* **Metadata Stripping on Social Platforms:** Most modern social media and messaging services (e.g., WhatsApp, Instagram, Facebook, X) automatically strip EXIF and GPS headers upon upload. Meaningful metadata extraction is primarily effective on original, uncompressed, or directly transferred image files.
* **Breach Endpoint Scope and Rate Limits:** Breach exposure detection relies on configured lookup endpoints or `--dry-run` simulation data. Unauthenticated queries against public OSINT APIs may be subject to strict rate limits and do not cover private or unindexed datasets.
* **Passive Reconnaissance Only:** This tool performs passive footprinting and metadata analysis only. It does not verify whether exposed credentials remain active, nor does it perform active probing or exploitation.
* **Local-Only Execution Policy:** All generated JSON and TXT reports are stored exclusively in the local `./output/` directory with zero external telemetry or data exfiltration. Users are responsible for ensuring proper authorization before scanning any target or file.

* ## Legal Disclaimer
**EXIF-Metadata-Breach-Exposure-Footprinter** is developed strictly for educational, research, and authorized security auditing purposes under the **IKB31603 Ethical Hacking** course at Universiti Kuala Lumpur (UniKL MIIT). Unauthorized extraction of metadata, profiling of individuals, or querying breach exposure indicators without explicit written authorization from the asset owner violates the **Malaysia Computer Crimes Act 1997 (Act 563)** and the **Personal Data Protection Act 2010 (PDPA)**. The authors assume zero liability for any misuse or unlawful activity conducted with this software.

## Rules of Engagement (RoE)
All operators using this tool must strictly comply with the following Rules of Engagement:
1. **Authorized Scope:** Execution is strictly confined to locally owned sample files (`./sample_targets`), loopback addresses (`127.0.0.1`, `localhost`), `example.com`, or explicitly authorized lab environments. Scanning system root directories or unauthorized public targets is prohibited.
2. **Time Windows:** Execution and authorized endpoint queries must only be conducted during approved laboratory sessions or scheduled assessment windows authorized by the asset owner.
3. **Permitted Techniques:** Only passive local EXIF metadata inspection (device tags, timestamps, GPS coordinates) and privacy-preserving SHA-256 prefix digest checks (sending only a 12-character truncated hash prefix) are permitted.
4. **Prohibited Actions:** Transmitting plaintext credentials or full hashes over the network, brute-forcing external services, scraping unauthorized public domains, and denial-of-service (DoS) request flooding are strictly prohibited.
5. **Emergency Stop Procedures:** Operators can immediately halt execution at any stage using the built-in **Kill Switch (`Ctrl+C` / `SIGINT`)**, which terminates all operations cleanly without leaving orphaned sockets or corrupting local report files.

## Responsible Disclosure Policy
If sensitive metadata (such as embedded GPS coordinates, internal device identifiers, or breach exposure indicators) is identified during an authorized audit:
* **Who to Contact:** Report findings directly to the designated System Administrator, Asset Owner, or the organization's Computer Security Incident Response Team (e.g., MyCERT for Malaysian national infrastructure).
* **When to Report:** Submit an initial confidential notification within **24 hours** of verification. Do not publicly disclose any findings until the asset owner has completed remediation (standard 90-day disclosure window).
* **How to Report:** Transmit findings over an encrypted communication channel (such as PGP-encrypted email) containing only redacted proof-of-concept details, affected file names, and remediation steps (such as stripping EXIF metadata via `exiftool` prior to public release).
