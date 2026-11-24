# EXIF-Metadata-Breach-Exposure-Footprinter
A modular cybersecurity assessment tool developed for educational and authorized security testing.


























## Limitations

* **Metadata Stripping on Social Platforms:** Most modern social media and messaging services (e.g., WhatsApp, Instagram, Facebook, X) automatically strip EXIF and GPS headers upon upload. Meaningful metadata extraction is primarily effective on original, uncompressed, or directly transferred image files.
* **Breach Endpoint Scope and Rate Limits:** Breach exposure detection relies on configured lookup endpoints or `--dry-run` simulation data. Unauthenticated queries against public OSINT APIs may be subject to strict rate limits and do not cover private or unindexed datasets.
* **Passive Reconnaissance Only:** This tool performs passive footprinting and metadata analysis only. It does not verify whether exposed credentials remain active, nor does it perform active probing or exploitation.
* **Local-Only Execution Policy:** All generated JSON and TXT reports are stored exclusively in the local `./output/` directory with zero external telemetry or data exfiltration. Users are responsible for ensuring proper authorization before scanning any target or file.
