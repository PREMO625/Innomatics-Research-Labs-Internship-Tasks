"""
Gradio web interface for the AI Resume Screening System.

Layout (per PRD Feature J):
    Left Panel  — Upload resumes, paste JD, Evaluate / Clear buttons
    Right Panel — Tabs: Ranked Results | Candidate Details | Raw JSON | Trace Info

Launch:  python app.py
"""

from __future__ import annotations

import json
import logging
import traceback
from pathlib import Path
from typing import List

import gradio as gr
import pandas as pd

# Side-effect import: validates env + sets LangSmith vars before anything else
from utils.config import LANGCHAIN_PROJECT, MODEL_NAME  # noqa: F401

from main import evaluate_candidates
from utils.schemas import CandidateEvaluation

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sample JD for convenience
# ---------------------------------------------------------------------------
_SAMPLE_JD_PATH = Path(__file__).parent / "sample_data" / "data_scientist_jd.txt"
_SAMPLE_JD = ""
if _SAMPLE_JD_PATH.exists():
    _SAMPLE_JD = _SAMPLE_JD_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Core callback
# ---------------------------------------------------------------------------

def run_evaluation(
    pdf_files: list | None,
    jd_text: str,
) -> tuple:
    """
    Gradio callback — runs the full pipeline and formats outputs.

    Returns:
        (ranking_df, details_md, raw_json_str, status_msg)
    """
    # Validation
    if not pdf_files:
        return (
            pd.DataFrame(),
            "⚠️ Please upload at least one PDF resume.",
            "{}",
            "❌ No resumes uploaded.",
        )

    if not jd_text or not jd_text.strip():
        return (
            pd.DataFrame(),
            "⚠️ Please paste a job description.",
            "{}",
            "❌ No job description provided.",
        )

    try:
        # Resolve file paths from Gradio upload objects
        pdf_paths: List[str] = []
        for f in pdf_files:
            # Gradio >= 5 returns a file path string directly
            if isinstance(f, str):
                pdf_paths.append(f)
            elif hasattr(f, "name"):
                pdf_paths.append(f.name)
            else:
                pdf_paths.append(str(f))

        logger.info(
            "Starting evaluation for %d resume(s)...", len(pdf_paths)
        )

        # Run the full pipeline
        evaluations, jd_requirements = evaluate_candidates(pdf_paths, jd_text)

        # ----- Build outputs -----
        ranking_df = _build_ranking_table(evaluations)
        details_md = _build_details_markdown(evaluations)
        raw_json = _build_raw_json(evaluations, jd_requirements)
        status = f"✅ Evaluated {len(evaluations)} candidate(s) successfully."

        return ranking_df, details_md, raw_json, status

    except Exception as exc:
        logger.error("Pipeline error: %s", traceback.format_exc())
        return (
            pd.DataFrame(),
            f"❌ An error occurred:\n```\n{exc}\n```",
            "{}",
            f"❌ Error: {exc}",
        )


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def _build_ranking_table(evals: List[CandidateEvaluation]) -> pd.DataFrame:
    """Build the ranked results DataFrame (Feature H)."""
    rows = []
    for rank, ev in enumerate(evals, start=1):
        rows.append({
            "Rank": rank,
            "Candidate": ev.name,
            "Score": ev.score_result.total_score,
            "Label": ev.score_result.label,
        })
    return pd.DataFrame(rows)


def _build_details_markdown(evals: List[CandidateEvaluation]) -> str:
    """Build a combined Markdown string with per-candidate details."""
    sections: list[str] = []
    for rank, ev in enumerate(evals, start=1):
        m = ev.match_result
        s = ev.score_result
        section = f"""
---
### #{rank} — {ev.name}  •  **{s.total_score}/100**  ({s.label})

#### Score Breakdown
| Component | Score |
|---|---|
| Required Skills | {s.required_skills_score} / 45 |
| Experience | {s.experience_score} / 25 |
| Tools | {s.tools_score} / 15 |
| Education | {s.education_score} / 5 |
| Bonus Signals | {s.bonus_score} / 10 |
| **Total** | **{s.total_score} / 100** |

#### Skills Analysis
- ✅ **Matched Required**: {', '.join(m.matched_required_skills) or 'None'}
- ❌ **Missing Required**: {', '.join(m.missing_required_skills) or 'None'}
- 🟢 **Matched Preferred**: {', '.join(m.matched_preferred_skills) or 'None'}
- 🔧 **Matched Tools**: {', '.join(m.matched_tools) or 'None'}
- 🔴 **Missing Tools**: {', '.join(m.missing_tools) or 'None'}

#### Recruiter Explanation
{ev.explanation}
"""
        sections.append(section.strip())
    return "\n\n".join(sections)


def _build_raw_json(evals, jd_requirements) -> str:
    """Serialize all evaluation data as pretty JSON."""
    payload = {
        "job_requirements": jd_requirements.model_dump(),
        "candidates": [
            {
                "name": ev.name,
                "resume_profile": ev.resume_profile.model_dump(),
                "match_result": ev.match_result.model_dump(),
                "score_result": ev.score_result.model_dump(),
                "explanation": ev.explanation,
            }
            for ev in evals
        ],
    }
    return json.dumps(payload, indent=2, default=str)


# ---------------------------------------------------------------------------
# Gradio UI  (Feature J)
# ---------------------------------------------------------------------------

def build_ui() -> gr.Blocks:
    """Construct and return the Gradio Blocks application."""

    with gr.Blocks(
        title="AI Resume Screening System",
        theme=gr.themes.Soft(),
        css="""
            .main-title { text-align: center; margin-bottom: 0.5rem; }
            .subtitle   { text-align: center; color: #666; margin-top: 0; }
        """,
    ) as demo:

        # Header
        gr.Markdown(
            "# 🎯 AI Resume Screening System",
            elem_classes=["main-title"],
        )
        gr.Markdown(
            f"*Powered by **{MODEL_NAME}** via Groq  •  Traced with LangSmith  •  Project: `{LANGCHAIN_PROJECT}`*",
            elem_classes=["subtitle"],
        )

        with gr.Row():
            # ---- LEFT PANEL ----
            with gr.Column(scale=1):
                gr.Markdown("### 📄 Inputs")

                pdf_input = gr.File(
                    label="Upload Resume PDFs",
                    file_count="multiple",
                    file_types=[".pdf"],
                    type="filepath",
                )

                jd_input = gr.Textbox(
                    label="Job Description",
                    placeholder="Paste the full job description here...",
                    lines=12,
                    value=_SAMPLE_JD,
                )

                with gr.Row():
                    evaluate_btn = gr.Button(
                        "🚀 Evaluate Candidates",
                        variant="primary",
                        scale=2,
                    )
                    clear_btn = gr.ClearButton(
                        value="🗑️ Clear",
                        scale=1,
                    )

                status_box = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=1,
                )

            # ---- RIGHT PANEL ----
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.Tab("📊 Ranked Results"):
                        ranking_table = gr.Dataframe(
                            headers=["Rank", "Candidate", "Score", "Label"],
                            label="Candidate Rankings",
                            interactive=False,
                        )

                    with gr.Tab("📝 Candidate Details"):
                        details_output = gr.Markdown(
                            value="*Upload resumes and click Evaluate to see detailed results.*"
                        )

                    with gr.Tab("🔗 Raw JSON"):
                        json_output = gr.Code(
                            label="Raw Extraction & Scoring Data",
                            language="json",
                            lines=25,
                        )

                    with gr.Tab("🔍 Trace Info"):
                        gr.Markdown(f"""
### LangSmith Tracing

All pipeline runs are automatically traced to **LangSmith**.

**How to view traces:**
1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Open project: **`{LANGCHAIN_PROJECT}`**
3. Filter by tags: `extraction`, `resume`, `jd`, `explanation`, `scoring`

**Tags used in this project:**
| Tag | Purpose |
|---|---|
| `extraction` | Resume & JD extraction chains |
| `resume` | Resume-specific extraction |
| `jd` | Job description extraction |
| `explanation` | Explanation generation |
| `scoring` | Score explanation chain |

**Suggested demo runs:**
- Upload a strong candidate resume → expect 80+ score
- Upload an average candidate resume → expect 50-79 score
- Upload a weak candidate resume → expect 0-49 score
""")

        # ---- Wire up callbacks ----
        evaluate_btn.click(
            fn=run_evaluation,
            inputs=[pdf_input, jd_input],
            outputs=[ranking_table, details_output, json_output, status_box],
        )

        clear_btn.add(
            [pdf_input, jd_input, ranking_table, details_output, json_output, status_box]
        )

    return demo


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = build_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
    )
