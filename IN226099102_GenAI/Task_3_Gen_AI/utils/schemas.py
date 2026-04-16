"""
Pydantic schemas for structured data extraction.

These schemas define the exact JSON shape returned by the LLM
and consumed by the deterministic scoring engine.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Resume extraction schema  (Feature C)
# ---------------------------------------------------------------------------

class ResumeProfile(BaseModel):
    """Structured profile extracted from a candidate's resume text."""

    name: Optional[str] = Field(
        None, description="Full name of the candidate"
    )
    skills: List[str] = Field(
        default_factory=list,
        description="Technical and soft skills mentioned in the resume",
    )
    tools: List[str] = Field(
        default_factory=list,
        description="Tools, frameworks, and platforms the candidate has used",
    )
    years_experience: Optional[float] = Field(
        None, description="Total years of professional experience"
    )
    education: List[str] = Field(
        default_factory=list,
        description="Degrees and educational qualifications",
    )
    projects: List[str] = Field(
        default_factory=list,
        description="Notable projects mentioned",
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="Professional certifications",
    )
    domains: List[str] = Field(
        default_factory=list,
        description="Industry domains the candidate has experience in",
    )


# ---------------------------------------------------------------------------
# Job description extraction schema  (Feature D)
# ---------------------------------------------------------------------------

class JobRequirements(BaseModel):
    """Structured requirements extracted from a job description."""

    role_title: Optional[str] = Field(
        None, description="Title of the role"
    )
    required_skills: List[str] = Field(
        default_factory=list,
        description="Skills explicitly listed as required",
    )
    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Skills listed as preferred / nice-to-have",
    )
    tools: List[str] = Field(
        default_factory=list,
        description="Tools and platforms required or preferred",
    )
    min_years_experience: Optional[float] = Field(
        None, description="Minimum years of experience required"
    )
    education_requirements: List[str] = Field(
        default_factory=list,
        description="Degree or education requirements",
    )


# ---------------------------------------------------------------------------
# Match results schema  (Feature E)
# ---------------------------------------------------------------------------

class MatchResult(BaseModel):
    """Output of the deterministic matching engine."""

    matched_required_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    matched_preferred_skills: List[str] = Field(default_factory=list)
    matched_tools: List[str] = Field(default_factory=list)
    missing_tools: List[str] = Field(default_factory=list)
    experience_gap: Optional[float] = Field(
        None,
        description="Positive = surplus, negative = shortfall, None = unknown",
    )
    education_match: bool = Field(False)
    bonus_points: int = Field(
        0, description="Count of projects + certifications"
    )


# ---------------------------------------------------------------------------
# Scoring result schema  (Feature F)
# ---------------------------------------------------------------------------

class ScoreResult(BaseModel):
    """Final score breakdown for a candidate."""

    required_skills_score: float = 0.0
    experience_score: float = 0.0
    tools_score: float = 0.0
    education_score: float = 0.0
    bonus_score: float = 0.0
    total_score: float = 0.0
    label: str = "Weak Fit"


# ---------------------------------------------------------------------------
# Full candidate evaluation  (pipeline output)
# ---------------------------------------------------------------------------

class CandidateEvaluation(BaseModel):
    """Complete evaluation result for one candidate."""

    name: str = "Unknown"
    resume_profile: ResumeProfile = Field(default_factory=ResumeProfile)
    match_result: MatchResult = Field(default_factory=MatchResult)
    score_result: ScoreResult = Field(default_factory=ScoreResult)
    explanation: str = ""
