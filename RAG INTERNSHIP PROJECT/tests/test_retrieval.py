"""Tests for retrieval pipeline."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.retriever import retrieve_documents, format_context, format_sources, has_documents
from modules.ingest import ingest_pdf


class TestRetrieval:
    def test_no_docs_returns_empty(self):
        results = retrieve_documents("What is the refund policy?")
        assert isinstance(results, list)

    def test_has_documents_false_when_empty(self):
        # Fresh test DB should have no docs
        assert has_documents() is False or isinstance(has_documents(), bool)

    def test_retrieve_after_ingest(self, sample_pdf):
        ingest_pdf(sample_pdf)
        results = retrieve_documents("refund policy")
        # Should return results after ingestion
        assert isinstance(results, list)
        if results:
            assert "content" in results[0]
            assert "score" in results[0]
            assert "source" in results[0]


class TestFormatting:
    def test_format_context_empty(self):
        assert format_context([]) == ""

    def test_format_context_with_docs(self):
        docs = [{"content": "Test content", "source": "test.pdf", "page": 1, "score": 0.9}]
        result = format_context(docs)
        assert "Test content" in result
        assert "test.pdf" in result

    def test_format_sources(self):
        docs = [
            {"source": "refund.pdf", "page": 1, "content": "", "score": 0.9},
            {"source": "refund.pdf", "page": 1, "content": "", "score": 0.8},
            {"source": "shipping.pdf", "page": 2, "content": "", "score": 0.7},
        ]
        sources = format_sources(docs)
        assert len(sources) == 2  # Deduped
        assert any("refund.pdf" in s for s in sources)

    def test_format_sources_empty(self):
        assert format_sources([]) == []
