# Applicant Tracking System (ATS) using AI & NLP

## Overview

This project is an **AI-powered Applicant Tracking System (ATS)** that automatically matches and ranks resumes against a given job description. It uses **Natural Language Processing (NLP)** and **Machine Learning techniques** to simulate how modern ATS platforms shortlist candidates.

The system is designed to help recruiters quickly identify the **best-fit candidates** based on:

* Resume–job text similarity
* Skill coverage
* Relevant experience
* Education match

---

## Key Features

* Upload and analyze **multiple resumes at once**
* Automatic **resume text extraction** (PDF / DOCX)
* **Experience extraction** using numeric patterns, date ranges, and role-based heuristics
* Weighted **multi-factor scoring system**
* Ranked candidate list with transparent scoring
* Simple and interactive **Streamlit UI**

---

## Tech Stack

* **Programming Language:** Python
* **Frontend:** Streamlit
* **NLP & ML:**

  * TF-IDF Vectorizer
  * Cosine Similarity
  * NLTK
* **Data Processing:** Pandas
* **Resume Parsing:**

  * PyMuPDF (PDF)
  * python-docx (DOCX)

---

## System Architecture

```
Resumes (PDF/DOCX)
        ↓
Text Extraction
        ↓
NLP Preprocessing
        ↓
Feature Matching & Scoring
        ↓
Candidate Ranking Output
```

---

## Scoring Logic

Each candidate is scored using a **weighted formula**:

| Component        | Weight |
| ---------------- | ------ |
| Text Similarity  | 40%    |
| Skill Coverage   | 30%    |
| Experience Match | 20%    |
| Education Match  | 10%    |

### Final Score Formula

```
Final Score =
(0.40 × Text Match) +
(0.30 × Skill Match) +
(0.20 × Experience Match) +
(0.10 × Education Match)
```

This makes the ranking **transparent and explainable**, which is critical in real ATS systems.

---

## Experience Extraction Strategy

The system extracts experience using:

* Numeric patterns: `3 years`, `5+ years`
* Date ranges: `2019 – 2023`
* Role and keyword context (e.g., Software Engineer, Data Analyst)

This hybrid approach improves robustness compared to simple keyword matching.

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/bhanvadiyaneel31-netizen/Applicant-Tracking-System.git
cd Applicant-Tracking-System
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## Testing Data

Resumes.zip is provided as sample input data to quickly test the ATS output.

---

## Sample Output

```
Candidate Name | Final Score | Skill Match | Experience
-------------------------------------------------------
John Doe       | 82%         | 90%         | 4 Years
Jane Smith     | 76%         | 85%         | 3 Years
```

Candidates are displayed in **descending order of relevance**.

---

## Use Cases

* Recruiters shortlisting resumes
* HR automation prototypes
* Resume screening for startups
* Internship / portfolio project for AI & ML roles

---

## Limitations

* Rule-based skill matching (can be enhanced with embeddings)
* No deep learning models (by design for interpretability)
* English resumes only

---

## Future Enhancements

* BERT / Sentence Transformers for semantic matching
* Resume skill ontology
* Bias mitigation techniques
* ATS score explainability dashboard
* Database integration
* API version (FastAPI)

---

## Project Status

**Stage:** Portfolio / Internship-ready
**Focus:** Practical NLP + ML application with explainable scoring

---

## Author

**Neel Bhanvadiya**
AI / ML Engineer (Aspirant)