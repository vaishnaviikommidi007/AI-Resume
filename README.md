# AI Resume Analyzer Using NLP

## Overview

AI Resume Analyzer is a Python-based web application that compares a candidate's resume with a job description using Natural Language Processing techniques.

The application extracts text from PDF resumes, calculates textual similarity, identifies matching skills, highlights potential skill gaps, and generates resume improvement suggestions.

## Features

- PDF resume text extraction
- Resume and job-description similarity analysis
- TF-IDF text representation
- Cosine similarity calculation
- Skill extraction using a predefined dictionary
- Matching and missing skill identification
- Skill coverage calculation
- Resume improvement suggestions
- Downloadable skill analysis CSV
- Downloadable analysis report

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- PyMuPDF
- Pandas

## NLP Techniques

### TF-IDF

Term Frequency-Inverse Document Frequency represents text numerically based on the importance of words in the documents being compared.

### Cosine Similarity

Cosine similarity measures the similarity between the numerical text representations.

### Skill Extraction

The application uses a predefined skill dictionary and text matching to identify skills in resumes and job descriptions.

## Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── analyzer.py
├── requirements.txt
└── README.md
```

## Installation

Clone or download the repository.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Limitations

- Similarity scores measure textual similarity and are not validated ATS scores.
- The skill dictionary does not cover every possible technical or soft skill.
- PDF extraction may fail on scanned documents without OCR.
- Recommendations should be reviewed by the user before modifying a resume.
- The application does not predict hiring decisions.

## Future Improvements

- Semantic similarity using sentence embeddings
- OCR support for scanned resumes
- Support for DOCX resumes
- Expanded skill taxonomy
- Evaluation against manually labelled resume-job pairs
- Optional AI-generated feedback grounded in resume content

## Disclaimer

This application is an educational project. Its scores and recommendations should not be treated as hiring decisions or guarantees of employment.