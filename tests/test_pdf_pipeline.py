import os
import sys
import base64
import json

import pytest

# Allow imports from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

fitz = pytest.importorskip("fitz")

import pdf_pipeline

SAMPLE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWP4////fwAJ+wP7gfKTDwAAAABJRU5ErkJggg=="
)


@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    rect1 = fitz.Rect(0, 0, 50, 50)
    page.insert_image(rect1, stream=SAMPLE_PNG)
    rect2 = fitz.Rect(60, 0, 110, 50)
    page.insert_image(rect2, stream=SAMPLE_PNG)
    text = "Para one.\n\nPara two.\n\nPara three.\n\nPara four."
    page.insert_textbox(fitz.Rect(0, 60, 200, 200), text)
    doc.save(pdf_path)
    return pdf_path


def test_extract_content(sample_pdf, tmp_path):
    content = pdf_pipeline.extract_content(str(sample_pdf), str(tmp_path))
    assert len(content.images) == 2
    assert len(content.paragraphs) >= 4
    for img in content.images:
        assert os.path.exists(img)
