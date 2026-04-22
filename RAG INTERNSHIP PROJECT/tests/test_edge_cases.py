"""Edge case tests and integration tests."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.config import Settings
from modules.graph import input_node, _calc_confidence


class TestEdgeCases:
    def test_empty_query_handling(self):
        state = {"query": "", "session_id": "t", "retrieved_docs": [], "context": "",
                 "answer": "", "confidence": 0.0, "route": "", "sources": [],
                 "ticket_id": "", "escalation_reason": "", "error": "", "intent": "", "admin_response": ""}
        result = input_node(state)
        assert result["route"] == "error"

    def test_very_long_query(self):
        long_q = "What is the refund policy? " * 500
        state = {"query": long_q, "session_id": "t", "retrieved_docs": [], "context": "",
                 "answer": "", "confidence": 0.0, "route": "", "sources": [],
                 "ticket_id": "", "escalation_reason": "", "error": "", "intent": "", "admin_response": ""}
        result = input_node(state)
        assert result["route"] == "retrieve"  # Should still process

    def test_special_characters_in_query(self):
        state = {"query": "What about <script>alert('xss')</script>?", "session_id": "t",
                 "retrieved_docs": [], "context": "", "answer": "", "confidence": 0.0,
                 "route": "", "sources": [], "ticket_id": "", "escalation_reason": "",
                 "error": "", "intent": "", "admin_response": ""}
        result = input_node(state)
        assert result["route"] == "retrieve"

    def test_confidence_with_empty_scores(self):
        assert _calc_confidence("q", "", "a", [{"score": 0}]) == 0.025


class TestConfigValidation:
    def test_missing_api_key(self):
        original = os.environ.get("GROQ_API_KEY", "")
        os.environ["GROQ_API_KEY"] = ""
        # Force reload of the class attribute
        Settings.GROQ_API_KEY = ""
        errors = Settings.validate()
        assert len(errors) > 0
        os.environ["GROQ_API_KEY"] = original
        Settings.GROQ_API_KEY = original

    def test_valid_config(self):
        os.environ["GROQ_API_KEY"] = "test_key"
        Settings.GROQ_API_KEY = "test_key"
        errors = Settings.validate()
        assert len(errors) == 0
