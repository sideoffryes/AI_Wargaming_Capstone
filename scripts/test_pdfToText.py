import pytest
from pdfToText import pdf_to_text
from reportlab.pdfgen import canvas

@pytest.fixture
def create_temp_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "This is a test PDF.")
    c.save()
    return pdf_path

def test_pdf_to_text(create_temp_pdf, tmp_path):
    pdf_path = create_temp_pdf
    output_txt = tmp_path / "output.txt"

    # Call the function
    pdf_to_text(pdf_path, output_txt)

    # Verify the output
    with open(output_txt, "r", encoding="utf-8") as f:
        text = f.read()
        assert "This is a test PDF." in text