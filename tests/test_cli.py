import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock
from doc_distill.cli import app
from pathlib import Path

runner = CliRunner()

@pytest.fixture
def mock_converter(mocker):
    return mocker.patch("doc_distill.cli.PDFConverter")

@pytest.fixture
def mock_compressor(mocker):
    return mocker.patch("doc_distill.cli.PromptCompressor")

def test_convert_file_success(mock_converter, tmp_path):
    # Create a dummy PDF file
    pdf_file = tmp_path / "test.pdf"
    pdf_file.touch()

    # Mock converter instance
    mock_instance = mock_converter.return_value
    mock_instance.to_markdown.return_value = "# Markdown Content"

    result = runner.invoke(app, ["convert", str(pdf_file)])
    
    assert result.exit_code == 0
    assert "Processing test.pdf" in result.stdout
    assert "Saved:" in result.stdout
    
    expected_md = tmp_path / "test.md"
    assert expected_md.exists()
    assert expected_md.read_text(encoding="utf-8") == "# Markdown Content"

def test_convert_file_not_found():
    result = runner.invoke(app, ["convert", "non_existent.pdf"])
    assert result.exit_code == 1
    # Rich console might wrap text, so check for key parts
    assert "Error" in result.stdout
    assert "does" in result.stdout
    assert "not exist" in result.stdout.replace("\n", " ")

def test_convert_not_pdf(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.touch()
    
    result = runner.invoke(app, ["convert", str(txt_file)])
    assert result.exit_code == 1
    assert "Error" in result.stdout
    assert "File is not a PDF" in result.stdout.replace("\n", " ")

def test_convert_with_compression(mock_converter, mock_compressor, tmp_path):
    pdf_file = tmp_path / "test.pdf"
    pdf_file.touch()

    mock_conv_instance = mock_converter.return_value
    mock_conv_instance.to_markdown.return_value = "Original Content"
    
    mock_comp_instance = mock_compressor.return_value
    mock_comp_instance.compress.return_value = "Compressed Content"

    result = runner.invoke(app, ["convert", str(pdf_file), "--compress"])
    
    assert result.exit_code == 0
    assert "Compressed:" in result.stdout
    
    expected_comp = tmp_path / "test_compressed.md"
    assert expected_comp.exists()
    assert expected_comp.read_text(encoding="utf-8") == "Compressed Content"

def test_convert_directory(mock_converter, tmp_path):
    # Create dir with 2 PDFs
    d = tmp_path / "pdfs"
    d.mkdir()
    (d / "p1.pdf").touch()
    (d / "p2.pdf").touch()
    
    mock_instance = mock_converter.return_value
    mock_instance.to_markdown.return_value = "Content"

    result = runner.invoke(app, ["convert", str(d)])
    
    assert result.exit_code == 0
    assert "Processing p1.pdf" in result.stdout
    assert "Processing p2.pdf" in result.stdout
