"""
Deterministic matching engine (Feature E).

Pure Python logic — no LLM calls here.
Compares a ResumeProfile against JobRequirements and produces a MatchResult.
"""

from __future__ import annotations

from utils.schemas import ResumeProfile, JobRequirements, MatchResult


def _normalize(items: list[str]) -> set[str]:
    """Lowercase and strip items for case-insensitive comparison."""
    return {item.strip().lower() for item in items if item}


def match_candidate(
    profile: ResumeProfile,
    requirements: JobRequirements,
) -> MatchResult:
    """
    Perform deterministic skill / experience / education matching.

    Args:
        profile: Extracted candidate profile.
        requirements: Extracted job requirements.

    Returns:
        MatchResult with matched/missing breakdowns.
    """
    # -----------------------------------------------------------------------
    # Normalize all lists to lowercase sets for fair comparison
    # -----------------------------------------------------------------------
    candidate_skills = _normalize(profile.skills)
    candidate_tools = _normalize(profile.tools)
    candidate_education = _normalize(profile.education)

    required_skills = _normalize(requirements.required_skills)
    preferred_skills = _normalize(requirements.preferred_skills)
    required_tools = _normalize(requirements.tools)
    required_education = _normalize(requirements.education_requirements)

    def _fuzzy_match(required_set: set[str], provided_set: set[str]) -> tuple[list[str], list[str]]:
        matched = []
        missing = []
        req_list = list(required_set)
        prov_list = list(provided_set)
        
        for req in req_list:
            found = False
            for prov in prov_list:
                if req in prov or prov in req:
                    found = True
                    break
            if found:
                matched.append(req)
            else:
                missing.append(req)
        return matched, missing

    # -----------------------------------------------------------------------
    # Required skills matching
    # -----------------------------------------------------------------------
    matched_req, missing_req = _fuzzy_match(required_skills, candidate_skills)

    # -----------------------------------------------------------------------
    # Preferred skills matching
    # -----------------------------------------------------------------------
    matched_pref, _ = _fuzzy_match(preferred_skills, candidate_skills)

    # -----------------------------------------------------------------------
    # Tools matching
    # -----------------------------------------------------------------------
    matched_tools, missing_tools = _fuzzy_match(required_tools, candidate_tools)

    # -----------------------------------------------------------------------
    # Experience gap  (positive = surplus, negative = shortfall)
    # -----------------------------------------------------------------------
    experience_gap = None
    if (
        profile.years_experience is not None
        and requirements.min_years_experience is not None
    ):
        experience_gap = profile.years_experience - requirements.min_years_experience

    # -----------------------------------------------------------------------
    # Education alignment — simple substring check
    # -----------------------------------------------------------------------
    education_match = False
    if required_education and candidate_education:
        # Check if any candidate degree keyword appears in any requirement
        for c_edu in candidate_education:
            for r_edu in required_education:
                if r_edu in c_edu or c_edu in r_edu:
                    education_match = True
                    break

    # -----------------------------------------------------------------------
    # Bonus signals — projects + certifications count
    # -----------------------------------------------------------------------
    bonus_points = len(profile.projects) + len(profile.certifications)

    return MatchResult(
        matched_required_skills=sorted(matched_req),
        missing_required_skills=sorted(missing_req),
        matched_preferred_skills=sorted(matched_pref),
        matched_tools=sorted(matched_tools),
        missing_tools=sorted(missing_tools),
        experience_gap=experience_gap,
        education_match=education_match,
        bonus_points=bonus_points,
    )
