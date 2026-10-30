"""Rule-based resume bullet suggestions; does not invent achievements."""
import re

WEAK_PHRASES = ["worked on", "responsible for", "helped with", "was involved in",
                "did a project on", "participated in"]

def improve_bullet(bullet: str) -> dict:
    original = bullet.strip().lstrip("•-* ").strip()
    if not original:
        return {"original": bullet, "suggestion": "", "reason": "Empty bullet point."}
    suggestion, reason = original, "Add tools, your specific contribution, and a verified result where appropriate."
    for phrase in sorted(WEAK_PHRASES, key=len, reverse=True):
        pattern = re.compile(r"\\b" + re.escape(phrase) + r"\\b", re.I)
        if pattern.search(suggestion):
            suggestion = pattern.sub("Developed", suggestion, count=1)
            reason = "Replaced vague wording with an action verb. Confirm that it accurately describes your contribution."
            break
    if suggestion[0].islower():
        suggestion = suggestion[0].upper() + suggestion[1:]
    if not suggestion.endswith((".", "!", "?")):
        suggestion += "."
    return {
        "original": original, "suggestion": suggestion, "reason": reason,
        "warning": "Review for accuracy. Never add unverified metrics, skills, or responsibilities.",
    }

def improve_resume_bullets(text: str) -> list[dict]:
    results = []
    for line in text.splitlines():
        if line.strip().startswith(("•", "-", "*", "▪", "●")):
            results.append(improve_bullet(line.strip()))
    return results
