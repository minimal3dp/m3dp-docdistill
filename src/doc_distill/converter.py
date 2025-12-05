import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from typing import Optional

class PDFConverter:
    """
    Handles the conversion of PDF files to raw text/markdown.
    
    This class provides functionality to extract text from PDF documents.
    It supports both direct text extraction and Optical Character Recognition (OCR)
    for scanned documents or pages with minimal selectable text.
    """

    def __init__(self, ocr_enabled: bool = False):
        """
        Initialize the PDFConverter.

        Args:
            ocr_enabled (bool): If True, enables OCR fallback for pages with low text content.
                                Defaults to False.
        """
        self.ocr_enabled = ocr_enabled

    def to_markdown(self, file_path: str) -> str:
        """
        Converts a single PDF file to a Markdown string.
        
        Iterates through each page of the PDF. If OCR is enabled and the page
        contains very little text (suggesting it might be an image/scan),
        OCR is performed. Otherwise, standard text extraction is used.
        
        Args:
            file_path (str): The absolute or relative path to the PDF file.
            
        Returns:
            str: A string containing the extracted content formatted as Markdown,
                 with page headers (e.g., "## Page 1").
        """
        doc = fitz.open(file_path)
        markdown_output = []

        for page_num, page in enumerate(doc):
            # 1. Try standard text extraction first
            text = page.get_text()
            
            # 2. Logic: If page has very little text and OCR is enabled, try OCR
            if self.ocr_enabled and len(text.strip()) < 50:
                text = self._perform_ocr(page)

            # Add a clear header for page separation (useful for LLMs to know context)
            markdown_output.append(f"\n## Page {page_num + 1}\n\n{text}")

        return "\n".join(markdown_output)

    def _perform_ocr(self, page) -> str:
        """
        Renders the PDF page as an image and runs Tesseract OCR.
        
        This method is used as a fallback when direct text extraction yields insufficient results.
        It renders the page at 2x zoom for better OCR accuracy.
        
        Args:
            page (fitz.Page): A PyMuPDF Page object.
            
        Returns:
            str: The text extracted from the page image via OCR.
        """
        # Zoom matrix for better OCR quality (2x zoom)
        mat = fitz.Matrix(2, 2) 
        pix = page.get_pixmap(matrix=mat)
        
        # Convert fitz Pixmap to PIL Image
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        # Run OCR
        return pytesseract.image_to_string(image)