import pandas as pd
import streamlit as st

# Extended feature modules are imported below the original dashboard section.

from analyzer import (
    extract_resume_text,
    analyze_resume,
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(
            120deg,
            #173b75,
            #3674c5
        );
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white;
        margin-bottom: 0.4rem;
    }

    .hero p {
        color: #e9f1ff;
        font-size: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="hero">
        <h1>📄 AI Resume Analyzer</h1>
        <p>
            Analyze resume-job similarity, identify skill gaps,
            and discover opportunities to improve your resume.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("About the Project")

    st.write(
        """
        This application uses Natural Language Processing
        to compare a resume with a job description.
        """
    )

    st.subheader("Technologies")

    st.write(
        """
        - Python
        - Streamlit
        - Scikit-learn
        - TF-IDF
        - Cosine Similarity
        - PyMuPDF
        - Pandas
        """
    )

    st.divider()

    st.caption(
        "The similarity score is not a validated ATS score "
        "or a prediction of hiring success."
    )


# ==========================================
# INPUT SECTION
# ==========================================

st.header("1. Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
    help="Upload a text-based PDF resume.",
)


st.header("2. Enter Job Details")

job_role = st.text_input(
    "Target job role",
    placeholder="Example: Machine Learning Engineer",
)

job_description = st.text_area(
    "Job description",
    height=220,
    placeholder=(
        "Paste the job description here, including "
        "required skills, qualifications, and responsibilities."
    ),
)


# ==========================================
# ANALYZE BUTTON
# ==========================================

analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True,
)


if analyze_button:

    if uploaded_file is None:

        st.error(
            "Please upload your resume PDF first."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        try:

            with st.spinner(
                "Extracting resume text and analyzing..."
            ):

                resume_text = extract_resume_text(
                    uploaded_file
                )

                if not resume_text.strip():

                    st.error(
                        "No readable text was found in this PDF. "
                        "Try a text-based PDF rather than a scanned image."
                    )

                    st.stop()

                results = analyze_resume(
                    resume_text,
                    job_description,
                )

                st.session_state["analysis_results"] = results

                st.session_state["resume_filename"] = (
                    uploaded_file.name
                )

                st.session_state["job_role"] = job_role

                st.session_state["resume_text"] = resume_text

                st.session_state["job_description"] = (
                    job_description
                )

        except Exception as error:

            st.error(
                "The resume could not be analyzed. "
                "Please check the PDF and try again."
            )

            st.exception(error)


# ==========================================
# DISPLAY RESULTS
# ==========================================

if "analysis_results" in st.session_state:

    results = st.session_state["analysis_results"]

    skill_analysis = results["skill_analysis"]

    similarity_score = results["similarity_score"]

    st.divider()

    st.header("3. Analysis Results")

    st.write(
        f"**Resume:** "
        f"{st.session_state['resume_filename']}"
    )

    st.write(
        f"**Target role:** "
        f"{st.session_state['job_role'] or 'Not specified'}"
    )

    st.caption(
        "The score measures textual similarity using TF-IDF "
        "and cosine similarity. It is not a hiring probability."
    )

    # --------------------------------------
    # METRICS
    # --------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Text Similarity",
            f"{similarity_score:.2f}%",
        )

    with col2:

        st.metric(
            "Matching Skills",
            len(skill_analysis["matching_skills"]),
        )

    with col3:

        st.metric(
            "Skills to Review",
            len(skill_analysis["missing_skills"]),
        )

    with col4:

        st.metric(
            "Skill Coverage",
            f"{skill_analysis['skill_coverage']:.2f}%",
        )

    st.progress(
        min(max(similarity_score / 100, 0.0), 1.0)
    )

    # --------------------------------------
    # SKILL MATCHING
    # --------------------------------------

    st.subheader("✅ Matching Skills")

    matching_skills = skill_analysis["matching_skills"]

    if matching_skills:

        st.success(
            ", ".join(matching_skills)
        )

    else:

        st.info(
            "No matching skills were detected. "
            "Check the terminology in the resume and job description."
        )

    # --------------------------------------
    # MISSING SKILLS
    # --------------------------------------

    st.subheader("⚠️ Skills to Review")

    missing_skills = skill_analysis["missing_skills"]

    if missing_skills:

        st.warning(
            ", ".join(missing_skills)
        )

        st.caption(
            "These skills were detected in the job description "
            "but not in the resume. This does not prove that "
            "you lack these skills."
        )

    else:

        st.success(
            "No skill gaps were detected using the current dictionary."
        )

    # --------------------------------------
    # ADDITIONAL SKILLS
    # --------------------------------------

    with st.expander("View additional skills in your resume"):

        additional_skills = skill_analysis["additional_skills"]

        if additional_skills:

            st.write(
                ", ".join(additional_skills)
            )

        else:

            st.write(
                "No additional skills were detected."
            )

    # --------------------------------------
    # SKILL COMPARISON TABLE
    # --------------------------------------

    st.subheader("📊 Detailed Skill Comparison")

    all_skills = sorted(
        set(skill_analysis["resume_skills"])
        | set(skill_analysis["job_skills"])
    )

    rows = []

    for skill in all_skills:

        in_resume = (
            skill in skill_analysis["resume_skills"]
        )

        in_job = (
            skill in skill_analysis["job_skills"]
        )

        if in_resume and in_job:

            status = "Matched"

        elif in_job and not in_resume:

            status = "Review"

        else:

            status = "Additional"

        rows.append(
            {
                "Skill": skill,
                "Found in Resume": (
                    "Yes" if in_resume else "No"
                ),
                "Found in Job Description": (
                    "Yes" if in_job else "No"
                ),
                "Status": status,
            }
        )

    if rows:

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Skill Analysis CSV",
            data=csv_data,
            file_name="skill_analysis.csv",
            mime="text/csv",
        )

    # --------------------------------------
    # IMPROVEMENT SUGGESTIONS
    # --------------------------------------

    st.subheader("💡 Resume Improvement Suggestions")

    for index, suggestion in enumerate(
        results["suggestions"],
        start=1,
    ):

        st.write(
            f"**{index}.** {suggestion}"
        )

    # --------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------

    st.subheader("📥 Download Report")

    report_lines = [
        "AI RESUME ANALYZER REPORT",
        "=" * 35,
        f"Resume: {st.session_state['resume_filename']}",
        f"Target Role: {st.session_state['job_role'] or 'Not specified'}",
        f"Text Similarity: {similarity_score:.2f}%",
        (
            "Skill Coverage: "
            f"{skill_analysis['skill_coverage']:.2f}%"
        ),
        "",
        "MATCHING SKILLS",
        ", ".join(matching_skills) or "None detected",
        "",
        "SKILLS TO REVIEW",
        ", ".join(missing_skills) or "None detected",
        "",
        "ADDITIONAL SKILLS",
        (
            ", ".join(skill_analysis["additional_skills"])
            or "None detected"
        ),
        "",
        "IMPROVEMENT SUGGESTIONS",
    ]

    for index, suggestion in enumerate(
        results["suggestions"],
        start=1,
    ):

        report_lines.append(
            f"{index}. {suggestion}"
        )

    report_lines.extend(
        [
            "",
            "LIMITATIONS",
            (
                "The similarity score measures textual similarity. "
                "It is not a validated ATS score or hiring probability."
            ),
            (
                "Skill extraction relies on a predefined keyword "
                "dictionary and may miss relevant skills."
            ),
        ]
    )

    report = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Full Analysis Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Resume Analyzer | Built with Python, NLP, "
    "Scikit-learn, PyMuPDF, and Streamlit"
)


# =============================================================================
# EXTENDED FEATURES — INTEGRATION OF THE 8 MODULES
# The original dashboard above is intentionally preserved. This section adds
# additional analysis tabs using the modules/ package.
# =============================================================================

from modules.job_matcher import analyze_match as analyze_with_modules
from modules.ats_checker import check_resume
from modules.skill_gap_analyzer import analyze_skill_gaps
from modules.resume_improver import improve_bullet, improve_resume_bullets
from modules.interview_generator import generate_questions
from modules.report_generator import analysis_to_text, analysis_to_csv


if "analysis_results" in st.session_state:
    _resume_text = st.session_state.get("resume_text", "")
    _job_description = st.session_state.get("job_description", "")
    _resume_filename = st.session_state.get("resume_filename", "resume.pdf")
    _job_role = st.session_state.get("job_role", "")

    if _resume_text.strip() and _job_description.strip():
        try:
            # These results are separate from the original analyzer output so
            # the original dashboard scores and behavior remain unchanged.
            _module_match = analyze_with_modules(_resume_text, _job_description)
            _ats_result = check_resume(_resume_text, _resume_filename)
            # Correct the email check if a platform or copied module regex differs.
            import re as _re
            _email_found = bool(_re.search(
                r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                _resume_text,
                _re.I,
            ))
            for _check in _ats_result.get("checks", []):
                if _check.get("name") == "Email address":
                    _check["passed"] = _email_found
                    _check["details"] = (
                        "Email detected." if _email_found else "No email detected."
                    )
            _ats_result["score"] = round(
                100 * sum(bool(item.get("passed")) for item in _ats_result.get("checks", []))
                / max(1, len(_ats_result.get("checks", [])))
            )
            _gap_result = analyze_skill_gaps(_resume_text, _job_description)
            _interview_questions = generate_questions(
                _resume_text, _job_description, limit=15
            )
        except Exception as _module_error:
            st.warning(
                "The original analysis above is available, but one or more extended "
                "modules could not run. Check that all eight files are inside the "
                f"`modules` folder. Details: {_module_error}"
            )
        else:
            st.divider()
            st.header("🚀 Extended Resume Intelligence")
            st.caption(
                "These are additional rule-based estimates from the eight modules. "
                "Review the suggestions yourself; they are not official ATS results."
            )

            _tab_overview, _tab_ats, _tab_gaps, _tab_improve, _tab_interview, _tab_reports = st.tabs([
                "✨ Extended Overview",
                "✅ ATS Checklist",
                "🧭 Skill Gap Roadmap",
                "📝 Resume Improver",
                "🎤 Interview Prep",
                "📥 Reports",
            ])

            with _tab_overview:
                _m1, _m2, _m3 = st.columns(3)
                _m1.metric("Estimated Overall Match", f"{_module_match['overall_match_score']:.2f}%")
                _m2.metric("TF-IDF Text Similarity", f"{_module_match['tfidf_text_similarity']:.2f}%")
                _m3.metric("Skill Coverage", f"{_module_match['skill_coverage']:.2f}%")
                st.progress(min(max(_module_match["overall_match_score"] / 100, 0), 1))
                st.info(_module_match["note"])
                _a, _b = st.columns(2)
                with _a:
                    st.markdown("#### Skills matched")
                    if _module_match["matched_skills"]:
                        st.success(", ".join(_module_match["matched_skills"]))
                    else:
                        st.write("No matching skills detected by the module dictionary.")
                with _b:
                    st.markdown("#### Skills to review")
                    if _module_match["missing_skills"]:
                        st.warning(", ".join(_module_match["missing_skills"]))
                    else:
                        st.success("No skill gaps detected by the module dictionary.")
                st.caption(
                    "This module-based estimate is separate from the original score above "
                    "because the matching methods may differ."
                )

            with _tab_ats:
                st.subheader("Resume Readiness Checklist")
                st.metric("Checklist score", f"{_ats_result['score']}%")
                for _item in _ats_result.get("checks", []):
                    if _item.get("passed"):
                        st.success(f"✓ **{_item['name']}** — {_item['details']}")
                    else:
                        st.warning(f"△ **{_item['name']}** — {_item['details']}")
                st.markdown("#### Notes")
                for _warning in _ats_result.get("warnings", []):
                    st.caption(f"• {_warning}")

            with _tab_gaps:
                st.subheader("Personalized Skill Gap Roadmap")
                _roadmap = _gap_result.get("roadmap", [])
                if _roadmap:
                    _roadmap_df = pd.DataFrame(_roadmap)
                    st.dataframe(_roadmap_df, use_container_width=True, hide_index=True)
                    st.markdown("#### Suggested next steps")
                    for _item in _roadmap:
                        with st.expander(f"{_item['skill'].title()} — {_item['priority']} priority"):
                            st.write(_item["suggestion"])
                else:
                    st.success("No missing skills were detected from the module's current skill dictionary.")
                st.caption(_gap_result.get("note", "Skill-gap results are dictionary-based."))

            with _tab_improve:
                st.subheader("Improve Resume Bullet Points")
                st.write(
                    "Paste one bullet at a time. The tool can suggest clearer wording, "
                    "but it will not know whether the claim is true—verify every edit."
                )
                _bullet_text = st.text_area(
                    "Resume bullet to improve",
                    placeholder="Example: Worked on a Python project for data analysis",
                    key="extended_bullet_input",
                    height=110,
                )
                if st.button("✨ Suggest Improved Bullet", key="extended_improve_button"):
                    _improved = improve_bullet(_bullet_text)
                    if _improved.get("suggestion"):
                        st.markdown("**Original**")
                        st.write(_improved["original"])
                        st.markdown("**Suggested version**")
                        st.success(_improved["suggestion"])
                        st.caption(_improved.get("reason", "Review the wording."))
                        st.warning(_improved.get("warning", "Verify all details before using."))
                    else:
                        st.info("Enter a bullet point first.")
                with st.expander("Try to detect existing bullet points in your resume"):
                    _existing_bullets = improve_resume_bullets(_resume_text)
                    if _existing_bullets:
                        for _idx, _bullet in enumerate(_existing_bullets, start=1):
                            st.markdown(f"**{_idx}. Original:** {_bullet['original']}")
                            st.markdown(f"**Suggestion:** {_bullet['suggestion']}")
                            st.caption(_bullet.get("reason", ""))
                    else:
                        st.info(
                            "No bullet points using common bullet symbols were detected. "
                            "You can paste a bullet into the box above."
                        )

            with _tab_interview:
                st.subheader("Practice Questions Based on Your Resume")
                st.write(
                    "Use these as practice prompts. They are generated from detected skills "
                    "and are not a guarantee of what an interviewer will ask."
                )
                for _idx, _question in enumerate(_interview_questions, start=1):
                    with st.expander(f"{_idx}. {_question['question']}"):
                        st.caption(f"Topic: {_question['skill'].title()}")
                        st.text_area(
                            "Your practice answer",
                            key=f"extended_interview_answer_{_idx}",
                            height=90,
                            placeholder="Write your answer here...",
                        )

            with _tab_reports:
                st.subheader("Download Extended Analysis")
                _report_text = analysis_to_text(_module_match, _ats_result, _gap_result)
                # Normalize newline escapes if a copied module contains literal backslashes.
                _report_text = _report_text.replace("\\n", "\n")
                st.download_button(
                    "⬇️ Download extended TXT report",
                    data=_report_text,
                    file_name="extended_resume_analysis.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                _report_csv = analysis_to_csv(_module_match)
                st.download_button(
                    "⬇️ Download module skill comparison CSV",
                    data=_report_csv,
                    file_name="extended_skill_analysis.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
    # =====================================================
    # FEATURE 1: ATS CHECKLIST
    # =====================================================

    import re

    st.divider()
    st.header("4. ATS Compatibility Checklist")

    resume_text = st.session_state.get("resume_text", "")

    ats_checks = {
        "Email address": bool(
            re.search(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                resume_text
            )
        ),

        "Phone number": bool(
            re.search(
                r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)",
                resume_text
            )
        ),

        "Education section": bool(
            re.search(
                r"\b(education|academic background|qualifications)\b",
                resume_text,
                re.IGNORECASE
            )
        ),

        "Projects section": bool(
            re.search(
                r"\b(projects|personal projects|academic projects)\b",
                resume_text,
                re.IGNORECASE
            )
        ),

        "Experience section": bool(
            re.search(
                r"\b(experience|internship|employment|work history)\b",
                resume_text,
                re.IGNORECASE
            )
        ),

        "Skills section": bool(
            re.search(
                r"\b(technical skills|skills|technologies)\b",
                resume_text,
                re.IGNORECASE
            )
        ),

        "Certifications section": bool(
            re.search(
                r"\b(certifications|certificates|courses)\b",
                resume_text,
                re.IGNORECASE
            )
        ),

        "Resume content available": len(resume_text.strip()) > 200
    }

    passed_checks = sum(ats_checks.values())
    total_checks = len(ats_checks)
    ats_score = (passed_checks / total_checks) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Checklist Score",
            f"{ats_score:.1f}%"
        )

    with col2:
        st.metric(
            "Checks Passed",
            f"{passed_checks}/{total_checks}"
        )

    st.progress(ats_score / 100)

    for check_name, passed in ats_checks.items():

        if passed:
            st.success(f"✅ {check_name}")
        else:
            st.warning(f"⚠️ {check_name} not detected")

    st.caption(
        "This checklist checks for basic resume elements. "
        "A missing element may be present in a format the "
        "application does not recognize. This is not an actual "
        "ATS vendor score."
        )
    # =====================================================
# FEATURE 2: INTERVIEW QUESTION GENERATOR
# =====================================================

st.divider()
st.header("5. AI/ML Interview Question Generator")

target_role = st.session_state.get(
    "job_role",
    "Software Engineer"
)

job_description = st.session_state.get(
    "job_description",
    ""
)

skill_analysis = st.session_state["analysis_results"]["skill_analysis"]

matching_skills = skill_analysis.get(
    "matching_skills",
    []
)

missing_skills = skill_analysis.get(
    "missing_skills",
    []
)

# Questions for common technical topics
question_bank = {
    "python": [
        "What are lists, tuples, sets, and dictionaries in Python?",
        "Explain the difference between shallow copy and deep copy.",
        "How do exceptions work in Python?"
    ],

    "machine learning": [
        "Explain supervised and unsupervised learning.",
        "What is overfitting, and how can you prevent it?",
        "Explain the bias-variance trade-off."
    ],

    "deep learning": [
        "What is an artificial neural network?",
        "What is the purpose of an activation function?",
        "Explain backpropagation."
    ],

    "sql": [
        "Explain the difference between WHERE and HAVING.",
        "What are primary keys and foreign keys?",
        "Explain the different types of SQL joins."
    ],

    "pandas": [
        "What is a DataFrame in Pandas?",
        "How do you handle missing values in a dataset?",
        "What is the difference between loc and iloc?"
    ],

    "scikit-learn": [
        "What is the purpose of train_test_split?",
        "Explain the difference between fit and predict.",
        "How do you evaluate a classification model?"
    ],

    "tensorflow": [
        "What is TensorFlow used for?",
        "What is the role of an optimizer in neural networks?",
        "How do you train a neural network?"
    ],

    "pytorch": [
        "What are tensors in PyTorch?",
        "What is automatic differentiation?",
        "Explain the purpose of the DataLoader."
    ],

    "nlp": [
        "What is tokenization?",
        "Explain stemming and lemmatization.",
        "What is the difference between TF-IDF and word embeddings?"
    ],

    "java": [
        "Explain the four pillars of object-oriented programming.",
        "What is the difference between an interface and an abstract class?",
        "How does exception handling work in Java?"
    ],

    "c++": [
        "Explain pointers and references in C++.",
        "What is the difference between a stack and a heap?",
        "Explain inheritance and polymorphism."
    ],

    "react": [
        "What are React components?",
        "Explain the difference between props and state.",
        "What are React Hooks?"
    ],

    "node.js": [
        "What is Node.js?",
        "Explain the event loop in Node.js.",
        "How do you handle asynchronous operations?"
    ],

    "git": [
        "What is the difference between git merge and git rebase?",
        "How do you resolve a merge conflict?",
        "What is the purpose of a Git branch?"
    ],

    "mongodb": [
        "What is the difference between SQL and MongoDB?",
        "What are documents and collections?",
        "How do you query documents in MongoDB?"
    ],

    "mysql": [
        "What is database normalization?",
        "Explain joins in MySQL.",
        "What is an index, and why is it useful?"
    ],

    "rest api": [
        "What is a REST API?",
        "Explain the difference between GET, POST, PUT, and DELETE.",
        "What are HTTP status codes?"
    ],

    "aws": [
        "What is cloud computing?",
        "What are EC2 and S3 used for?",
        "What is the difference between scalability and elasticity?"
    ]
}

def generate_interview_questions(
    role,
    description,
    resume_skills,
    review_skills
):
    questions = []

    # Role-based questions
    questions.extend([
        f"Explain your understanding of the {role} role.",
        "Describe a project you completed and the problem it solves.",
        "What was the most challenging technical problem you faced?",
        "How do you test and debug your code?",
        "How would you improve the performance of an application?"
    ])

    # Questions based on skills found in the resume
    normalized_resume = [
        skill.lower() for skill in resume_skills
    ]

    normalized_description = description.lower()

    for skill, skill_questions in question_bank.items():

        if (
            skill in normalized_resume
            or skill in normalized_description
        ):
            questions.extend(skill_questions)

    # Questions about requirements not detected in the resume
    for skill in review_skills[:5]:
        questions.append(
            f"Explain {skill} and describe how it can be used "
            f"in a {role} project."
        )

    # Remove duplicate questions
    unique_questions = list(dict.fromkeys(questions))

    return unique_questions


if st.button(
    "🎯 Generate Interview Questions",
    key="generate_interview_questions"
):

    questions = generate_interview_questions(
        target_role,
        job_description,
        matching_skills,
        missing_skills
    )

    st.session_state["generated_questions"] = questions


if "generated_questions" in st.session_state:

    questions = st.session_state["generated_questions"]

    st.subheader("Your Personalized Interview Questions")

    for index, question in enumerate(questions, start=1):

        st.write(f"**Q{index}.** {question}")

    questions_text = "\n".join(
        f"{index}. {question}"
        for index, question in enumerate(questions, start=1)
    )

    st.download_button(
        "⬇️ Download Interview Questions",
        data=questions_text,
        file_name="interview_questions.txt",
        mime="text/plain",
        key="download_interview_questions"
    )

    st.caption(
        "Questions are generated from predefined templates "
        "and detected job-description keywords. They are "
        "not generated by a large language model."
    )
    # =====================================================
# FEATURE 3: BEFORE-AND-AFTER RESUME COMPARISON
# =====================================================

st.divider()
st.header("6. Before-and-After Resume Comparison")

st.write(
    "Upload an improved version of your resume to compare "
    "its similarity and skill coverage against the original."
)

improved_resume_file = st.file_uploader(
    "Upload your improved resume PDF",
    type=["pdf"],
    key="improved_resume_upload"
)

if st.button(
    "📊 Compare Resume Versions",
    key="compare_resume_versions"
):

    if improved_resume_file is None:

        st.warning(
            "Please upload the improved resume PDF first."
        )

    else:

        try:

            with st.spinner(
                "Analyzing the improved resume..."
            ):

                original_resume_text = st.session_state[
                    "resume_text"
                ]

                current_job_description = st.session_state[
                    "job_description"
                ]

                improved_resume_text = extract_resume_text(
                    improved_resume_file
                )

                if not improved_resume_text.strip():

                    st.error(
                        "No readable text was found in the "
                        "improved resume PDF."
                    )

                else:

                    # Analyze original resume
                    original_results = analyze_resume(
                        original_resume_text,
                        current_job_description
                    )

                    # Analyze improved resume
                    improved_results = analyze_resume(
                        improved_resume_text,
                        current_job_description
                    )

                    original_skills = original_results[
                        "skill_analysis"
                    ]

                    improved_skills = improved_results[
                        "skill_analysis"
                    ]

                    original_similarity = original_results[
                        "similarity_score"
                    ]

                    improved_similarity = improved_results[
                        "similarity_score"
                    ]

                    original_coverage = original_skills[
                        "skill_coverage"
                    ]

                    improved_coverage = improved_skills[
                        "skill_coverage"
                    ]

                    original_matching = len(
                        original_skills["matching_skills"]
                    )

                    improved_matching = len(
                        improved_skills["matching_skills"]
                    )

                    st.subheader("Comparison Results")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(
                            "### Original Resume"
                        )

                        st.metric(
                            "Text Similarity",
                            f"{original_similarity:.2f}%"
                        )

                        st.metric(
                            "Skill Coverage",
                            f"{original_coverage:.2f}%"
                        )

                        st.metric(
                            "Matching Skills",
                            original_matching
                        )

                    with col2:

                        st.markdown(
                            "### Improved Resume"
                        )

                        st.metric(
                            "Text Similarity",
                            f"{improved_similarity:.2f}%",
                            delta=(
                                f"{improved_similarity - original_similarity:.2f} "
                                "percentage points"
                            )
                        )

                        st.metric(
                            "Skill Coverage",
                            f"{improved_coverage:.2f}%",
                            delta=(
                                f"{improved_coverage - original_coverage:.2f} "
                                "percentage points"
                            )
                        )

                        st.metric(
                            "Matching Skills",
                            improved_matching,
                            delta=(
                                improved_matching - original_matching
                            )
                        )

                    comparison_data = pd.DataFrame({
                        "Metric": [
                            "Text Similarity (%)",
                            "Skill Coverage (%)",
                            "Matching Skills"
                        ],

                        "Original Resume": [
                            original_similarity,
                            original_coverage,
                            original_matching
                        ],

                        "Improved Resume": [
                            improved_similarity,
                            improved_coverage,
                            improved_matching
                        ]
                    })

                    st.subheader("Detailed Comparison")

                    st.dataframe(
                        comparison_data,
                        use_container_width=True,
                        hide_index=True
                    )

                    csv_data = comparison_data.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        "⬇️ Download Comparison CSV",
                        data=csv_data,
                        file_name="resume_comparison.csv",
                        mime="text/csv",
                        key="download_resume_comparison"
                    )

                    if (
                        improved_similarity > original_similarity
                        and improved_coverage >= original_coverage
                    ):

                        st.success(
                            "The revised resume has a higher text "
                            "similarity score, with skill coverage "
                            "maintained or improved."
                        )

                    elif (
                        improved_similarity > original_similarity
                        or improved_coverage > original_coverage
                    ):

                        st.info(
                            "Some metrics improved. Review all the "
                            "results before deciding whether the "
                            "revised resume is better."
                        )

                    else:

                        st.warning(
                            "The measured metrics did not improve. "
                            "Review the job requirements and the "
                            "changes made to the resume."
                        )

                    st.caption(
                        "Comparison results depend on the existing "
                        "analysis algorithm. Higher similarity does "
                        "not guarantee a better resume or a higher "
                        "chance of getting hired."
                    )

        except Exception as error:

            st.error(
                "Could not compare the resume versions."
            )

            st.exception(error)