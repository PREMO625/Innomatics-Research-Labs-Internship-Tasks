"""
Unit tests for chains.scorer — deterministic scoring logic.
"""

import pytest
from utils.schemas import MatchResult, JobRequirements
from chains.scorer import score_candidate, _label_from_score


class TestLabelFromScore:
    """Test the label classification boundaries."""

    def test_strong_fit(self):
        assert _label_from_score(80) == "Strong Fit"
        assert _label_from_score(100) == "Strong Fit"
        assert _label_from_score(95.5) == "Strong Fit"

    def test_moderate_fit(self):
        assert _label_from_score(50) == "Moderate Fit"
        assert _label_from_score(79) == "Moderate Fit"
        assert _label_from_score(67.3) == "Moderate Fit"

    def test_weak_fit(self):
        assert _label_from_score(0) == "Weak Fit"
        assert _label_from_score(49) == "Weak Fit"
        assert _label_from_score(30.5) == "Weak Fit"


class TestScoreCandidate:
    """Test the full scoring engine."""

    @pytest.fixture
    def jd(self) -> JobRequirements:
        return JobRequirements(
            required_skills=["Python", "ML", "SQL", "NLP"],
            tools=["TensorFlow", "Pandas", "Git"],
            min_years_experience=3.0,
            education_requirements=["master's"],
        )

    def test_perfect_candidate(self, jd):
        """A candidate matching everything should score near 100."""
        match = MatchResult(
            matched_required_skills=["python", "ml", "sql", "nlp"],
            missing_required_skills=[],
            matched_tools=["tensorflow", "pandas", "git"],
            missing_tools=[],
            experience_gap=2.0,
            education_match=True,
            bonus_points=5,
        )
        result = score_candidate(match, jd)
        assert result.total_score == 100.0
        assert result.label == "Strong Fit"

    def test_zero_match_candidate(self, jd):
        """A candidate matching nothing should score very low."""
        match = MatchResult(
            matched_required_skills=[],
            missing_required_skills=["python", "ml", "sql", "nlp"],
            matched_tools=[],
            missing_tools=["tensorflow", "pandas", "git"],
            experience_gap=-3.0,
            education_match=False,
            bonus_points=0,
        )
        result = score_candidate(match, jd)
        assert result.total_score == 0.0
        assert result.label == "Weak Fit"

    def test_partial_candidate(self, jd):
        """A candidate with partial matches should score in middle ranges."""
        match = MatchResult(
            matched_required_skills=["python", "sql"],
            missing_required_skills=["ml", "nlp"],
            matched_tools=["pandas"],
            missing_tools=["tensorflow", "git"],
            experience_gap=0.0,
            education_match=True,
            bonus_points=2,
        )
        result = score_candidate(match, jd)
        assert 30 < result.total_score < 75
        assert result.required_skills_score == 22.5  # 2/4 * 45

    def test_score_clamped_to_100(self, jd):
        """Score must never exceed 100."""
        match = MatchResult(
            matched_required_skills=["python", "ml", "sql", "nlp"],
            missing_required_skills=[],
            matched_tools=["tensorflow", "pandas", "git"],
            missing_tools=[],
            experience_gap=10.0,
            education_match=True,
            bonus_points=20,
        )
        result = score_candidate(match, jd)
        assert result.total_score <= 100.0

    def test_score_clamped_to_0(self, jd):
        """Score must never go below 0."""
        match = MatchResult(
            matched_required_skills=[],
            missing_required_skills=["python", "ml", "sql", "nlp"],
            matched_tools=[],
            missing_tools=["tensorflow", "pandas", "git"],
            experience_gap=-100.0,
            education_match=False,
            bonus_points=0,
        )
        result = score_candidate(match, jd)
        assert result.total_score >= 0.0

    def test_unknown_experience_gives_partial_credit(self, jd):
        """Unknown experience → 50% of experience weight."""
        match = MatchResult(
            matched_required_skills=["python", "ml", "sql", "nlp"],
            missing_required_skills=[],
            matched_tools=["tensorflow", "pandas", "git"],
            missing_tools=[],
            experience_gap=None,
            education_match=True,
            bonus_points=5,
        )
        result = score_candidate(match, jd)
        assert result.experience_score == 12.5  # 25 * 0.5

    def test_empty_jd_full_credit(self):
        """An empty JD should give full credit everywhere (nothing required)."""
        jd = JobRequirements()
        match = MatchResult()
        result = score_candidate(match, jd)
        # required_skills: 1.0 * 45, tools: 1.0 * 15, exp: 0.5*25, edu: 0, bonus: 0
        assert result.required_skills_score == 45.0
        assert result.tools_score == 15.0
