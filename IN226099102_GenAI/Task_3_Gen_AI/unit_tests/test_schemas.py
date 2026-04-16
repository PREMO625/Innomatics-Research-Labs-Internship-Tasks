"""
Unit tests for utils.schemas — Pydantic model validation.
"""

import pytest
from utils.schemas import (
    ResumeProfile,
    JobRequirements,
    MatchResult,
    ScoreResult,
    CandidateEvaluation,
)


class TestResumeProfile:
    """Tests for the ResumeProfile schema."""

    def test_default_values(self):
        """All fields should have safe defaults."""
        profile = ResumeProfile()
        assert profile.name is None
        assert profile.skills == []
        assert profile.tools == []
        assert profile.years_experience is None
        assert profile.education == []
        assert profile.projects == []
        assert profile.certifications == []
        assert profile.domains == []

    def test_full_construction(self):
        """A fully populated profile should validate without errors."""
        profile = ResumeProfile(
            name="Jane Doe",
            skills=["Python", "Machine Learning"],
            tools=["TensorFlow", "Git"],
            years_experience=5.0,
            education=["Master's in CS"],
            projects=["Fraud Detection System"],
            certifications=["AWS ML Specialty"],
            domains=["Finance"],
        )
        assert profile.name == "Jane Doe"
        assert len(profile.skills) == 2
        assert profile.years_experience == 5.0

    def test_serialization_roundtrip(self):
        """model_dump() and re-construction should produce identical objects."""
        original = ResumeProfile(name="Test", skills=["SQL"])
        data = original.model_dump()
        rebuilt = ResumeProfile(**data)
        assert original == rebuilt


class TestJobRequirements:
    """Tests for the JobRequirements schema."""

    def test_default_values(self):
        jd = JobRequirements()
        assert jd.role_title is None
        assert jd.required_skills == []
        assert jd.min_years_experience is None

    def test_full_construction(self):
        jd = JobRequirements(
            role_title="Data Scientist",
            required_skills=["Python", "SQL"],
            preferred_skills=["Spark"],
            tools=["Jupyter"],
            min_years_experience=3,
            education_requirements=["Master's"],
        )
        assert jd.role_title == "Data Scientist"
        assert len(jd.required_skills) == 2


class TestMatchResult:
    """Tests for MatchResult defaults and construction."""

    def test_defaults(self):
        m = MatchResult()
        assert m.matched_required_skills == []
        assert m.experience_gap is None
        assert m.education_match is False
        assert m.bonus_points == 0


class TestScoreResult:
    """Tests for ScoreResult defaults and label."""

    def test_defaults(self):
        s = ScoreResult()
        assert s.total_score == 0.0
        assert s.label == "Weak Fit"


class TestCandidateEvaluation:
    """Tests for the top-level evaluation model."""

    def test_defaults(self):
        ev = CandidateEvaluation()
        assert ev.name == "Unknown"
        assert ev.explanation == ""
        assert ev.score_result.total_score == 0.0
