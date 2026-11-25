# EXIF-Metadata-Breach-Exposure-Footprinter

A Python-based Offensive OSINT tool developed for educational purposes and authorized cybersecurity assessments under the IKB31603 Ethical Hacking course.

This tool extracts metadata from local image files, identifies potential privacy exposure indicators, and evaluates possible breach exposure using a risk analysis module. It generates structured JSON and TXT reports to help users understand the information that may be exposed through image metadata.

The project follows an ethical testing approach with authorization confirmation, target scope validation, and local report storage.

## Key Features

- **EXIF Metadata Extraction:** Extracts available metadata from supported image files, including camera information, software details, timestamps, and GPS coordinates.
- **GPS Coordinate Processing:** Converts GPS coordinates into decimal format when GPS metadata is available.
- **Exposure Indicator Checking:** Performs digest-based exposure lookups through an optional authorized API endpoint.
- **Risk Assessment:** Evaluates identified exposure indicators and assigns risk levels based on the analysis results.
- **Duplicate Filtering:** Identifies and removes duplicate findings during analysis.
- **Remediation Suggestions:** Provides recommendations to help users reduce potential information exposure.
- **Report Generation:** Generates structured JSON and TXT reports.
- **Ethical Guardrails:** Includes authorization confirmation, target scope validation, and a Ctrl+C emergency stop handler.
- **Dry-Run Mode:** Supports simulated execution without sending network requests.

## Project Structure

```text
EXIF-Metadata-Breach-Exposure-Footprinter/
│
├── analysis/
│   ├── analyzer.py
│   ├── reporter.py
│   └── __init__.py
│
├── core/
│   ├── footprinter.py
│   └── __init__.py
│
├── ethics/
│   ├── guardrails.py
│   └── __init__.py
│
├── sample_targets/
│   └── qa_exif_test.jpg
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### Module Description

| Module | Description |
|---|---|
| `main.py` | Main entry point and command-line interface |
| `core/` | Handles metadata extraction and exposure indicator checks |
| `analysis/` | Performs risk analysis and generates reports |
| `ethics/` | Handles authorization, scope validation, and emergency stop controls |
| `sample_targets/` | Contains sample images for testing |

## System Requirements

- Python 3.10 or newer
- Git
- Internet connection only when using an authorized external network endpoint
- Windows operating system (tested environment)

Other operating systems may require additional compatibility testing.

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/A070025/EXIF-Metadata-Breach-Exposure-Footprinter.git
```

### 2. Navigate to the Project Directory

```bash
cd EXIF-Metadata-Breach-Exposure-Footprinter
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The required Python libraries are:

- Pillow
- Requests

### 4. Verify the Installation

```bash
python main.py --help
```

This command displays the available command-line options.

## Usage Instructions

Before execution, users must review the legal disclaimer and confirm that they have authorization to perform the assessment.

### 1. Run in Dry-Run Mode

```bash
python main.py --dry-run
```

This runs the tool in simulation mode without sending network requests.

### 2. Run an Authorized Local Assessment

```bash
python main.py -t 127.0.0.1 -d ./sample_targets
```

This command processes supported image files inside the specified local directory.

### 3. Specify an Output Directory

```bash
python main.py -t 127.0.0.1 -d ./sample_targets -o ./output
```

This stores the generated reports in the specified output directory.

**Note:** The `--target` argument is a target identifier used by the application. Specifying a domain such as `example.com` does not mean that the tool scans or extracts images from that website. Image processing is performed on local files supplied through the `--directory` argument.

## Command-Line Arguments

| Argument | Description | Default |
|---|---|---|
| `-h`, `--help` | Displays help information | — |
| `-t`, `--target` | Specifies the authorized target identifier | `127.0.0.1` |
| `-d`, `--directory` | Specifies the local image directory | `./sample_targets` |
| `-e`, `--endpoint` | Specifies an optional authorized API endpoint | `None` |
| `-o`, `--output` | Specifies the report output directory | `output` |
| `--dry-run` | Runs simulation mode without network requests | Disabled |

## Optional API Endpoint

The tool supports an optional endpoint for digest-based exposure lookups.

When this feature is used:

1. The tool generates a SHA-256 digest from the relevant data.
2. Only a truncated 12-character digest prefix is sent as a query parameter.
3. The endpoint response is processed by the application.
4. Matching exposure indicators may be included in the analysis report.

The endpoint must be within the configured hostname allowlist:

- `127.0.0.1`
- `localhost`
- `example.com`

The expected response contains a top-level JSON `matches` array. Individual match entries may contain a `summary` field.

**Important:** A truncated digest prefix is not equivalent to sending the original plaintext data, but it may still reveal information through matching or correlation. Use only an endpoint that has been explicitly authorized.

No external endpoint is configured by default.

## Output Reports

The tool generates two report formats:

### JSON Report

The JSON report stores structured assessment information, including metadata findings and analysis results. It is suitable for further processing and integration with other tools.

### TXT Report

The TXT report provides a readable summary of the assessment results for documentation and review.

By default, reports are saved inside the local `output/` directory.

Users should protect generated reports because they may contain sensitive metadata, such as GPS coordinates, device identifiers, or exposure indicators.

## Purpose
**The EXIF Metadata & Breach Exposure Footprinter CLI** is an authorized open-source intelligence (OSINT) and passive reconnaissance command-line tool designed to identify unintended information disclosure across digital media and target identifiers. Specifically, it inspects image files for embedded Exchangeable Image File Format (EXIF) metadata such as camera make/model, editing software, creation timestamps, and GPS coordinates while performing controlled, privacy-preserving breach-exposure indicator checks on authorized target identifies.

## System Architecture
The application follows a decoupled, four-layer modular architecture to separate core intelligence gathering, secondary risk analysis, user presentation, and ethical safety controls:

* **CLI & Ethical Guardrails Layer (`main.py / guardrails`):** Parses command-line flags (`argparse`), enforces default safe targets( `localhost`, `127.0.0.1`, `example.com`), validates target scope prior to execution, displays the mandatory Computer Crimes Act startup disclaimer, and handles clean interrupt termination (`SIGINT`).
* **Core Footprinting Engine (`core/footprinter.py`):** Executes the primary intelligence extraction logic through modular functions (`extract_exif_findings`, `check_exposure_indicators`, and `run_footprint_core`) and standardize raw findings into a uniform list of dictionaries.
* **Secondary Analysis Module (`analyzer`):** Ingests standardized records from `core/footprinter.py` to perform deduplication, severity classification, and risk scoring while safely handling empty or incomplete datasets.
* **Reporting & Local Storage Module (`reporter`):** Formats processed results into aligned console tables and writes timestamped, locally stored output reports without external data exfiltration.

## Execution Workflow
1. **Startup & Scope Verification:** The user invokes the CLI with target parameters and optional image paths. The guardrails module displays the legal disclaimer, requires explicit user confirmation, and validates that the target falls within authorized scope.

2. **EXIF Metadata Extraction:** If image paths are supplied, `extract_exif_findings()` opens each image safely using `Pillow`(`PIL.Image` and `PIL.ExifTags`), inspects standard device/software tags(`Make`, `Model`, `Software`, `DateTimeOriginal`), and converts raw Degree-Minutes-Seconds(DMS) GPS tags into decimal latitude and longitude coordinates via `_dms_to_decimal()`.

3. **Breach Exposure Indicator Check:** `check_exposure_indicators()` normalizes the target string and generates an anonymized 12-character SHA-256 lookup digest prefix (`digest_prefix`). Depending on runtime flags, it either simulates the check(`--dry-run`), performs a local digest check when no endpoint is specified, or queries an authorized lookup endpoint using only the truncated hash prefix.

4. **Schema Standardization & Handoff:** `run_footprint_core()` aggregates all EXIF and exposure findings into standardized 8-field records (`record_id`, `category`, `source`, `target`, `indicator`, `raw_value`, `confidence`, `timestamp`) and passes them downstream for risk analysis, terminal rendering, and local report generation.
 
## Limitations

- **Metadata Availability:** Metadata extraction depends on the information embedded in the original image. Some social media and messaging platforms may remove or modify EXIF metadata during upload or image processing.
- **Endpoint Dependency:** Exposure lookup results depend on the configured endpoint, its available dataset, and its supported response format.
- **No Credential Verification:** The tool does not verify whether exposed credentials are currently valid.
- **Passive Assessment:** The tool does not perform brute-force attacks, active exploitation, or unauthorized system access.
- **Risk Assessment:** Risk scores represent potential exposure indicators and should not be treated as proof of an actual security breach.
- **Local Image Scope:** The tool processes supported image files from a specified local directory. It does not automatically download images from websites.

## Legal Disclaimer

This project is developed strictly for educational, research, digital forensics training, and authorized cybersecurity assessment purposes under the IKB31603 Ethical Hacking course at Universiti Kuala Lumpur (UniKL MIIT).

Users must obtain proper authorization from the relevant asset owner before performing any assessment.

Unauthorized access, misuse of personal information, or activities outside the approved assessment scope may violate applicable laws, including the Malaysia Computer Crimes Act 1997 (Act 563) and the Personal Data Protection Act 2010 (PDPA), where applicable.

The developers do not encourage or support unauthorized activities. Users are responsible for ensuring that their use of this software complies with applicable laws, policies, and authorization requirements.

## Rules of Engagement (RoE)

All users must follow these Rules of Engagement:

1. **Authorized Scope:** Only assess files, systems, and endpoints that are owned by the user or covered by explicit authorization.
2. **Target Restrictions:** Follow the application's configured target validation and use approved laboratory environments only.
3. **Permitted Activities:** Perform local EXIF metadata inspection and authorized digest-based exposure lookups only.
4. **Prohibited Activities:** Do not perform unauthorized access, brute-force attacks, denial-of-service attacks, or unauthorized data collection.
5. **Data Protection:** Do not transmit plaintext credentials or complete sensitive hashes to unauthorized services.
6. **Report Handling:** Store generated reports securely and share findings only with authorized parties.
7. **Emergency Stop:** Use `Ctrl+C` to request immediate termination through the built-in SIGINT handler.

## Responsible Disclosure

If sensitive information or potential exposure indicators are identified during an authorized assessment:

- Notify the relevant system administrator or asset owner through an approved communication channel.
- Provide sufficient evidence to explain the finding without unnecessarily exposing sensitive information.
- Include practical remediation recommendations.
- Avoid public disclosure until the responsible organization has reviewed and addressed the issue.

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more information.

---

**Developed for:** IKB31603 Ethical Hacking

**Institution:** Universiti Kuala Lumpur (UniKL MIIT)

**Project Category:** Category 6 – Offensive OSINT

**Version:** 1.0.0