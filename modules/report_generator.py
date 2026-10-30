"""Export analysis results as text and CSV."""
import csv
import io
from datetime import datetime

def analysis_to_text(analysis: dict, ats_result: dict | None = None, gap_result: dict | None = None) -> str:
    lines = [
        "AI RESUME ANALYZER REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Overall estimated match: {analysis.get('overall_match_score', 'N/A')}%",
        f"TF-IDF text similarity: {analysis.get('tfidf_text_similarity', 'N/A')}%",
        f"Skill coverage: {analysis.get('skill_coverage', 'N/A')}%",
        "",
        "Matched skills: " + (", ".join(analysis.get("matched_skills", [])) or "None detected"),
        "Missing skills: " + (", ".join(analysis.get("missing_skills", [])) or "None detected"),
        "Resume skills: " + (", ".join(analysis.get("resume_skills", [])) or "None detected"),
        "", "Important note: " + analysis.get("note", "Review all results manually."),
    ]
    if ats_result:
        lines.extend(["", f"Resume checklist score: {ats_result.get('score', 'N/A')}%"])
        for item in ats_result.get("checks", []):
            status = "PASS" if item["passed"] else "REVIEW"
            lines.append(f"- {status}: {item['name']} — {item['details']}")
    if gap_result:
        lines.extend(["", "Suggested learning roadmap:"])
        for item in gap_result.get("roadmap", []):
            lines.append(f"- {item['skill']} ({item['priority']}): {item['suggestion']}")
    return "\\n".join(lines)

def analysis_to_csv(analysis: dict) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["skill", "status"])
    matched = set(analysis.get("matched_skills", []))
    missing = set(analysis.get("missing_skills", []))
    for skill in sorted(matched | missing):
        writer.writerow([skill, "Matched" if skill in matched else "Missing"])
    return output.getvalue().encode("utf-8-sig")
