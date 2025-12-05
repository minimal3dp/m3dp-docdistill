# Doc-Distill User Guide

Doc-Distill is a powerful, lightweight tool designed to convert PDF documents into Markdown. It features a specialized "Compression" mode that optimizes text for Large Language Model (LLM) prompts by removing non-essential tokens while preserving semantic meaning.

## Table of Contents
- [Installation](#installation)
- [CLI Usage](#cli-usage)
    - [Basic Conversion](#basic-conversion)
    - [Compression Mode](#compression-mode)
    - [Bulk Processing](#bulk-processing)
    - [OCR Support](#ocr-support)
- [Library Usage](#library-usage)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- **Python 3.10+**: Ensure you have a compatible Python version installed.
- **Tesseract OCR** (Optional): Required only if you need to process scanned documents.

#### Installing Tesseract
- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download and install from the [official GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki).

### Installing Doc-Distill
We recommend using `uv` for a fast and reliable setup, but standard `pip` works as well.

#### Using UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/doc-distill.git
cd doc-distill

# Sync dependencies
uv sync

# Run the tool
uv run doc-distill --help
```

#### Using Pip
```bash
pip install .
```

## CLI Usage

The Command Line Interface (CLI) is the primary way to interact with Doc-Distill.

### Basic Conversion
Convert a single PDF to Markdown.

```bash
uv run doc-distill convert ./documents/report.pdf
```
**Output**: Creates `./documents/report.md`.

### Compression Mode
Generate an additional compressed version of the text, optimized for LLM context windows. This removes stop words, punctuation, and excessive whitespace. This technique is inspired by [this FreeCodeCamp article](https://www.freecodecamp.org/news/how-to-compress-your-prompts-and-reduce-llm-costs/).

```bash
uv run doc-distill convert ./documents/report.pdf --compress
```
**Output**: Creates `./documents/report.md` AND `./documents/report_compressed.md`.

### Bulk Processing
You can pass a directory path instead of a file path to process all PDFs within that directory.

```bash
uv run doc-distill convert ./library/ --output ./processed_library/
```

### OCR Support
If your PDFs are scanned images (no selectable text), enable OCR (Optical Character Recognition). This is slower but necessary for image-based PDFs.

```bash
uv run doc-distill convert ./scans/invoice.pdf --ocr
```

## Library Usage

Doc-Distill can be imported and used directly in your Python projects.

### converting a PDF

```python
from doc_distill.converter import PDFConverter

# Initialize converter (enable OCR if needed)
converter = PDFConverter(ocr_enabled=True)

# Convert file
markdown_text = converter.to_markdown("path/to/document.pdf")

print(markdown_text)
```

### Compressing Text for LLMs

```python
from doc_distill.compressor import PromptCompressor

# Initialize compressor
compressor = PromptCompressor()

# Compress text
raw_text = "The quick brown fox jumps over the lazy dog."
optimized_text = compressor.compress(raw_text)

print(optimized_text)
# Output: "quick brown fox jumps lazy dog"
```

## Troubleshooting

### "Tesseract not found" error
Ensure Tesseract is installed and in your system's PATH. You can verify this by running `tesseract --version` in your terminal.

### "No PDFs found"
Double-check the directory path you provided. The tool looks for files ending in `.pdf` (case-insensitive).
