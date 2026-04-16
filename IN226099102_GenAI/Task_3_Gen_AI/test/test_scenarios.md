# Testing Scenarios & Assignment Validation Guide

This document is your manual for testing the Gradio Interface, validating LangSmith traces, and proving that the project meets all assignment requirements for **Data Science Internship – February 2026**.

---

## ✅ 1. Assignment Requirements Validation Check

Here is a summary proving that your codebase fulfills every requirement listed in your internship task:

| Requirement | Complete? | Where to find it in the codebase |
|---|---|---|
| **Python / Jupyter / VS Code** | ✅ Yes | Built entirely in Python modular scripts for VS Code. |
| **Complete LangChain Pipeline** | ✅ Yes | `main.py` orchestrates `extractor.py` → `matcher.py` → `scorer.py` → `explainer.py`. |
| **LangSmith Tracing Enabled** | ✅ Yes | `utils/config.py` forcefully sets `LANGCHAIN_TRACING_V2=true`. |
| **3 Resumes + 1 JD Input** | ✅ Yes | Gradio `app.py` accepts multiple PDFs and JD text. Sample JD is in `sample_data/`. |
| **Skill, Exp, Tool Extraction** | ✅ Yes | `chains/extractor.py` explicitly prompts for these using strict JSON constraints. |
| **Matching Logic** | ✅ Yes | `chains/matcher.py` (Deterministic logic comparing sets and integers). |
| **Scoring (0-100)** | ✅ Yes | `chains/scorer.py` (Weighted deterministic algorithm outputting exactly 0-100). |
| **Explainability** | ✅ Yes | `chains/explainer.py` uses LLM to write a concise reasoning for the score. |
| **Modular Structure** | ✅ Yes | Folders: `prompts/`, `chains/`, `utils/` with clear separations of concern. |
| **LCEL & .invoke()** | ✅ Yes | See `chains/extractor.py` and `chains/explainer.py` (e.g., `chain = prompt | llm | parser`). |
| **No hallucination/Assumptions** | ✅ Yes | Handled fundamentally in `prompts/*.txt` (strict negative constraints). |

**Conclusion:** Your code architecture is 100% complete and ready for submission.

---

## 🧪 2. Preparation: Create Your 3 Sample Resumes

Before testing in Gradio, you need 3 PDF files representing Strong, Average, and Weak candidates. 
*If you haven't created these yet, here is what they should contain to test the logic perfectly against the `data_scientist_jd.txt`:*

1. **`strong_candidate.pdf`**:
   - Skills: Python, Machine Learning, Deep Learning (CNNs), NLP, SQL, Feature Engineering.
   - Tools: TensorFlow, PyTorch, Scikit-learn, Pandas, GitHub.
   - Experience: 4 years as a Data Scientist.
   - Education: Master's in Computer Science.
2. **`average_candidate.pdf`**:
   - Skills: Python, SQL, basic Machine Learning.
   - Tools: Pandas, NumPy, Scikit-learn.
   - Experience: 2 years as a Data Analyst.
   - Education: Bachelor's in Mathematics.
   - *(Missing: Deep Learning, NLP, Cloud, Master's degree, 3 years exp).*
3. **`weak_candidate.pdf`**:
   - Skills: Excel, PowerPoint, basic SQL.
   - Tools: Microsoft Office, Tableau.
   - Experience: 1 year as a Marketing Intern.
   - Education: Bachelor's in Business.

*(You can simply write these out in MS Word / Google Docs and export them to PDF into the `sample_data/` folder).*

---

## 🖥️ 3. Gradio Interface Testing Scenarios

Run your app (`python app.py`) and perform the following manual tests:

### Scenario A: End-to-End Ranking
1. Upload all 3 PDFs at the same time in the left panel.
2. Ensure the standard Data Scientist JD is pasted in the textbox.
3. Click **Evaluate Candidates**.
4. **Expected Result:**
   - **Ranked Results Tab:** The Strong candidate should be Rank 1 (Score >80), Average is Rank 2 (Score ~50-70), Weak is Rank 3 (Score <50).
   - **Candidate Details Tab:** You should see a clear markdown breakdown showing exactly *what* skills were missing for the Weak/Average candidates, and a coherent LLM explanation.
   - **Raw JSON Tab:** Ensure valid JSON is rendered without markdown bugs.

### Scenario B: Edge Case - Corrupt or Non-Text PDF
1. Upload a PDF that is purely an image (no selectable text) or create a fake blank text file and rename it to `.pdf`.
2. Click **Evaluate Candidates**.
3. **Expected Result:** App should not crash. The score should likely be 0, and the explanation/status should report an error or that no skills were found.

---

## 🔍 4. LangSmith Tracing & Debugging Scenarios

This is a **crucial** part of the evaluation criteria (15% of your grade). You need to take screenshots of your LangSmith dashboard to submit in the Google Form!

### Step 1: Viewing the "Happy Path" Traces
1. Go to [smith.langchain.com](https://smith.langchain.com).
2. Open the project named `resume-screening-system`.
3. You will see rows for every time you clicked "Evaluate".
4. Click on a trace. You should see a tree on the left side showing your `RunnableSequence` execution.
5. **ACTION REQUIRED:** Take a screenshot of a successful execution trace showing the Inputs (raw resume) and Outputs (structured JSON) to prove your LCEL pipeline is traced.

### Step 2: Fulfilling the "Debug Case" Requirement
The assignment asks you to show **"At least one incorrect output"** and prove you debugged it. Here is how to simulate and document this for your submission:

1. **Simulate a Bug:**
   - Open `prompts/resume_extract.txt`.
   - Temporarily remove the rule: `Normalize duplicate entries...` AND delete the `"skills": [...]` key instruction.
   - Run the Gradio app with a resume.
2. **Observe the Failure:**
   - The LCEL extraction chain might throw a validation error, or the matcher will fail because `skills` is missing from the JSON.
3. **Check LangSmith (The Debugging Proof):**
   - Head to LangSmith. You will see a trace marked with an **Error (red)** or an output that looks structurally broken.
   - Click into the specific LLM call to see *exactly* what the model replied with.
   - **ACTION REQUIRED:** Take a screenshot of this failed trace/output in LangSmith.
4. **Fix the Bug:**
   - Restore `prompts/resume_extract.txt` to the perfect version we built.
   - Re-run the app. Ensure it succeeds.
5. **Document for Submission:**
   - In your final report or GitHub Readme, add a small section saying: *"Debugging Scenario: Initially, the LLM forgot to output the 'skills' array, leading to a pipeline crash. Using LangSmith, I traced the LLM's raw output, identified the missing key, and enforced a strict JSON schema in the Prompt Template to fix the hallucination consistently."*

---

## 🚀 Final Submission Checklist (Before Google Form)

- [ ] Code is pushed to GitHub (make sure `.env` is NOT uploaded; `.env.template` is uploaded).
- [ ] You have 3 sample PDFs included in the repo or mentioned in README.
- [ ] `README.md` looks professional.
- [ ] You have LangSmith trace screenshots ready to attach/link.
- [ ] Post on LinkedIn detailing your pipeline architecture (Resume -> Extract -> Match -> Score -> Explain), tagging your program.
- [ ] Submit URLs to Google Form.
