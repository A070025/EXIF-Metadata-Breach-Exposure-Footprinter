# EXIF Project – PowerShell Execution Log

**Project:** EXIF-Metadata-Breach-Exposure-Footprinter
**Course:** IKB31603 – Cybersecurity Project
**Category:** Category 6 – Offensive OSINT
**Repository:** https://github.com/A070025/EXIF-Metadata-Breach-Exposure-Footprinter
**Branch:** main
**Documentation Date:** 25 November 2026

---

## 1. Purpose

This document records selected PowerShell commands, Git operations, testing activities, results, and troubleshooting performed during the development and integration of the EXIF Metadata Breach & Exposure Footprinter project.

It serves as a supplementary technical record alongside the project's README and Development Log.

**Record limitation:** This document is reconstructed from available command history and project records. It is not a complete PowerShell transcript. Some historical terminal outputs were not saved.

## 2. Development Environment

| Item | Details |
|---|---|
| Operating System | Windows |
| Terminal | Windows PowerShell |
| Programming Language | Python |
| Version Control | Git |
| Remote Repository | GitHub |
| Main Branch | main |
| Project Directory | EXIF-Metadata-Breach-Exposure-Footprinter |

## 3. Project Directory

The project was accessed from a local Windows working directory.

For privacy, the complete local directory path and Windows username are intentionally omitted.

## 4. Important PowerShell Commands

### 4.1 Project Inspection

```powershell
Get-ChildItem -Force
Get-Content .\main.py
Get-Content .\qa_output\*.json
Get-Content .\core\footprinter.py
Get-Content .\ethics\guardrails.py
```

These commands were used to inspect project files, source code, and generated test results.

### 4.2 Python Testing

```powershell
python main.py --help
python main.py --dry-run
```

Purpose:

- Verify CLI argument information.
- Execute the project in dry-run mode.
- Check integration of the main project modules.
- Review the terminal report and generated output files.

### 4.3 Git Inspection

```powershell
git status
git log --oneline --graph --decorate -10
git diff origin/main -- core/footprinter.py ethics/guardrails.py
```

These commands were used to inspect repository status, commit history, and source-code differences.

## 5. Quality Assurance Results

The following results were recorded during the dry-run test before the latest remote changes were merged.

**Test command:**

```powershell
python main.py --dry-run
```

**Recorded results:**

| Test item | Result |
|---|---|
| Target | 127.0.0.1 |
| Test mode | Dry-run |
| Images processed | 1 |
| Unique findings | 5 |
| Duplicate findings | 0 |
| Overall risk score | 4.88/10.0 |
| Overall severity | MEDIUM |

### 5.1 Severity Summary

| Severity | Findings |
|---|---:|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 1 |
| LOW | 4 |
| INFO | 0 |

### 5.2 Generated Reports

The application generated local JSON and TXT reports.

Example output filenames:

```text
exif_breach_footprinter_127.0.0.1_20261125_021036.json
exif_breach_footprinter_127.0.0.1_20261125_021036.txt
```

The reports were reviewed to compare their findings and summary information.

**Important:** The `EXP-DRY-001` finding was simulated by the dry-run mechanism. It does not represent proof of an actual data breach or a real external exposure lookup.

## 6. Code Fixes and Integration

### 6.1 Core Footprinter

File:

```text
core/footprinter.py
```

Issue:

- The return statement in the exposure indicator checking function was incorrectly positioned inside a loop.
- This could cause incomplete results or return an unexpected value when no matches were found.

Correction:

- Moved the return statement outside the loop while keeping it inside the appropriate try block.
- Checked multiple-match, empty-match, and request-error scenarios using mock tests.

### 6.2 Ethics Guardrails

File:

```text
ethics/guardrails.py
```

Issue:

- Directory validation did not properly reject a path that pointed to a file instead of a directory.

Correction:

```python
if not os.path.isdir(abs_dir):
    print(f"[!] SCOPE VIOLATION: '{abs_dir}' is not a valid directory.")
    sys.exit(1)
```

The validation was checked using a file path and a missing directory scenario.

## 7. Git Version Control Activities

### 7.1 Check Repository Status

```powershell
git status
```

### 7.2 Add and Commit Documentation

```powershell
git add README.md
git commit -m "docs: improve project README documentation"
```

Development Log commit:

```powershell
git add EXIF_Project_Development_Log.md
git commit -m "docs: add project development log"
```

PowerShell Execution Log commit:

```powershell
git add EXIF_Project_PowerShell_Execution_Log.md
git commit -m "docs: add PowerShell execution log"
```

### 7.3 Fetch Remote Changes

```powershell
git fetch origin
```

The remote branch contained new commits that were not yet integrated into the local branch.

### 7.4 Merge Remote Changes

```powershell
git merge origin/main
```

The merge completed successfully using the `ort` strategy.

Changes included:

- README documentation updates.
- Pinned Pillow and Requests dependency versions.
- Addition of a real image sample.
- Removal of the previous QA test image.

### 7.5 Push Changes to GitHub

```powershell
git push origin main
```

Recorded successful pushes included:

```text
8546bbd..8681e8b main -> main
8681e8b..b44b300 main -> main
```

### 7.6 Final Repository Verification

```powershell
git status
```

Recorded final result:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Final Git status:** Successful.

## 8. GitHub Release

The project release was published as:

```text
v1.0.0
```

The release tag remains associated with commit:

```text
6a723c0
```

Subsequent documentation and merge commits were pushed to the `main` branch without changing the existing release tag.

## 9. PowerShell Command History Backup

The PowerShell command history was backed up to the user's Desktop.

Backup filenames:

```text
EXIF_Project_All_Commands.txt
EXIF_Project_All_Commands.csv
```

The original PowerShell history file was located at the standard PSReadLine history location:

```text
ConsoleHost_history.txt
```

The backup was created using the following commands:

```powershell
Copy-Item (Get-PSReadLineOption).HistorySavePath "$([Environment]::GetFolderPath('Desktop'))\EXIF_Project_All_Commands.txt"
```

CSV export:

```powershell
$history = Get-Content (Get-PSReadLineOption).HistorySavePath
$history | ForEach-Object { [PSCustomObject]@{ Command = $_ } } | Export-Csv "$([Environment]::GetFolderPath('Desktop'))\EXIF_Project_All_Commands.csv" -NoTypeInformation -Encoding UTF8
```

**Important limitation:** These backup files contain recorded commands only. They do not contain all historical terminal outputs or a complete PowerShell transcript.

## 10. Troubleshooting and Lessons Learned

The following issues occurred during project documentation and Git operations:

| Issue | Resolution |
|---|---|
| Git push rejected because the remote branch had new commits | Fetched remote changes and merged `origin/main` |
| Git opened a text editor during merge | Completed the merge commit using the editor |
| Incorrect attempt to execute a folder path as a command | Used the correct command to open the project file |
| PowerShell history did not contain terminal outputs | Created command-history backups and reconstructed available results |
| Execution Log was incomplete | Prepared a corrected and complete documentation version |

These activities helped improve familiarity with PowerShell, Git version control, project documentation, and troubleshooting.

## 11. Final Status and Conclusion

| Activity | Status |
|---|---|
| Project source inspection | Completed |
| Dry-run QA test | Completed for pre-latest-merge state |
| JSON and TXT report review | Completed |
| Core module correction | Completed |
| Ethics guardrails correction | Completed |
| Development Log | Committed and pushed |
| PowerShell Execution Log | Committed and pushed |
| Remote Git changes | Merged |
| GitHub push | Successful |
| Final Git status | Clean |
| Release v1.0.0 | Published |

The documented PowerShell activities cover project inspection, QA testing, code corrections, Git version control, remote integration, command-history backup, and final repository verification.

The local repository was successfully synchronized with GitHub. The final Git status confirmed that the `main` branch was up to date with `origin/main` and the working tree was clean.

This execution log is intended to provide a supplementary record of the project's development and integration activities.

---

**End of Document**