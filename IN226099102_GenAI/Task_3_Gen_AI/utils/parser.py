"""
PDF text extraction utilities.

Uses pdfplumber (primary) with pypdf fallback, as recommended in doc.md.
Handles corrupt, empty, and scanned-image PDFs gracefully.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract text from a PDF file.

    Strategy:
        1. Try pdfplumber first (better for tables / structured layouts).
        2. Fall back to pypdf if pdfplumber returns empty text.
        3. Return an error message string if both fail.

    Args:
        file_path: Absolute path to the PDF file.

    Returns:
        A string of extracted text, or an error message prefixed with '[ERROR]'.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return f"[ERROR] File not found: {file_path.name}"

    if not file_path.suffix.lower() == ".pdf":
        return f"[ERROR] Not a PDF file: {file_path.name}"

    text = ""

    # -----------------------------------------------------------------------
    # Attempt 1 — pdfplumber (best for complex layouts)
    # -----------------------------------------------------------------------
    try:
        import pdfplumber

        with pdfplumber.open(str(file_path)) as pdf:
            pages: list[str] = []
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
            text = "\n\n".join(pages).strip()
    except Exception as exc:
        logger.warning("pdfplumber failed for %s: %s", file_path.name, exc)

    # -----------------------------------------------------------------------
    # Attempt 2 — pypdf fallback
    # -----------------------------------------------------------------------
    if not text:
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(file_path))
            pages = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
            text = "\n\n".join(pages).strip()
        except Exception as exc:
            logger.error("pypdf also failed for %s: %s", file_path.name, exc)
            return f"[ERROR] Could not read PDF: {file_path.name} — {exc}"

    if not text:
        return (
            f"[ERROR] No readable text in {file_path.name}. "
            "The PDF may be scanned or image-only."
        )

    return text


def extract_texts_from_pdfs(
    file_paths: List[str | Path],
) -> List[Tuple[str, str]]:
    """
    Batch extract text from multiple PDF files.

    Args:
        file_paths: List of absolute paths.

    Returns:
        List of (filename, extracted_text) tuples.
    """
    results: List[Tuple[str, str]] = []
    for fp in file_paths:
        fp = Path(fp)
        text = extract_text_from_pdf(fp)
        results.append((fp.stem, text))
    return results
