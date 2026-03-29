# 📊 Student Club Outreach Data Cleaner

## 📌 Project Overview
During university club recruitment drives, the PR and Outreach team relies on digital forms to collect student sign-ups. However, the resulting raw data is often highly unstructured. Students frequently submit duplicate entries, mistype their 10-character university registration numbers, or provide invalid email addresses. 

This project is a Python-based automation tool built to solve this exact logistical bottleneck. It ingests messy, raw CSV data, systematically cleans it using string manipulation and conditional logic, and outputs a pristine dataset ready for official club communications.

## ✨ Key Features
* **Automated Duplicate Removal:** Utilizes Python `sets` to ensure no registration number is processed twice, executing in $O(1)$ time complexity to save hours of manual sorting.
* **Format Validation:** Strictly checks registration numbers against the university's standard 10-character alphanumeric format (e.g., `25BEC10025`).
* **Email Verification:** Performs structural checks on provided email addresses to catch common typos (missing `@` or domain).
* **Non-Destructive Error Logging:** Instead of just deleting bad data, it routes invalid entries to a separate `error_log.csv` with the specific rejection reason, allowing the team to manually follow up if necessary.

## 📥 Input vs. 📤 Output Example

**Raw Input (`raw_signups.csv`):**
| Name | Registration Number | Email |
| :--- | :--- | :--- |
| Rudra Pandey | 25BEC10025 | rudra@university.edu |
| Neha Gupta | 25BEC10050 | neha@university.edu |
| Rudra Pandey | 25BEC10025 | rudra@university.edu *(Duplicate!)* |
| Random Student | 12345 | random.com *(Bad ID & Email!)* |

**Clean Output (`clean_attendees.csv`):**
*(The perfect list used to send out club emails)*
| Name | Registration Number | Email |
| :--- | :--- | :--- |
| Rudra Pandey | 25BEC10025 | rudra@university.edu |
| Neha Gupta | 25BEC10050 | neha@university.edu |

**Error Log (`error_log.csv`):**
| Name | Registration Number | Email | Error Reason |
| :--- | :--- | :--- | :--- |
| Rudra Pandey | 25BEC10025 | rudra@university.edu | Duplicate Entry |
| Random Student | 12345 | random.com | Invalid Registration Format |

## ⚙️ Prerequisites
* Python 3.x installed on your system.
* A basic terminal or command prompt.

## 🚀 Setup & Usage Instructions

1. **Clone the Repository:**
   Download the project files to your local machine.
   ```bash
   git clone <your-github-repo-url>

AUTHOR :[RUDRA PANDEY]
REGISRATION NO.[25BEC10025]
VIT BHOPAL UNIVERSITY
