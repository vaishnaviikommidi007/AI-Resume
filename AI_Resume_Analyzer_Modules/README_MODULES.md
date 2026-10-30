# AI Resume Analyzer modules

Copy the `modules` folder into the root of your project (next to `app.py`).

## Install
Activate your venv and run:
```powershell
python -m pip install -r requirements.txt
```

## Quick test
```powershell
python -c "from modules.job_matcher import analyze_match; print(analyze_match('Python SQL and machine learning projects', 'Python developer with SQL and machine learning'))"
```

## Minimal Streamlit integration
```python
import streamlit as st
from modules.resume_parser import extract_text_from_pdf_bytes, ResumeParsingError
from modules.job_matcher import analyze_match
from modules.skill_gap_analyzer import analyze_skill_gaps
from modules.ats_checker import check_resume
from modules.interview_generator import generate_questions
from modules.report_generator import analysis_to_text, analysis_to_csv
from modules.resume_improver import improve_resume_bullets

st.title("AI Resume Analyzer")
resume_file = st.file_uploader("Upload a text-based PDF resume", type=["pdf"])
job_description = st.text_area("Paste the job description")

if st.button("Analyze"):
    if not resume_file or not job_description.strip():
        st.error("Upload a resume and paste a job description.")
    else:
        try:
            resume_text = extract_text_from_pdf_bytes(resume_file.getvalue())
            match = analyze_match(resume_text, job_description)
            gaps = analyze_skill_gaps(resume_text, job_description)
            ats = check_resume(resume_text, resume_file.name)
            st.metric("Estimated match", f"{match['overall_match_score']}%")
            st.metric("Skill coverage", f"{match['skill_coverage']}%")
            st.write("Matched skills", match["matched_skills"])
            st.write("Missing skills", match["missing_skills"])
            st.subheader("Resume checklist")
            st.write(ats["checks"])
            st.subheader("Learning roadmap")
            st.write(gaps["roadmap"])
            st.subheader("Interview questions")
            st.write(generate_questions(resume_text, job_description))
            st.subheader("Bullet suggestions")
            st.write(improve_resume_bullets(resume_text))
            st.download_button("Download text report", analysis_to_text(match, ats, gaps), "resume_analysis.txt")
            st.download_button("Download skill CSV", analysis_to_csv(match), "skill_analysis.csv", "text/csv")
            st.caption(match["note"])
        except ResumeParsingError as exc:
            st.error(str(exc))
```

## Notes
- Scores are heuristics, not official ATS scores or hiring predictions.
- The skill dictionary is intentionally basic; expand `DEFAULT_SKILLS` for more skills and aliases.
- Scanned PDFs need OCR; this code reports when no selectable text is present.
- Rule-based resume suggestions must be reviewed for truthfulness.
