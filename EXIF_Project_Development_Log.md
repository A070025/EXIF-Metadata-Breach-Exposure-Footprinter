\# EXIF Metadata Breach \& Exposure Footprinter

\## Project Development Log



\*\*Course:\*\* IKB31603  

\*\*Project Category:\*\* Category 6 – Offensive OSINT  

\*\*Version:\*\* 1.0.0  

\*\*Repository:\*\* https://github.com/A070025/EXIF-Metadata-Breach-Exposure-Footprinter  

\*\*Documentation Date:\*\* 25 November 2026



\---



\## 1. Project Overview



EXIF Metadata Breach \& Exposure Footprinter is an OSINT security tool developed to identify potential information exposure through image metadata.



The tool extracts available EXIF metadata, analyzes potential exposure indicators, calculates risk levels, and generates local JSON and TXT reports.



The project is intended for authorized security auditing, cybersecurity education, and digital forensics training.



\## 2. Project Team and Responsibilities



The project was developed through collaboration among four members.



\- \*\*Member 1 – Core Development:\*\* Developed the core metadata extraction module and standardized raw output.

\- \*\*Member 2 – Analysis and Reporting:\*\* Developed finding analysis, risk scoring, terminal reporting, and local report generation.

\- \*\*Member 3 – CLI and Ethical Guardrails:\*\* Developed command-line functionality, target validation, authorization prompts, and scope restrictions.

\- \*\*Member 4 – Integration and QA:\*\* Managed repository integration, code review, testing, README improvements, documentation, and release preparation.



\## 3. Development Environment



The project was developed and tested using the following environment:



\- Operating System: Windows 11

\- Programming Language: Python 3.13.17

\- Code Editor: Visual Studio Code / Notepad

\- IDE / Terminal: Windows PowerShell

\- Version Control: Git

\- Remote Repository: GitHub

\- Image Processing Library: Pillow

\- HTTP Library: Requests



\## 4. Repository Setup and Git Workflow



The repository was cloned from GitHub to the local computer.



Git was used to manage source code changes, synchronize team contributions, resolve integration conflicts, and publish the final project version.



The main repository workflow included:



\- Cloning the project repository.

\- Reviewing source code and project structure.

\- Checking changes between local and remote branches.

\- Integrating team contributions.

\- Committing verified changes.

\- Pushing the updated main branch to GitHub.



\## 5. Code Review and Bug Fixes



During integration and code review, several issues were identified and addressed.



\### 5.1 Exposure Indicator Return Logic



The `check\_exposure\_indicators()` function in `core/footprinter.py` had a return statement positioned inside a loop.



This could cause the function to return after processing only the first result. It could also return an unexpected `None` value when no matching results were found.



\*\*Improvement:\*\* The return statement was moved outside the loop to ensure that all matching results are returned correctly, including an empty result list.



\### 5.2 Directory Validation



The directory validation function in `ethics/guardrails.py` did not properly verify whether an existing path was a directory.



This could cause an error when the selected path referred to a file instead of a directory.



\*\*Improvement:\*\* Added a directory validation check using `os.path.isdir()` before accessing directory contents.



\## 6. Integration and Merge Process



The local project branch had diverged from the remote `origin/main` branch.



A merge operation was performed to integrate the latest team contributions with local QA fixes.



A merge conflict was identified in:



`core/footprinter.py`



The conflict was reviewed and resolved while preserving the corrected return statement placement.



The merged changes were committed successfully.



\*\*Merge commit:\*\* `6a723c0`



The updated main branch was pushed to GitHub successfully.



\## 7. Quality Assurance (QA) Testing



Several checks were performed to verify project stability and integration.



| Test | Command | Result |

|---|---|---|

| CLI help | `python main.py --help` | Passed |

| Python compilation | `python -m py\_compile` | Passed |

| Whitespace validation | `git diff --check` | Passed |

| Dry-run execution | `python main.py --dry-run` | Passed |

| JSON report inspection | Manual inspection | Passed |

| TXT report inspection | Manual inspection | Passed |

| Git repository status | `git status` | Clean |



\## 8. Dry-Run Test Results



The project was tested using the synthetic EXIF sample image in `sample\_targets`.



The test used the default local target `127.0.0.1` and dry-run mode.



\*\*Test results:\*\*



\- Total unique findings: 5

\- Duplicate findings: 0

\- Overall risk score: 4.88/10.0

\- Overall risk level: MEDIUM

\- Critical findings: 0

\- High findings: 0

\- Medium findings: 1

\- Low findings: 4



The test generated both JSON and TXT reports successfully.



\*\*Important:\*\* The `EXP-DRY-001` finding is a simulated exposure indicator generated during dry-run testing. It does not represent a confirmed real-world data breach.



\## 9. GitHub Release v1.0.0



After integration and QA testing, the project was prepared for its first release.



The following release activities were completed:



\- Created annotated Git tag `v1.0.0`.

\- Pushed the tag to the remote GitHub repository.

\- Published the GitHub Release using the `v1.0.0` tag.

\- Prepared release notes describing features, testing, and limitations.



The release represents the integrated project version after the completed QA process.



\## 10. Final Project Status



The project integration and QA activities were completed successfully.



The main branch was synchronized with the remote repository, the working tree was clean, and the `v1.0.0` release was published.



The project includes metadata extraction, exposure analysis, risk scoring, reporting, and ethical scope controls.



Future improvements may include additional test cases, broader metadata format support, and further validation of optional exposure indicator integrations.



\---



\*\*Document prepared for:\*\* IKB31603 Cybersecurity Project  

\*\*Role:\*\* Member 4 – Integration and QA

