import re
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# TECHNICAL SKILLS DATABASE
# ==========================================

SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "express.js",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "data analysis",
    "data visualization",
    "power bi",
    "tableau",
    "mongodb",
    "mysql",
    "postgresql",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "fastapi",
    "flask",
    "django",
    "rest api",
    "data structures",
    "algorithms",
    "problem solving",
    "communication",
    "teamwork",
    "leadership",
    "excel",
    "statistics",
    "linear regression",
    "logistic regression",
    "random forest",
    "xgboost",
    "nlp",
    "transformers",
    "generative ai",
    "large language models",
    "rag",
    "prompt engineering",
    "linux",
    "networking",
    "c",
]


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_resume_text(uploaded_file):

    pdf_bytes = uploaded_file.getvalue()

    with fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        pages = []

        for page in document:
            pages.append(page.get_text("text"))

    return "\n".join(pages)


# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# EXTRACT SKILLS
# ==========================================

def extract_skills(text):

    text = clean_text(text)

    detected_skills = []

    for skill in SKILLS:

        # Avoid matching short skills inside unrelated words.
        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            detected_skills.append(skill)

    return sorted(set(detected_skills))


# ==========================================
# CALCULATE TEXT SIMILARITY
# ==========================================

def calculate_similarity(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(score) * 100, 2)


# ==========================================
# ANALYZE SKILLS
# ==========================================

def analyze_skills(resume_text, job_description):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matching_skills = sorted(
        resume_skills & job_skills
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    additional_skills = sorted(
        resume_skills - job_skills
    )

    if job_skills:

        skill_coverage = round(
            len(matching_skills) / len(job_skills) * 100,
            2
        )

    else:

        skill_coverage = 0.0

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "skill_coverage": skill_coverage,
    }


# ==========================================
# GENERATE IMPROVEMENT SUGGESTIONS
# ==========================================

def generate_suggestions(
    resume_text,
    job_description,
    similarity_score,
    skill_analysis
):

    suggestions = []

    resume_text = clean_text(resume_text)

    matching_skills = skill_analysis["matching_skills"]

    missing_skills = skill_analysis["missing_skills"]

    if similarity_score < 30:

        suggestions.append(
            "The resume has relatively low textual similarity "
            "to this job description. Review the role requirements "
            "and describe relevant experience more clearly."
        )

    elif similarity_score < 60:

        suggestions.append(
            "Review the job description and make sure relevant "
            "projects, skills, and experience are clearly described."
        )

    else:

        suggestions.append(
            "The resume has relatively strong textual similarity "
            "to this job description. Review the individual "
            "requirements to ensure they are accurately represented."
        )

    if missing_skills:

        suggestions.append(
            "Review these job-description skills that were not "
            "detected in the resume: "
            + ", ".join(missing_skills)
            + ". Add them only if you genuinely possess them."
        )

    if not matching_skills:

        suggestions.append(
            "No overlapping skills were detected using the current "
            "skill dictionary. Check whether the job description "
            "and resume use different terminology."
        )

    if len(resume_text.split()) < 100:

        suggestions.append(
            "The extracted resume text is relatively short. "
            "Check whether all PDF pages and relevant content "
            "were extracted correctly."
        )

    if not re.search(
        r"\b(project|projects|developed|implemented|built)\b",
        resume_text
    ):

        suggestions.append(
            "If applicable, describe relevant projects and explain "
            "your individual contributions and technologies used."
        )

    suggestions.append(
        "Where possible, describe measurable outcomes in your "
        "projects, such as model performance, test coverage, "
        "processing time, or the number of records evaluated."
    )

    return suggestions


# ==========================================
# MAIN ANALYSIS FUNCTION
# ==========================================

def analyze_resume(resume_text, job_description):

    if not resume_text.strip():

        raise ValueError(
            "The resume contains no extractable text."
        )

    if not job_description.strip():

        raise ValueError(
            "Please provide a job description."
        )

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )

    skill_analysis = analyze_skills(
        resume_text,
        job_description
    )

    suggestions = generate_suggestions(
        resume_text,
        job_description,
        similarity_score,
        skill_analysis
    )

    return {
        "similarity_score": similarity_score,
        "skill_analysis": skill_analysis,
        "suggestions": suggestions,
    }
