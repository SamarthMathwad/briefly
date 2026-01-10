# src/pdf_utils.py

import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    Returns concatenated text of all pages.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text("text")
            text += page_text + "\n"
    return text
