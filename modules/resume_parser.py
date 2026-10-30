"""Extract readable text from uploaded PDF resumes."""
from pathlib import Path
import pymupdf

class ResumeParsingError(ValueError):
    """Raised when a resume cannot be parsed or has no readable text."""

def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.replace("\\x00", " ").splitlines()]
    return "\\n".join(line for line in lines if line)

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    if not pdf_bytes:
        raise ResumeParsingError("The uploaded file is empty.")
    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
            text = "\\n".join(page.get_text("text") for page in document).strip()
    except Exception as exc:
        raise ResumeParsingError("Could not read this PDF. Please upload a valid PDF.") from exc
    if not text:
        raise ResumeParsingError("No selectable text found. This may be a scanned PDF; OCR is not included yet.")
    return clean_text(text)

def extract_text_from_path(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return extract_text_from_pdf_bytes(file_path.read_bytes())

def get_resume_sections(text: str) -> dict[str, str]:
    headings = {
        "summary": {"summary", "professional summary", "profile", "objective", "career objective"},
        "education": {"education", "academic background", "qualifications"},
        "skills": {"skills", "technical skills", "core skills", "technical expertise"},
        "experience": {"experience", "work experience", "employment", "internship", "internships"},
        "projects": {"projects", "academic projects", "personal projects"},
        "certifications": {"certifications", "certificates", "courses"},
        "achievements": {"achievements", "awards", "accomplishments"},
    }
    lookup = {heading: name for name, values in headings.items() for heading in values}
    sections, current = {"other": []}, "other"
    for line in text.splitlines():
        key = lookup.get(line.strip().rstrip(":").lower())
        if key:
            current = key
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return {key: "\\n".join(value).strip() for key, value in sections.items() if "\\n".join(value).strip()}
