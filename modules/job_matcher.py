"""TF-IDF text similarity and explicit skill-coverage matching."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.skill_extractor import find_skill_gaps

def calculate_similarity(resume_text: str, job_description: str) -> float:
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([resume_text, job_description])
    except ValueError:
        return 0.0
    return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100), 2)

def analyze_match(resume_text: str, job_description: str) -> dict:
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")
    if not job_description.strip():
        raise ValueError("Job description is empty.")
    similarity = calculate_similarity(resume_text, job_description)
    gaps = find_skill_gaps(resume_text, job_description)
    skills = gaps["job_skills"]
    coverage = round(100 * len(gaps["required_skills_found"]) / len(skills), 2) if skills else 0.0
    overall = round((similarity + coverage) / 2, 2) if skills else similarity
    return {
        "overall_match_score": overall,
        "tfidf_text_similarity": similarity,
        "skill_coverage": coverage,
        "resume_skills": gaps["resume_skills"],
        "job_skills": skills,
        "matched_skills": gaps["required_skills_found"],
        "missing_skills": gaps["missing_skills"],
        "note": "Heuristic estimate only; not an official ATS score or hiring prediction.",
    }
