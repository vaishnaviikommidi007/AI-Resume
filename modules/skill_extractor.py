"""Dictionary-based technical skill extraction."""
import re

DEFAULT_SKILLS = {
    "python": ["python"], "java": ["java"], "c++": ["c++", "cpp"],
    "javascript": ["javascript", "js"], "typescript": ["typescript"],
    "react": ["react", "react.js"], "node.js": ["node.js", "nodejs"],
    "html": ["html", "html5"], "css": ["css", "css3"], "sql": ["sql"],
    "mysql": ["mysql"], "mongodb": ["mongodb", "mongo db"], "git": ["git"],
    "github": ["github"], "docker": ["docker"], "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"], "azure": ["azure", "microsoft azure"],
    "machine learning": ["machine learning", "ml"], "deep learning": ["deep learning"],
    "nlp": ["natural language processing", "nlp"], "computer vision": ["computer vision"],
    "tensorflow": ["tensorflow"], "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"], "pandas": ["pandas"],
    "numpy": ["numpy"], "data analysis": ["data analysis", "data analytics"],
    "power bi": ["power bi", "powerbi"], "tableau": ["tableau"],
    "rest api": ["rest api", "restful api", "rest apis"], "fastapi": ["fastapi"],
    "flask": ["flask"], "streamlit": ["streamlit"], "agile": ["agile"],
    "linux": ["linux"], "data structures": ["data structures", "dsa"],
    "algorithms": ["algorithms"],
}

def _contains_term(text: str, term: str) -> bool:
    term = term.strip()
    if not term:
        return False
    return re.search(r"(?<!\\w)" + re.escape(term) + r"(?!\\w)", text, flags=re.I) is not None

def extract_skills(text: str, skill_dictionary: dict | None = None) -> list[str]:
    dictionary = skill_dictionary or DEFAULT_SKILLS
    found = []
    for canonical, aliases in dictionary.items():
        if any(_contains_term(text, term) for term in [canonical, *aliases]):
            found.append(canonical)
    return sorted(set(found))

def find_skill_gaps(resume_text: str, job_description: str, skill_dictionary: dict | None = None) -> dict:
    resume = set(extract_skills(resume_text, skill_dictionary))
    job = set(extract_skills(job_description, skill_dictionary))
    return {
        "resume_skills": sorted(resume),
        "required_skills_found": sorted(resume & job),
        "missing_skills": sorted(job - resume),
        "job_skills": sorted(job),
    }
