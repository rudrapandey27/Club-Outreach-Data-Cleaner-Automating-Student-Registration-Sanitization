import csv
import re
import os

# ── File paths ──────────────────────────────────────────────────────────────
INPUT_FILE  = "raw_signups.csv"
OUTPUT_FILE = "clean_attendees.csv"
ERROR_FILE  = "error_log.csv"

# ── Validation helpers ───────────────────────────────────────────────────────

# BUG 1 FIX: Strict pattern — 2 digits + 3 uppercase letters + 5 digits
REG_PATTERN = re.compile(r"^\d{2}[A-Z]{3}\d{5}$")

def is_valid_registration(reg_id: str) -> bool:
    """Return True only if reg_id matches the university format e.g. 25BEC10025."""
    return bool(REG_PATTERN.match(reg_id))

def is_valid_email(email: str) -> bool:
    """
    BUG 2 FIX: Structural email check.
    Ensures format is  something@domain.tld  — not just '@' presence.
    """
    pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return bool(pattern.match(email))

# ── Main cleaner ─────────────────────────────────────────────────────────────

def clean_data(input_path: str, output_path: str, error_path: str) -> None:
    if not os.path.exists(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        return

    seen_ids: set[str] = set()   # tracks already-processed registration numbers

    clean_rows: list[dict] = []
    error_rows: list[dict] = []

    with open(input_path, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            # BUG 3 FIX: Normalise whitespace and case before any comparison
            name   = row.get("Name", "").strip()
            reg_id = row.get("Registration Number", "").strip().upper()
            email  = row.get("Email", "").strip()

            # ── Duplicate check ──────────────────────────────────────────────
            if reg_id in seen_ids:
                error_rows.append({
                    "Name": name,
                    "Registration Number": reg_id,
                    "Email": email,
                    "Error Reason": "Duplicate Entry",
                })
                continue

            # ── Registration format check ────────────────────────────────────
            if not is_valid_registration(reg_id):
                error_rows.append({
                    "Name": name,
                    "Registration Number": reg_id,
                    "Email": email,
                    "Error Reason": "Invalid Registration Format",
                })
                continue

            # ── Email format check ───────────────────────────────────────────
            if not is_valid_email(email):
                error_rows.append({
                    "Name": name,
                    "Registration Number": reg_id,
                    "Email": email,
                    "Error Reason": "Invalid Email Format",
                })
                continue

            # ── All checks passed ────────────────────────────────────────────
            seen_ids.add(reg_id)
            clean_rows.append({
                "Name": name,
                "Registration Number": reg_id,
                "Email": email,
            })

    # BUG 4 FIX: Always pass newline='' to open() when using csv.writer/DictWriter
    #            (prevents blank rows between data rows on Windows)
    clean_fieldnames = ["Name", "Registration Number", "Email"]
    with open(output_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=clean_fieldnames)
        writer.writeheader()
        writer.writerows(clean_rows)

    error_fieldnames = ["Name", "Registration Number", "Email", "Error Reason"]
    with open(error_path, "w", newline="", encoding="utf-8") as errfile:
        writer = csv.DictWriter(errfile, fieldnames=error_fieldnames)
        writer.writeheader()
        writer.writerows(error_rows)

    print(f"✅  Clean records   : {len(clean_rows)}  → {output_path}")
    print(f"❌  Error records   : {len(error_rows)}  → {error_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    clean_data(INPUT_FILE, OUTPUT_FILE, ERROR_FILE) 