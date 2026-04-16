# AI Resume Screening System with Tracing

A production-style AI Resume Screening System that evaluates candidate resumes against a job description using LangChain pipelines, LangSmith tracing, deterministic scoring logic, and a polished Gradio web interface.

## 🏗️ Architecture

```
gen_ai_task_3/
├── .env                    # API keys (not committed)
├── .env.template           # Template for required env vars
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── app.py                  # Gradio web interface (entry point)
├── main.py                 # Pipeline orchestrator
├── doc.md                  # Internal API documentation
├── prd.md                  # Product requirements document
├── prompts/
│   ├── resume_extract.txt  # Resume extraction prompt
│   ├── jd_extract.txt      # JD extraction prompt 
│   └── explain.txt         # Explanation generation prompt
├── chains/
│   ├── extractor.py        # LCEL chains for resume & JD extraction
│   ├── matcher.py          # Deterministic matching engine
│   ├── scorer.py           # Deterministic weighted scoring engine
│   └── explainer.py        # LLM explanation chain
├── utils/
│   ├── config.py           # Environment loading & validation
│   ├── schemas.py          # Pydantic data models
│   └── parser.py           # PDF text extraction (pdfplumber + pypdf)
├── sample_data/
│   └── data_scientist_jd.txt  # Sample job description
└── unit_tests/
    ├── test_schemas.py     # Schema validation tests
    ├── test_matcher.py     # Matching engine tests
    ├── test_scorer.py      # Scoring engine tests
    └── test_parser.py      # PDF parser tests
```

## 🚀 Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.template` to `.env` and fill in your API keys:

```bash
cp .env.template .env
```

Required keys:
- `GROQ_API_KEY` — Get from [console.groq.com](https://console.groq.com)
- `LANGCHAIN_API_KEY` — Get from [smith.langchain.com](https://smith.langchain.com)

### 4. Run the application

```bash
python app.py
```

Open `http://localhost:7860` in your browser.

### 5. Run unit tests

```bash
pytest unit_tests/ -v
```

## 📋 How to Use

1. **Upload Resumes** — Upload one or more PDF resumes via the left panel.
2. **Paste Job Description** — Paste (or use the pre-loaded sample) JD text.
3. **Click "Evaluate Candidates"** — The system will:
   - Parse PDF text from each resume
   - Extract structured candidate profiles via LLM
   - Extract JD requirements via LLM
   - Match candidates against JD (deterministic)
   - Score candidates (deterministic weighted scoring)
   - Generate recruiter-friendly explanations via LLM
   - Rank all candidates by score
4. **View Results** across 4 tabs:
   - **Ranked Results** — Table with Rank, Name, Score, Label
   - **Candidate Details** — Score breakdown, skills analysis, explanation
   - **Raw JSON** — Full structured extraction data
   - **Trace Info** — Instructions to view LangSmith traces

## ⚖️ Scoring System

| Component | Weight | Description |
|---|---|---|
| Required Skills | 45 | Ratio of matched/total required skills |
| Experience | 25 | Full if meets/exceeds, proportional otherwise |
| Tools | 15 | Ratio of matched/total required tools |
| Education | 5 | Binary — matches or doesn't |
| Bonus Signals | 10 | Projects + certifications (up to 5 items) |

### Labels
- **Strong Fit**: 80–100
- **Moderate Fit**: 55–79
- **Weak Fit**: 0–54

## 🔍 LangSmith Tracing

All LLM calls are automatically traced. View them at [smith.langchain.com](https://smith.langchain.com).

**Tags used:**
- `extraction`, `resume` — Resume extraction chain
- `extraction`, `jd` — JD extraction chain
- `explanation`, `scoring` — Explanation chain

## 🛠️ Tech Stack

- **LLM**: `meta-llama/llama-4-scout-17b-16e-instruct` via Groq
- **Pipeline**: LangChain LCEL (ChatPromptTemplate | ChatGroq | StrOutputParser)
- **Tracing**: LangSmith
- **UI**: Gradio Blocks
- **PDF Parsing**: pdfplumber + pypdf fallback
- **Validation**: Pydantic v2
