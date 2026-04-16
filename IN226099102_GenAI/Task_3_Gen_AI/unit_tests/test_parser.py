"""
Unit tests for utils.parser — PDF text extraction.
"""

import pytest
from pathlib import Path
from utils.parser import extract_text_from_pdf


class TestExtractTextFromPdf:
    """Test the PDF parser's error handling and edge cases."""

    def test_file_not_found(self):
        """Non-existent file should return an error string."""
        result = extract_text_from_pdf("/nonexistent/file.pdf")
        assert result.startswith("[ERROR]")
        assert "not found" in result.lower()

    def test_non_pdf_file(self, tmp_path):
        """A non-PDF file should be rejected."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Hello world")
        result = extract_text_from_pdf(str(txt_file))
        assert result.startswith("[ERROR]")
        assert "not a pdf" in result.lower()

    def test_empty_pdf(self, tmp_path):
        """An empty / zero-byte PDF should trigger a graceful error."""
        empty_pdf = tmp_path / "empty.pdf"
        empty_pdf.write_bytes(b"")
        result = extract_text_from_pdf(str(empty_pdf))
        assert result.startswith("[ERROR]")

    def test_return_type_is_string(self):
        """Return value should always be a string."""
        result = extract_text_from_pdf("anything.pdf")
        assert isinstance(result, str)
