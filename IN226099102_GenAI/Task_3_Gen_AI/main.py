"""
Main pipeline orchestrator for the AI Resume Screening System.

Coordinates the full flow:
    Resume PDF → Parse Text → Extract Profile → Extract JD →
    Match → Score → Explain → Return CandidateEvaluation

All steps are traced via LangSmith automatically (env vars set in config).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

# Ensure env is loaded before any LangChain import
from utils.config import LANGCHAIN_PROJECT  # noqa: F401  (side-effect import)

from utils.parser import extract_text_from_pdf
from utils.schemas import (
    CandidateEvaluation,
    JobRequirements,
    ResumeProfile,
)
from chains.extractor import extract_resume, extract_jd
from chains.matcher import match_candidate
from chains.scorer import score_candidate
from chains.explainer import explain_candidate

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Single-candidate pipeline
# ---------------------------------------------------------------------------

def evaluate_single_candidate(
    resume_text: str,
    jd_requirements: JobRequirements,
    filename: str = "unknown",
) -> CandidateEvaluation:
    """
    Run the full evaluation pipeline for one candidate.

    Args:
        resume_text: Raw text extracted from the candidate's PDF.
        jd_requirements: Pre-extracted job requirements (avoids re-extraction).
        filename: Original filename (used as fallback name).

    Returns:
        A fully populated CandidateEvaluation.
    """
    # Step 1 — Extract structured resume profile
    logger.info("Extracting profile from: %s", filename)
    profile: ResumeProfile = extract_resume(resume_text)

    # Use extracted name or fall back to filename
    candidate_name = profile.name or filename

    # Step 2 — Deterministic matching
    logger.info("Matching candidate: %s", candidate_name)
    match = match_candidate(profile, jd_requirements)

    # Step 3 — Deterministic scoring
    logger.info("Scoring candidate: %s", candidate_name)
    score = score_candidate(match, jd_requirements)

    # Step 4 — LLM explanation
    logger.info("Generating explanation for: %s", candidate_name)
    explanation = explain_candidate(candidate_name, match, score)

    return CandidateEvaluation(
        name=candidate_name,
        resume_profile=profile,
        match_result=match,
        score_result=score,
        explanation=explanation,
    )


# ---------------------------------------------------------------------------
# Multi-candidate pipeline  (Feature H — Ranking)
# ---------------------------------------------------------------------------

def evaluate_candidates(
    pdf_paths: List[str | Path],
    jd_text: str,
) -> Tuple[List[CandidateEvaluation], JobRequirements]:
    """
    Run the full pipeline for multiple candidates and rank them.

    Args:
        pdf_paths: List of paths to PDF resume files.
        jd_text: Raw job description text.

    Returns:
        Tuple of (ranked evaluations sorted by score desc, extracted JD requirements).
    """
    # Step 0 — Extract JD requirements once (shared across all candidates)
    logger.info("Extracting job description requirements...")
    jd_requirements = extract_jd(jd_text)

    evaluations: List[CandidateEvaluation] = []

    for pdf_path in pdf_paths:
        pdf_path = Path(pdf_path)

        # Step 1 — Parse PDF text
        logger.info("Parsing PDF: %s", pdf_path.name)
        resume_text = extract_text_from_pdf(pdf_path)

        # Handle parse errors gracefully
        if resume_text.startswith("[ERROR]"):
            logger.warning("Skipping %s: %s", pdf_path.name, resume_text)
            evaluations.append(
                CandidateEvaluation(
                    name=pdf_path.stem,
                    explanation=f"⚠️ Could not process this resume.\n{resume_text}",
                )
            )
            continue

        # Steps 2-4 — Full evaluation
        evaluation = evaluate_single_candidate(
            resume_text=resume_text,
            jd_requirements=jd_requirements,
            filename=pdf_path.stem,
        )
        evaluations.append(evaluation)

    # Step 5 — Rank by score descending (Feature H)
    evaluations.sort(key=lambda e: e.score_result.total_score, reverse=True)

    return evaluations, jd_requirements
