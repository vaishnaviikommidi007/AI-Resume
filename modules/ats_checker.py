"""Basic resume structure/readability checklist, not an official ATS test."""
import re
from modules.resume_parser import get_resume_sections

def check_resume(text: str, file_name: str = "") -> dict:
    if not text or not text.strip():
        return {"score": 0, "checks": [
            {"name": "Readable text", "passed": False, "details": "No text was extracted."}],
            "warnings": ["Scanned PDFs may require OCR."]}
    sections = get_resume_sections(text)
    words = len(text.split())
    email = bool(
    re.search(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        text,
        re.IGNORECASE
    )
    )
    phone = bool(re.search(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)", text))
    checks = [
        {"name": "Readable text", "passed": True, "details": f"Extracted approximately {words} words."},
        {"name": "Email address", "passed": email, "details": "Email detected." if email else "No email detected."},
        {"name": "Phone number", "passed": phone, "details": "Phone-like number detected." if phone else "No phone detected."},
        {"name": "Education section", "passed": "education" in sections, "details": "Education heading detected." if "education" in sections else "Education heading not detected."},
        {"name": "Skills section", "passed": "skills" in sections, "details": "Skills heading detected." if "skills" in sections else "Skills heading not detected."},
        {"name": "Projects or experience", "passed": ("projects" in sections or "experience" in sections), "details": "Projects/experience heading detected." if ("projects" in sections or "experience" in sections) else "No common projects/experience heading detected."},
        {"name": "Length", "passed": 150 <= words <= 1200, "details": f"{words} words; broad heuristic only."},
    ]
    score = round(100 * sum(c["passed"] for c in checks) / len(checks))
    warnings = [
        "This checklist is not a real ATS compatibility test or hiring prediction.",
        "Section detection uses common headings and may miss unusual formatting.",
        "Review every result manually before changing your resume.",
    ]
    if file_name and not file_name.lower().endswith(".pdf"):
        warnings.append("Filename does not end in .pdf.")
    return {"score": score, "checks": checks, "warnings": warnings}
