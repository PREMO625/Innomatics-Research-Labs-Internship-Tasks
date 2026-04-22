"""Tests for the database module."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import db


class TestSettings:
    def test_default_settings_initialized(self):
        s = db.get_all_settings()
        assert "confidence_threshold" in s
        assert "top_k" in s
        assert "escalation_enabled" in s

    def test_update_setting(self):
        db.update_setting("confidence_threshold", "0.5")
        assert db.get_setting("confidence_threshold") == "0.5"

    def test_get_nonexistent_setting(self):
        assert db.get_setting("nonexistent", "default") == "default"


class TestTickets:
    def test_create_ticket(self):
        tid = db.create_ticket("sess1", "Help me")
        assert tid.startswith("TKT-")
        ticket = db.get_ticket(tid)
        assert ticket is not None
        assert ticket["query"] == "Help me"
        assert ticket["status"] == "open"

    def test_respond_to_ticket(self):
        tid = db.create_ticket("sess1", "Need help")
        db.respond_to_ticket(tid, "Here's your answer")
        ticket = db.get_ticket(tid)
        assert ticket["status"] == "resolved"
        assert ticket["admin_response"] == "Here's your answer"

    def test_get_all_tickets(self):
        db.create_ticket("s1", "q1")
        db.create_ticket("s2", "q2")
        tickets = db.get_all_tickets()
        assert len(tickets) >= 2

    def test_get_tickets_by_status(self):
        tid = db.create_ticket("s1", "q1")
        db.respond_to_ticket(tid, "done")
        db.create_ticket("s2", "q2")
        open_t = db.get_all_tickets("open")
        resolved_t = db.get_all_tickets("resolved")
        assert len(open_t) >= 1
        assert len(resolved_t) >= 1

    def test_get_nonexistent_ticket(self):
        assert db.get_ticket("FAKE-123") is None


class TestDocuments:
    def test_register_document(self):
        did = db.register_document("test.pdf", "/path/test.pdf", 1024, 5, 20)
        assert did.startswith("DOC-")
        docs = db.get_all_documents()
        assert any(d["id"] == did for d in docs)

    def test_clear_all_documents(self):
        db.register_document("a.pdf", "/a.pdf")
        db.register_document("b.pdf", "/b.pdf")
        db.clear_all_documents()
        assert len(db.get_all_documents()) == 0


class TestSessions:
    def test_create_session(self):
        sid = db.create_session()
        assert len(sid) == 12

    def test_save_and_get_messages(self):
        sid = db.create_session()
        msgs = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
        db.save_session_messages(sid, msgs)
        loaded = db.get_session_messages(sid)
        assert len(loaded) == 2
        assert loaded[0]["content"] == "hi"

    def test_get_messages_unknown_session(self):
        assert db.get_session_messages("nonexistent") == []
