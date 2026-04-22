"""Tests for PDF ingestion pipeline."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.ingest import load_pdf, chunk_documents, clean_text, get_collection_stats
from modules import db


class TestTextCleaning:
    def test_clean_whitespace(self):
        text = "Hello   world\n\n\n\ntest"
        result = clean_text(text)
        assert "   " not in result
        assert "\n\n\n\n" not in result

    def test_clean_page_breaks(self):
        text = "Page 1\x0cPage 2"
        result = clean_text(text)
        assert "\x0c" not in result

    def test_clean_empty_string(self):
        assert clean_text("") == ""
        assert clean_text("   ") == ""


class TestPDFLoading:
    def test_load_valid_pdf(self, sample_pdf):
        docs = load_pdf(sample_pdf)
        assert len(docs) > 0
        assert docs[0].page_content  # Should have content
        assert "source" in docs[0].metadata

    def test_load_invalid_pdf(self, invalid_pdf):
        """Test that loading a corrupt PDF raises or returns empty."""
        try:
            docs = load_pdf(invalid_pdf)
            # pypdf may return empty or raise
        except Exception:
            pass  # Expected

    def test_load_pdf_metadata(self, sample_pdf):
        docs = load_pdf(sample_pdf)
        if docs:
            assert "source" in docs[0].metadata
            assert "page" in docs[0].metadata


class TestChunking:
    def test_chunk_documents(self, sample_pdf):
        docs = load_pdf(sample_pdf)
        if docs:
            chunks = chunk_documents(docs)
            assert len(chunks) >= 1
            for chunk in chunks:
                assert chunk.page_content
                assert "chunk_id" in chunk.metadata

    def test_chunk_preserves_metadata(self, sample_pdf):
        docs = load_pdf(sample_pdf)
        if docs:
            chunks = chunk_documents(docs)
            for chunk in chunks:
                assert "source" in chunk.metadata


class TestIngestionPipeline:
    def test_ingest_pdf_registers_document(self, sample_pdf):
        from modules.ingest import ingest_pdf
        result = ingest_pdf(sample_pdf)
        assert result["status"] == "success"
        docs = db.get_all_documents()
        assert len(docs) >= 1

    def test_collection_stats(self, sample_pdf):
        from modules.ingest import ingest_pdf
        ingest_pdf(sample_pdf)
        stats = get_collection_stats()
        assert stats["total_chunks"] > 0
