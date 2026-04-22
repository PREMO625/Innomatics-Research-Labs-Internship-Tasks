"""
Shared pytest fixtures for the test suite.
"""
import os
import sys
import pytest
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override settings BEFORE importing modules
os.environ["SQLITE_PATH"] = os.path.join(tempfile.gettempdir(), "test_support.db")
os.environ["CHROMA_DIR"] = os.path.join(tempfile.gettempdir(), "test_chroma_db")
os.environ["UPLOAD_DIR"] = os.path.join(tempfile.gettempdir(), "test_uploads")
# Set a dummy key if not present to allow module import
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = "test_key_not_real"


@pytest.fixture(autouse=True)
def clean_test_db():
    """Clean up test database before and after each test."""
    db_path = os.environ["SQLITE_PATH"]
    if os.path.exists(db_path):
        os.remove(db_path)
    from modules.db import init_db
    init_db()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a sample PDF for testing."""
    try:
        from pypdf import PdfWriter
        writer = PdfWriter()
        from pypdf._page import PageObject
        from pypdf.generic import RectangleObject
        import io

        # Create a simple PDF with text
        from reportlab.pdfgen import canvas as rl_canvas
        buf = io.BytesIO()
        c = rl_canvas.Canvas(buf)
        c.drawString(72, 720, "Refund Policy")
        c.drawString(72, 700, "Our refund policy allows returns within 30 days of purchase.")
        c.drawString(72, 680, "To request a refund, contact support with your order number.")
        c.drawString(72, 660, "Refunds are processed within 5-7 business days.")
        c.drawString(72, 640, "Items must be in original condition for a full refund.")
        c.showPage()
        c.drawString(72, 720, "Shipping Information")
        c.drawString(72, 700, "Standard shipping takes 5-7 business days.")
        c.drawString(72, 680, "Express shipping is available for 2-3 day delivery.")
        c.drawString(72, 660, "Free shipping on orders over $50.")
        c.showPage()
        c.save()
        buf.seek(0)

        pdf_path = str(tmp_path / "test_refund_policy.pdf")
        with open(pdf_path, "wb") as f:
            f.write(buf.read())
        return pdf_path
    except ImportError:
        # Fallback: create a minimal PDF without reportlab
        pdf_path = str(tmp_path / "test_refund_policy.pdf")
        _create_minimal_pdf(pdf_path)
        return pdf_path


@pytest.fixture
def invalid_pdf(tmp_path):
    """Create an invalid/corrupt PDF file for testing."""
    pdf_path = str(tmp_path / "corrupt.pdf")
    with open(pdf_path, "w") as f:
        f.write("This is not a valid PDF file content.")
    return pdf_path


@pytest.fixture
def empty_file(tmp_path):
    """Create an empty file."""
    path = str(tmp_path / "empty.pdf")
    with open(path, "wb") as f:
        f.write(b"")
    return path


def _create_minimal_pdf(path: str):
    """Create a minimal valid PDF without external dependencies."""
    content = """%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj

3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj

4 0 obj
<< /Length 168 >>
stream
BT
/F1 12 Tf
72 720 Td
(Refund Policy: Returns accepted within 30 days.) Tj
0 -20 Td
(Standard shipping takes 5-7 business days.) Tj
0 -20 Td
(Free shipping on orders over fifty dollars.) Tj
ET
endstream
endobj

5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000486 00000 n 

trailer
<< /Size 6 /Root 1 0 R >>
startxref
556
%%EOF"""
    with open(path, "w") as f:
        f.write(content)
