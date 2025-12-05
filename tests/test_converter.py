import pytest
from unittest.mock import MagicMock, patch
from doc_distill.converter import PDFConverter

@pytest.fixture
def mock_fitz(mocker):
    return mocker.patch("doc_distill.converter.fitz")

@pytest.fixture
def mock_pytesseract(mocker):
    return mocker.patch("doc_distill.converter.pytesseract")

@pytest.fixture
def mock_image(mocker):
    return mocker.patch("doc_distill.converter.Image")

def test_to_markdown_standard(mock_fitz):
    # Setup mock document
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "This is some sample text content."
    mock_doc.__iter__.return_value = [mock_page]
    mock_fitz.open.return_value = mock_doc

    converter = PDFConverter(ocr_enabled=False)
    result = converter.to_markdown("dummy.pdf")

    assert "## Page 1" in result
    assert "This is some sample text content." in result
    mock_fitz.open.assert_called_with("dummy.pdf")

def test_to_markdown_ocr_fallback(mock_fitz, mock_pytesseract, mock_image):
    # Setup mock document with empty text
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "   " # Empty text
    mock_doc.__iter__.return_value = [mock_page]
    mock_fitz.open.return_value = mock_doc

    # Setup OCR return
    mock_pytesseract.image_to_string.return_value = "OCR Extracted Text"
    
    # Setup Image mocking
    mock_pix = MagicMock()
    mock_pix.tobytes.return_value = b"fake_image_data"
    mock_page.get_pixmap.return_value = mock_pix

    converter = PDFConverter(ocr_enabled=True)
    result = converter.to_markdown("scan.pdf")

    assert "## Page 1" in result
    assert "OCR Extracted Text" in result
    mock_pytesseract.image_to_string.assert_called()

def test_ocr_disabled_skips_ocr(mock_fitz, mock_pytesseract):
    # Setup mock document with empty text
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "   "
    mock_doc.__iter__.return_value = [mock_page]
    mock_fitz.open.return_value = mock_doc

    converter = PDFConverter(ocr_enabled=False)
    result = converter.to_markdown("scan.pdf")

    # Should just contain the empty text (or whitespace)
    assert "## Page 1" in result
    mock_pytesseract.image_to_string.assert_not_called()
