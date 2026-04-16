"""
Explainability chain (Feature G).

Generates a recruiter-friendly explanation using LLM via LCEL,
given the match + score context for a candidate.
"""

from __future__ import annotations

import logging
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from utils.config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from utils.schemas import MatchResult, ScoreResult

logger = logging.getLogger(__name__)

_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def _build_llm() -> ChatGroq:
    """Build the ChatGroq LLM instance."""
    return ChatGroq(
        model=MODEL_NAME,
        temperature=0.3,  # Slightly creative for explanation text
        max_tokens=MAX_TOKENS,
        max_retries=3,
        api_key=GROQ_API_KEY,
    )


def explain_candidate(
    candidate_name: str,
    match: MatchResult,
    score: ScoreResult,
) -> str:
    """
    Generate a concise recruiter-friendly explanation.

    Pipeline: ChatPromptTemplate -> ChatGroq -> StrOutputParser

    Args:
        candidate_name: Name of the candidate.
        match: Deterministic match result.
        score: Deterministic score result.

    Returns:
        Human-readable explanation string.
    """
    prompt_template = (_PROMPT_DIR / "explain.txt").read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior technical recruiter."),
        ("user", prompt_template),
    ])

    llm = _build_llm()
    parser = StrOutputParser()

    chain = prompt | llm | parser

    # Format experience gap for display
    if match.experience_gap is not None:
        exp_gap_str = (
            f"{match.experience_gap:+.1f} years"
            if match.experience_gap != 0
            else "Meets requirement"
        )
    else:
        exp_gap_str = "Unknown (not specified in resume or JD)"

    try:
        explanation: str = chain.invoke(
            {
                "candidate_name": candidate_name,
                "score": score.total_score,
                "label": score.label,
                "matched_required": ", ".join(match.matched_required_skills) or "None",
                "missing_required": ", ".join(match.missing_required_skills) or "None",
                "matched_preferred": ", ".join(match.matched_preferred_skills) or "None",
                "matched_tools": ", ".join(match.matched_tools) or "None",
                "missing_tools": ", ".join(match.missing_tools) or "None",
                "experience_gap": exp_gap_str,
                "education_match": "Yes" if match.education_match else "No",
                "bonus_points": str(match.bonus_points),
            },
            config={"tags": ["explanation", "scoring"]},
        )
        return explanation.strip()
    except Exception as exc:
        logger.error("Explanation generation failed: %s", exc)
        return (
            f"Score: {score.total_score}/100 ({score.label}). "
            "Explanation could not be generated due to an error."
        )
