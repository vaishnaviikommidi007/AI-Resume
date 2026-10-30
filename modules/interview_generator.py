"""Generate starter interview questions from detected skills."""
from modules.skill_extractor import extract_skills

QUESTION_TEMPLATES = {
    "python": ["How did you use Python in a project?", "How do you debug Python code and handle exceptions?"],
    "machine learning": ["How did you select and evaluate a model?", "How would you detect and reduce overfitting?"],
    "sql": ["Describe a query using joins or aggregation.", "How would you investigate a slow SQL query?"],
    "react": ["How did you manage component state?", "How do props differ from state in React?"],
    "docker": ["Why would you containerize this application?", "What is the purpose of a Dockerfile?"],
    "aws": ["Which AWS services could host this project, and why?", "How would you secure cloud resources?"],
    "nlp": ["How would you evaluate an NLP system?", "What are the limitations of keyword-based text analysis?"],
}

def generate_questions(resume_text: str, job_description: str = "", limit: int = 10) -> list[dict]:
    skills = extract_skills(f"{resume_text}\\n{job_description}")
    questions = []
    for skill in skills:
        templates = QUESTION_TEMPLATES.get(skill, [
            f"Describe a project or task where you used {skill}.",
            f"What challenges can arise when using {skill}, and how would you address them?",
        ])
        questions.extend({"skill": skill, "question": q} for q in templates)
    questions.append({"skill": "projects", "question":
        "Choose one project and explain its problem, your contribution, technical decisions, testing, and limitations."})
    unique, seen = [], set()
    for item in questions:
        if item["question"] not in seen:
            seen.add(item["question"])
            unique.append(item)
    return unique[:max(1, limit)]
