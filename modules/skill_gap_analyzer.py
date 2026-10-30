"""Identify missing skills and suggest learning activities."""
from modules.skill_extractor import find_skill_gaps

SUGGESTIONS = {
    "docker": "Learn images, containers, Dockerfiles, and basic container networking.",
    "aws": "Learn IAM, S3, EC2, and deploy a small application.",
    "azure": "Explore cloud fundamentals and deploy a simple web application.",
    "kubernetes": "Learn Pods, Deployments, Services, and ConfigMaps.",
    "sql": "Practice joins, aggregation, subqueries, and window functions.",
    "machine learning": "Build a supervised-learning project and evaluate it with suitable metrics.",
    "deep learning": "Study neural-network fundamentals and train a small model.",
    "nlp": "Build a text-classification or information-extraction project.",
    "rest api": "Create and test a REST API with input validation and clear errors.",
    "python": "Practice functions, data structures, exceptions, modules, and testing.",
    "pandas": "Practice cleaning, joining, grouping, and summarizing datasets.",
    "scikit-learn": "Build a preprocessing and model-evaluation pipeline.",
}

def analyze_skill_gaps(resume_text: str, job_description: str) -> dict:
    data = find_skill_gaps(resume_text, job_description)
    roadmap = []
    for skill in data["missing_skills"]:
        roadmap.append({
            "skill": skill,
            "priority": "High" if skill in {"python", "sql", "machine learning", "docker", "aws"} else "Medium",
            "suggestion": SUGGESTIONS.get(skill, f"Learn the fundamentals of {skill} and complete a small practical exercise."),
        })
    return {**data, "roadmap": roadmap,
            "note": "Dictionary-based skill detection can miss synonyms and context; review the results."}
