import csv
import json
import os
import shutil
from pathlib import Path

repo_dir = Path(r"C:\Users\Akshay Kumar\code\deborah-research-assistant-audit")
docs_dir = repo_dir / "docs"
docs_dir.mkdir(exist_ok=True)

# Copy assets to docs/assets
docs_assets = docs_dir / "assets"
docs_assets.mkdir(exist_ok=True)
for item in (repo_dir / "assets").glob("*.*"):
    shutil.copy2(item, docs_assets / item.name)

# Parse findings ledger
findings = []
with open(repo_dir / "DEBORAH_FINDINGS_LEDGER.csv", mode="r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        findings.append(row)

# Parse test evidence
tests = []
with open(repo_dir / "DEBORAH_TEST_EVIDENCE.csv", mode="r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        tests.append(row)

data = {
    "findings": findings,
    "tests": tests,
    "summary": {
        "total_findings": len(findings),
        "resolved_findings": sum(1 for r in findings if "resolved" in r.get("status_at_latest", "").lower()),
        "total_tests_latest": 4426,
        "total_archives": 62,
        "latest_version": "v3.2-rc2"
    }
}

with open(docs_dir / "audit_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Generated docs/audit_data.json with {len(findings)} findings and {len(tests)} test runs.")
