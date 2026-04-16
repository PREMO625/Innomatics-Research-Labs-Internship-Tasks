"""
Unit tests for chains.matcher — deterministic matching logic.
"""

import pytest
from utils.schemas import ResumeProfile, JobRequirements
from chains.matcher import match_candidate


class TestMatchCandidate:
    """Test the deterministic matching engine."""

    @pytest.fixture
    def sample_jd(self) -> JobRequirements:
        """Shared JD fixture."""
        return JobRequirements(
            role_title="Data Scientist",
            required_skills=["Python", "Machine Learning", "SQL", "NLP"],
            preferred_skills=["MLOps", "Cloud Computing"],
            tools=["TensorFlow", "Pandas", "Git"],
            min_years_experience=3.0,
            education_requirements=["master's"],
        )

    def test_strong_candidate(self, sample_jd):
        """A candidate matching most skills should get high match counts."""
        profile = ResumeProfile(
            name="Strong Candidate",
            skills=["Python", "Machine Learning", "SQL", "NLP", "MLOps"],
            tools=["TensorFlow", "Pandas", "Git"],
            years_experience=5.0,
            education=["Master's in Computer Science"],
            projects=["Fraud Detector", "Chatbot"],
            certifications=["AWS ML Specialty"],
        )
        result = match_candidate(profile, sample_jd)

        assert len(result.matched_required_skills) == 4
        assert len(result.missing_required_skills) == 0
        assert len(result.matched_tools) == 3
        assert result.experience_gap == 2.0
        assert result.education_match is True
        assert result.bonus_points == 3  # 2 projects + 1 cert

    def test_weak_candidate(self, sample_jd):
        """A candidate with few matches should have many missing skills."""
        profile = ResumeProfile(
            name="Weak Candidate",
            skills=["Excel", "PowerPoint"],
            tools=["Microsoft Office"],
            years_experience=1.0,
            education=["Bachelor's in Business"],
        )
        result = match_candidate(profile, sample_jd)

        assert len(result.matched_required_skills) == 0
        assert len(result.missing_required_skills) == 4
        assert result.experience_gap == -2.0
        assert result.education_match is False

    def test_case_insensitive_matching(self, sample_jd):
        """Matching should be case-insensitive."""
        profile = ResumeProfile(
            skills=["python", "MACHINE LEARNING", "sql", "nlp"],
            tools=["tensorflow", "PANDAS", "git"],
        )
        result = match_candidate(profile, sample_jd)

        assert len(result.matched_required_skills) == 4
        assert len(result.matched_tools) == 3

    def test_no_experience_data(self, sample_jd):
        """When experience is unknown, gap should be None."""
        profile = ResumeProfile(skills=["Python"])
        result = match_candidate(profile, sample_jd)
        assert result.experience_gap is None

    def test_empty_jd(self):
        """An empty JD should produce full-credit matches (nothing required)."""
        profile = ResumeProfile(skills=["Python"])
        jd = JobRequirements()
        result = match_candidate(profile, jd)

        assert len(result.missing_required_skills) == 0
        assert result.experience_gap is None
