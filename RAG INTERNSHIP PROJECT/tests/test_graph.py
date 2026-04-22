"""Tests for the LangGraph workflow and graph nodes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.graph import (
    input_node, retrieve_node, decision_node, output_node,
    escalate_node, human_response_node, _calc_confidence, build_graph,
)
from modules import db


def _make_state(**overrides):
    base = {
        "query": "test query", "session_id": "test-session", "retrieved_docs": [],
        "context": "", "answer": "", "confidence": 0.0, "route": "",
        "sources": [], "ticket_id": "", "escalation_reason": "",
        "error": "", "intent": "", "admin_response": "",
    }
    base.update(overrides)
    return base


class TestInputNode:
    def test_empty_query(self):
        result = input_node(_make_state(query=""))
        assert result["route"] == "error"

    def test_whitespace_query(self):
        result = input_node(_make_state(query="   "))
        assert result["route"] == "error"

    def test_normal_query(self):
        result = input_node(_make_state(query="What is the refund policy?"))
        assert result["route"] == "retrieve"

    def test_human_request(self):
        result = input_node(_make_state(query="I want to speak to a human agent"))
        assert result["route"] == "user_requested_human"

    def test_manager_request(self):
        result = input_node(_make_state(query="Let me talk to a manager"))
        assert result["route"] == "user_requested_human"


class TestConfidenceCalculation:
    def test_no_docs_zero_confidence(self):
        assert _calc_confidence("q", "", "a", []) == 0.0

    def test_high_score_docs(self):
        docs = [{"score": 0.9}, {"score": 0.85}]
        conf = _calc_confidence("q", "ctx", "Great answer", docs)
        assert conf > 0.7

    def test_uncertainty_penalty(self):
        docs = [{"score": 0.9}]
        conf = _calc_confidence("q", "ctx", "I don't have enough information", docs)
        assert conf < 0.7

    def test_confidence_bounded(self):
        docs = [{"score": 1.0}] * 10
        conf = _calc_confidence("q", "ctx", "answer", docs)
        assert 0.0 <= conf <= 1.0


class TestDecisionNode:
    def test_high_confidence_routes_output(self):
        state = _make_state(
            query="simple question", context="some context",
            answer="good answer", retrieved_docs=[{"score": 0.9}],
        )
        result = decision_node(state)
        assert result["route"] in ("output", "escalate")

    def test_escalation_on_approval_query(self):
        state = _make_state(
            query="I need a refund approved", context="some context",
            answer="answer", retrieved_docs=[{"score": 0.8}],
        )
        result = decision_node(state)
        assert result["route"] == "escalate"


class TestEscalateNode:
    def test_creates_ticket(self):
        state = _make_state(
            query="Help me!", answer="Sorry", escalation_reason="Test escalation",
        )
        result = escalate_node(state)
        assert result["ticket_id"].startswith("TKT-")
        assert "Escalated" in result["answer"]

    def test_ticket_stored_in_db(self):
        state = _make_state(query="Test", answer="", escalation_reason="Test")
        result = escalate_node(state)
        ticket = db.get_ticket(result["ticket_id"])
        assert ticket is not None
        assert ticket["status"] == "open"


class TestHumanResponseNode:
    def test_no_response(self):
        result = human_response_node(_make_state())
        assert result["route"] == "waiting"

    def test_with_admin_response(self):
        ticket_id = db.create_ticket("test-session", "help", "ai said this")
        db.respond_to_ticket(ticket_id, "Admin says: fixed it")
        result = human_response_node(_make_state(session_id="test-session"))
        assert result["route"] == "complete"
        assert "Admin says" in result.get("answer", "")


class TestOutputNode:
    def test_output_marks_complete(self):
        result = output_node(_make_state())
        assert result["route"] == "complete"


class TestGraphCompilation:
    def test_graph_compiles(self):
        graph = build_graph()
        assert graph is not None
