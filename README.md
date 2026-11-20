# AI Resume Analyzer Using Natural Language Processing (NLP)

A Python-based web application designed to analyze resumes against job descriptions using Natural Language Processing (NLP) techniques. The application extracts information from PDF resumes, evaluates textual similarity, identifies matching and missing skills, and generates actionable suggestions to help candidates improve their resumes.

## Project Overview

AI Resume Analyzer is a centralized resume evaluation platform that helps candidates understand how well their resumes align with specific job descriptions.

The application uses TF-IDF vectorization and Cosine Similarity to measure textual similarity between a resume and a job description. It also performs skill extraction using a predefined skill dictionary to identify relevant technical skills, highlight skill gaps, and calculate skill coverage.

The project demonstrates the practical application of NLP, text processing, information extraction, and machine learning techniques in a real-world recruitment-related use case.

## Key Objectives

- Automate resume analysis using NLP techniques.
- Evaluate resume relevance against job descriptions.
- Identify technical skills available in candidate resumes.
- Detect missing skills and potential skill gaps.
- Calculate resume-job description similarity.
- Generate suggestions for improving resume content.
- Provide downloadable analysis reports for further reference.

## Features

### 1. PDF Resume Text Extraction

- Upload resumes in PDF format.
- Extract textual content using PyMuPDF.
- Convert PDF content into text for further processing.
- Prepare extracted text for NLP-based analysis.

### 2. Resume and Job Description Matching

- Compare candidate resumes with job descriptions.
- Represent textual content using TF-IDF vectorization.
- Calculate similarity using Cosine Similarity.
- Generate a numerical similarity score.
- Help candidates understand the textual relevance of their resumes.

### 3. Skill Extraction and Identification

- Maintain a predefined dictionary of technical skills.
- Identify relevant skills from resume content.
- Extract required skills from job descriptions.
- Identify skills present in both documents.
- Highlight missing skills that may require attention.

### 4. Skill Gap Analysis

- Compare extracted resume skills with job requirements.
- Identify matching and missing skills.
- Categorize skill gaps based on predefined priority rules, if configured.
- Help candidates identify areas for improvement.

### 5. Skill Coverage Calculation

- Calculate the percentage of required job skills covered by the resume.
- Provide a quantitative overview of skill alignment.
- Present matching and missing skills for easier interpretation.

### 6. Resume Improvement Suggestions

- Generate suggestions based on identified skill gaps.
- Highlight areas where resume content can be improved.
- Recommend including relevant skills when supported by the candidate's actual experience.
- Help candidates improve the relevance and clarity of their resumes.

### 7. Downloadable Reports

- Generate downloadable skill analysis CSV files.
- Provide downloadable resume analysis reports.
- Allow candidates to retain and review their analysis results.

## 🛠️ Technology Stack

### Programming Language

| Technology | Purpose |
|---|---|
| Python | Core programming language used for application development. |

### Frontend and Application Framework

| Technology | Purpose |
|---|---|
| Streamlit | Building the interactive web application and user interface. |

### NLP and Machine Learning

| Technology | Purpose |
|---|---|
| Scikit-learn | Implementing TF-IDF vectorization and Cosine Similarity. |
| TF-IDF | Converting textual documents into numerical feature representations. |
| Cosine Similarity | Measuring similarity between resume and job description vectors. |

### PDF Processing and Data Handling

| Technology | Purpose |
|---|---|
| PyMuPDF | Extracting textual content from PDF resumes. |
| Pandas | Processing skill information and generating downloadable CSV reports. |

### Development Tools

| Technology | Purpose |
|---|---|
| Visual Studio Code | Application development and debugging. |
| Git | Version control and source code management. |
| GitHub | Project hosting and repository management. |
| Jupyter Notebook | Experimentation and testing of Python-based concepts. |

## 🔄 Complete Resume Analysis Workflow

The application follows a structured workflow to analyze resumes against job descriptions.

1. **Resume Upload:** The candidate uploads a resume in PDF format.
2. **Text Extraction:** PyMuPDF extracts textual content from the uploaded PDF.
3. **Job Description Input:** The candidate provides the target job description.
4. **Text Preprocessing:** Extracted resume text and job description are prepared for analysis.
5. **TF-IDF Vectorization:** Both documents are converted into numerical representations.
6. **Similarity Calculation:** Cosine Similarity calculates the textual similarity between the documents.
7. **Skill Extraction:** A predefined skill dictionary identifies skills from both documents.
8. **Skill Gap Analysis:** Matching and missing skills are identified.
9. **Skill Coverage Calculation:** The application calculates the percentage of required skills covered by the resume.
10. **Recommendation Generation:** Resume improvement suggestions are generated based on the analysis.
11. **Report Generation:** Results are presented through the application and made available for download.

### Additional Analysis Rules

- Similarity scores represent textual similarity, not actual ATS scores.
- Skill matching is based on the predefined skill dictionary.
- Missing skills are identified by comparing extracted resume skills with job requirements.
- Recommendations should be reviewed before modifying resume content.
- The application does not make hiring decisions.

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or later (use a version compatible with the installed dependencies).
- Visual Studio Code.
- Git.
- pip package manager.

### Step 1: Clone the Repository

```bash
git clone https://github.com/vaishnaviikommidi007/AI-Resume.git
```

Navigate to the project directory:

```bash
cd AI-Resume
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

The application uses dependencies such as:

- Streamlit
- Scikit-learn
- PyMuPDF
- Pandas

### Step 5: Run the Application

Start the Streamlit development server:

```bash
python -m streamlit run app.py
```

### Step 6: Access the Application

Open the local URL displayed in the terminal.

Typically:

```text
http://localhost:8501
```

The application is now ready for resume analysis.

## Learning Outcomes

Through this project, the following concepts were applied:

- Python-based application development.
- Natural Language Processing fundamentals.
- Text preprocessing and feature extraction.
- TF-IDF vectorization.
- Cosine Similarity and vector-based comparison.
- Skill extraction using dictionary-based matching.
- Skill gap identification and analysis.
- Data processing using Pandas.
- PDF text extraction using PyMuPDF.
- Building interactive applications using Streamlit.
- Generating downloadable analysis reports.
- Applying machine learning concepts to a practical recruitment-related problem.

## Project Information

| Category | Details |
|---|---|
| Project Name | AI Resume Analyzer Using Natural Language Processing |
| Domain | Artificial Intelligence and Natural Language Processing |
| Application Type | Python-Based Web Application |
| Programming Language | Python |
| Framework | Streamlit |
| NLP Library | Scikit-learn |
| PDF Processing | PyMuPDF |
| Data Processing | Pandas |
| Core Techniques | TF-IDF and Cosine Similarity |
| Repository | vaishnaviikommidi007/AI-Resume |
| Project Purpose | Educational and Practical Application of NLP |

## Disclaimer

This application is developed as an educational project to demonstrate the practical implementation of Natural Language Processing techniques in resume analysis.

The generated similarity scores, skill coverage percentages, and recommendations are intended to assist candidates in understanding resume relevance. They should not be treated as official ATS evaluation scores, hiring decisions, or guarantees of employment.
