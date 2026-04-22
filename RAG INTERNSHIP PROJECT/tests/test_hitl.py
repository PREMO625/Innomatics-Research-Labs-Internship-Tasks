"""Tests for the HITL escalation module."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.hitl import (
    detect_human_request, detect_approval_needed, detect_frustration,
    should_escalate, create_escalation_ticket, admin_respond,
    get_pending_tickets, get_resolved_tickets, get_admin_response_for_session,
)
from modules import db


class TestEscalationDetection:
    def test_detect_human_request(self):
        assert detect_human_request("I want to speak to a human agent") is True
        assert detect_human_request("Let me talk to a manager") is True
        assert detect_human_request("What is your return policy?") is False

    def test_detect_approval_needed(self):
        assert detect_approval_needed("I need a refund") is True
        assert detect_approval_needed("Cancel my order") is True
        assert detect_approval_needed("How are you?") is False

    def test_detect_frustration(self):
        assert detect_frustration("This is unacceptable!") is True
        assert detect_frustration("I was charged twice") is True
        assert detect_frustration("Thank you for helping") is False


class TestShouldEscalate:
    def test_escalate_on_user_request(self):
        esc, reason = should_escalate("speak to a human", 0.9, 0.7, [{"score": 0.9}])
        assert esc is True
        assert "human agent" in reason.lower()

    def test_escalate_on_low_confidence(self):
        esc, reason = should_escalate("normal query", 0.3, 0.7, [{"score": 0.3}])
        assert esc is True
        assert "confidence" in reason.lower()

    def test_escalate_on_no_context(self):
        esc, reason = should_escalate("random query", 0.0, 0.7, [])
        assert esc is True

    def test_no_escalation_high_confidence(self):
        esc, reason = should_escalate("simple question", 0.9, 0.7, [{"score": 0.9}])
        assert esc is False

    def test_escalation_disabled(self):
        settings_dict = {"escalation_enabled": "false", "escalation_on_user_request": "true"}
        esc, reason = should_escalate("speak to human", 0.1, 0.7, [], settings_dict)
        assert esc is False


class TestTicketLifecycle:
    def test_create_and_respond(self):
        tid = create_escalation_ticket("sess1", "Help!", reason="Test")
        assert tid.startswith("TKT-")
        pending = get_pending_tickets()
        assert any(t["id"] == tid for t in pending)

        admin_respond(tid, "Issue resolved.")
        resolved = get_resolved_tickets()
        assert any(t["id"] == tid for t in resolved)

    def test_admin_response_for_session(self):
        tid = create_escalation_ticket("sess-check", "Problem", reason="Test")
        assert get_admin_response_for_session("sess-check") is None
        admin_respond(tid, "Fixed it!")
        resp = get_admin_response_for_session("sess-check")
        assert resp == "Fixed it!"

    def test_respond_nonexistent_ticket(self):
        result = admin_respond("FAKE-123", "response")
        assert result is False
