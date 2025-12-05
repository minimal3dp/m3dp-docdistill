Doc-Distill

Doc-Distill is a lightweight tool to convert PDF documents into Markdown, with a specialized "Compression" feature designed to optimize text for Large Language Model (LLM) prompts.

It can be used as a standalone CLI tool or imported as a Python library.

Features

Bulk Processing: Convert a single file or a whole directory.

Prompt Compression: Algorithmic reduction of tokens (removing stop words, punctuation, whitespace) based on semantic compression principles. Inspired by [this FreeCodeCamp article](https://www.freecodecamp.org/news/how-to-compress-your-prompts-and-reduce-llm-costs/).

Hybrid Extraction: Uses direct text extraction for speed, with optional OCR (Tesseract) fallback for scanned pages.

Modern Stack: Built with Python 3.10+, uv, and typer.

Installation

Prerequisites

Python 3.10+

Tesseract OCR (Optional, only for OCR support):

Mac: brew install tesseract

Ubuntu: sudo apt-get install tesseract-ocr

Windows: Download the Tesseract installer.

Using UV (Recommended)

# Clone the repo
git clone [https://github.com/yourusername/doc-distill.git](https://github.com/yourusername/doc-distill.git)
cd doc-distill

# Create virtualenv and install dependencies
uv sync

# Run the tool
uv run doc-distill --help


CLI Usage

1. Basic Conversion (PDF -> MD)

uv run doc-distill convert ./my_document.pdf


Output: my_document.md

2. Conversion with Compression

uv run doc-distill convert ./my_document.pdf --compress


Output: my_document.md AND my_document_compressed.md

3. Bulk Processing Directory

uv run doc-distill convert ./papers/ --compress --output ./processed_papers/


4. Enable OCR (Slower, but works on scans)

uv run doc-distill convert ./scanned_doc.pdf --ocr


Library Usage

You can use doc-distill in your own Python projects:

from doc_distill import PDFConverter, PromptCompressor

# 1. Convert PDF
converter = PDFConverter(ocr_enabled=True)
raw_md = converter.to_markdown("manual.pdf")

# 2. Compress for LLM
compressor = PromptCompressor()
optimized_prompt = compressor.compress(raw_md)

print(f"Original length: {len(raw_md)}")
print(f"Compressed length: {len(optimized_prompt)}")


License

MIT