# Product Requirements Document (PRD)

## Project Title

AI Resume Screening System with Tracing (Assignment Submission Ready)

## Project Root Folder

`gen_ai_task_3/`

---

# 1. Executive Summary

Build a production-style AI Resume Screening System that evaluates candidate resumes against a job description using LangChain pipelines, LangSmith tracing, deterministic scoring logic, and a Gradio web interface.

The system must:

* Accept PDF resumes
* Accept job description text
* Extract structured candidate information
* Compare candidate fit against job requirements
* Generate a score (0-100)
* Explain the score transparently
* Log all pipeline steps in LangSmith
* Demonstrate runs for Strong / Average / Weak candidates

This project should feel like a real recruiter tool, not just a notebook script.

---

# 2. Final Technical Decisions

## IDE / Development Environment

Primary target: VS Code
(Colab acceptable only for experimentation)

## LLM Provider

Groq API

## Final Model Choice

`meta-llama/llama-4-scout-17b-16e-instruct`

Reason:

* Strong structured extraction
* Good speed
* Higher token throughput
* Strong balance of quality + iteration speed

## UI Framework

Gradio

## Pipeline Framework

LangChain (PromptTemplate + LCEL + invoke())

## Observability

LangSmith (mandatory)

## Parsing Libraries

pypdf or pdfplumber

---

# 3. Assignment Mapping

## Required Inputs

* Minimum 3 resumes:

  * Strong candidate
  * Average candidate
  * Weak candidate
* 1 Job Description (Data Scientist recommended)

## Required Pipeline

Resume → Extract → Match → Score → Explain → Trace

## Required Submission Assets

* GitHub repository link
* LinkedIn post link
* LangSmith screenshots
* Working code

---

# 4. Product Vision

Create an AI recruiter assistant that reduces manual screening time while keeping decisions explainable, measurable, and debuggable.

---

# 5. User Personas

## Primary User

Recruiter / Hiring Manager

## Secondary User

Assignment Evaluator

## Tertiary User

Developer learning GenAI systems

---

# 6. Core Features

# Feature A: Resume Upload

## Inputs

* PDF resumes (mandatory)
* Multiple files supported

## Behavior

* Upload 1 to N resumes
* Extract raw text from each PDF
* Validate readable content
* Handle parse errors gracefully

## Errors

* Corrupt PDF
* Empty PDF
* Scanned image PDF with no text layer
* Password-protected PDF

---

# Feature B: Job Description Input

## Methods

1. Paste text in textbox (mandatory)
2. Upload JD file (optional)

---

# Feature C: Resume Structured Extraction

For each resume extract only from provided text:

```json
{
  "name": "",
  "skills": [],
  "tools": [],
  "years_experience": null,
  "education": [],
  "projects": [],
  "certifications": [],
  "domains": []
}
```

## Rules

* No hallucination
* If missing => null / []
* Return strict JSON
* Normalize duplicates

---

# Feature D: JD Requirement Extraction

Extract:

```json
{
  "role_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "tools": [],
  "min_years_experience": null,
  "education_requirements": []
}
```

---

# Feature E: Matching Engine

Deterministic Python logic preferred.

Compute:

* Matched required skills
* Missing required skills
* Preferred skill matches
* Tool matches
* Experience gap / surplus
* Education alignment
* Bonus relevance (projects/certs)

---

# Feature F: Scoring Engine

Use deterministic weighted scoring.

## Weighting

* Required Skills: 45
* Experience: 25
* Tools: 15
* Education: 5
* Bonus Signals: 10

## Formula

```python
score = sum(component_scores)
score = max(0, min(100, score))
```

## Labels

* 80–100 = Strong Fit
* 55–79 = Moderate Fit
* 0–54 = Weak Fit

---

# Feature G: Explainability Engine

LLM generates concise recruiter-friendly explanation.

Output sections:

* Final score summary
* Key strengths
* Missing requirements
* Why candidate ranked here
* Suggested improvements

---

# Feature H: Ranking Engine

When multiple resumes uploaded:

* Evaluate all candidates
* Sort by score descending
* Display rank #1, #2, #3...

---

# Feature I: LangSmith Tracing (Mandatory)

Every run must trace:

* Resume parsing
  n- Resume extraction
* JD extraction
* Matching
* Scoring
* Explanation

## Required Demo Runs

* strong_candidate
* average_candidate
* weak_candidate

## Debug Case Required

Example:
Initial prompt misses SQL from resume.
Prompt improved.
Re-run and compare traces.

## Suggested Tags

* extraction
* scoring
* debug_case
* final_submission

---

# Feature J: Gradio Interface

## Why Gradio

Transforms script into product demo.

## Layout

## Left Panel

* Upload resume PDFs
* Paste Job Description
* Evaluate button
* Clear button

## Right Panel

Tabs:

1. Ranked Results
2. Candidate Details
3. Raw JSON
4. Trace Instructions

## Ranked Results View

Table columns:

* Rank
* Candidate Name
* Score
* Label

## Candidate Details View

* Skills matched
* Missing skills
* Explanation
* Structured data

---

# 7. Functional Flow

1. Launch app
2. Upload resumes
3. Paste JD
4. Click Evaluate
5. For each resume:

   * Parse PDF text
   * Extract structured profile
   * Extract JD requirements
   * Match candidate vs JD
   * Score candidate
   * Generate explanation
   * Send trace to LangSmith
6. Show ranked outputs
7. Export screenshots for submission

---

# 8. Project Folder Structure

```text
gen_ai_task_3/
├── .env
├── .env.template
├── requirements.txt
├── README.md
├── app.py
├── main.py
├── doc.md
├── prompts/
│   ├── resume_extract.txt
│   ├── jd_extract.txt
│   ├── explain.txt
├── chains/
│   ├── extractor.py
│   ├── matcher.py
│   ├── scorer.py
│   ├── explainer.py
├── utils/
│   ├── parser.py
│   ├── schemas.py
│   ├── config.py
├── sample_data/
│   ├── strong_resume.pdf
│   ├── average_resume.pdf
│   ├── weak_resume.pdf
│   ├── data_scientist_jd.txt
```

---

# 9. Environment File Requirements

## .env

```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=resume-screening-system
MODEL_PROVIDER=groq
MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
TEMPERATURE=0
MAX_TOKENS=2048
```

## Behavior

* Load automatically with python-dotenv
* Validate required keys at startup
* Show readable error if missing

---

# 10. Prompt Engineering Rules

All prompts must include:

* Use only supplied text
* Do not infer unsupported claims
* Return strict JSON if requested
* Use null for unknown scalar fields
* Use [] for unknown lists
* Keep outputs concise and deterministic

---

# 11. LangChain Implementation Rules

Must use:

* PromptTemplate
* LCEL pipelines
* .invoke()
* Modular chain files

Avoid monolithic script logic.

---

# 12. Non-Functional Requirements

* Clean code
* Modular architecture
* Well-commented
* Readable names
* Fast response time
* Robust error handling
* Easy setup
* GitHub ready

---

# 13. Acceptance Criteria

Project passes when:

* App runs locally
* PDFs upload successfully
* JD input works
* Structured extraction works
* Scores generated for all candidates
* Explanations shown
* Ranking shown
* LangSmith traces visible
* 3 sample resumes tested
* Code follows folder structure

---

# 14. Submission Checklist

* GitHub repo uploaded
* README complete
* Screenshots of UI
* Screenshots of LangSmith traces
* LinkedIn post published
* Google Form submitted

---

# 15. Nice-to-Have Enhancements

* CSV export
* PDF report export
* Candidate comparison charts
* Deploy on Hugging Face Spaces
* Dark mode UI
* Batch mode screening

---

# 16. Build Strategy for Coding Agent

Phase 1:

* Setup project
* Create env loader
* Build parser
* Build chains
* Build scoring logic
* Build UI
* Validate traces

Phase 2:

* Improve prompts
* Better styling
* Add exports
* Improve docs

---

# 17. Final Insight

This is not just an assignment. It is a portfolio-grade GenAI system demonstrating:

* LLM pipelines
* Explainable AI
* Tooling discipline
* Observability
* Real product thinking
