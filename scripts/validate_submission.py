from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "01_CabinSentinel_One_Page_Brief.pdf",
    "02_CabinSentinel_PRD.pdf",
    "03_CabinSentinel_Wireframe_UI_Flow.pdf",
    "04_Gate_G1_Checklist.pdf",
    "README_Submission.txt",
    "AI_LOG.md",
]

errors = []
for name in REQUIRED:
    path = ROOT / name
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"missing or empty: {name}")

for name in [n for n in REQUIRED if n.endswith(".pdf")]:
    path = ROOT / name
    if path.is_file() and path.read_bytes()[:5] != b"%PDF-":
        errors.append(f"invalid PDF signature: {name}")

brief = ROOT / REQUIRED[0]
if brief.is_file():
    data = brief.read_bytes()
    # Chromium PDFs expose one /Type /Page object per page plus /Pages; this is a simple guard.
    page_count = data.count(b"/Type /Page\n")
    if page_count != 1:
        errors.append(f"brief must be exactly 1 page; detected {page_count}")

readme = ROOT / "README_Submission.txt"
if readme.is_file() and "Confirmed public repository" not in readme.read_text(encoding="utf-8"):
    errors.append("README repository section missing")

if errors:
    print("Gate G1 validation FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Gate G1 validation PASSED")
