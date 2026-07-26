import os
from PyPDF2 import PdfReader
from docx import Document


def extract_pdf(file_path):
    """Extract text from PDF."""
    text = ""

    try:
        reader = PdfReader(file_path)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print("PDF Error:", e)

    return text


def extract_docx(file_path):
    """Extract text from DOCX."""
    text = ""

    try:
        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        print("DOCX Error:", e)

    return text


def extract_text(file_path):
    """
    Detect file type and extract text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    elif extension == ".docx":
        return extract_docx(file_path)

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")