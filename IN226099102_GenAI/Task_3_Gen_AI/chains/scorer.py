"""
Deterministic scoring engine (Feature F).

Weighted scoring with the exact weights from the PRD:
    Required Skills : 45
    Experience      : 25
    Tools           : 15
    Education       :  5
    Bonus Signals   : 10
"""

from __future__ import annotations

from utils.schemas import MatchResult, ScoreResult, JobRequirements


# ---------------------------------------------------------------------------
# Scoring weights (from PRD section 6 — Feature F)
# ---------------------------------------------------------------------------
W_REQUIRED_SKILLS = 45
W_EXPERIENCE = 25
W_TOOLS = 15
W_EDUCATION = 5
W_BONUS = 10


def _label_from_score(score: float) -> str:
    """Map a numeric score to a human-readable fit label."""
    if score >= 80:
        return "Strong Fit"
    elif score >= 50:
        return "Moderate Fit"
    return "Weak Fit"


def score_candidate(
    match: MatchResult,
    requirements: JobRequirements,
) -> ScoreResult:
    """
    Compute a deterministic 0-100 score for a candidate.

    Args:
        match: Deterministic match output.
        requirements: Original JD requirements (needed for total counts).

    Returns:
        ScoreResult with component breakdowns, total score, and label.
    """
    # -----------------------------------------------------------------------
    # Required skills score  (45 pts)
    # -----------------------------------------------------------------------
    total_required = len(match.matched_required_skills) + len(match.missing_required_skills)
    if total_required > 0:
        required_ratio = len(match.matched_required_skills) / total_required
    else:
        required_ratio = 1.0  # No requirements => full credit
    req_score = round(required_ratio * W_REQUIRED_SKILLS, 2)

    # -----------------------------------------------------------------------
    # Experience score  (25 pts)
    # -----------------------------------------------------------------------
    if match.experience_gap is None:
        # Unknown experience → give partial credit
        exp_score = round(W_EXPERIENCE * 0.5, 2)
    elif match.experience_gap >= 0:
        exp_score = float(W_EXPERIENCE)
    else:
        # Negative gap: partial credit proportional to how close they are
        min_exp = requirements.min_years_experience or 1
        ratio = max(0, 1 + (match.experience_gap / min_exp))
        exp_score = round(ratio * W_EXPERIENCE, 2)

    # -----------------------------------------------------------------------
    # Tools score  (15 pts)
    # -----------------------------------------------------------------------
    total_tools = len(match.matched_tools) + len(match.missing_tools)
    if total_tools > 0:
        tools_ratio = len(match.matched_tools) / total_tools
    else:
        tools_ratio = 1.0
    tools_score = round(tools_ratio * W_TOOLS, 2)

    # -----------------------------------------------------------------------
    # Education score  (5 pts)
    # -----------------------------------------------------------------------
    edu_score = float(W_EDUCATION) if match.education_match else 0.0

    # -----------------------------------------------------------------------
    # Bonus score  (10 pts)  —  up to 5 bonus items counted
    # -----------------------------------------------------------------------
    bonus_ratio = min(match.bonus_points / 5, 1.0)
    bonus_score = round(bonus_ratio * W_BONUS, 2)

    # -----------------------------------------------------------------------
    # Total
    # -----------------------------------------------------------------------
    total = req_score + exp_score + tools_score + edu_score + bonus_score
    total = max(0.0, min(100.0, round(total, 2)))

    return ScoreResult(
        required_skills_score=req_score,
        experience_score=exp_score,
        tools_score=tools_score,
        education_score=edu_score,
        bonus_score=bonus_score,
        total_score=total,
        label=_label_from_score(total),
    )
