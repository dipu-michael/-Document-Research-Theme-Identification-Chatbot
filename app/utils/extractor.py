import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io

def extract_text_from_pdf(file_bytes):
    """
    Extracts text from a PDF using PyMuPDF.
    Falls back to OCR if the document appears scanned.
    """
    text = ""

    try:
        # Try extracting text normally (text-based PDFs)
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()

        # If text is empty, fallback to OCR
        if not text.strip():
            text = extract_text_from_scanned_pdf(file_bytes)

    except Exception as e:
        print("PDF text extraction failed:", e)
        text = extract_text_from_scanned_pdf(file_bytes)

    return text


def extract_text_from_scanned_pdf(file_bytes):
    """
    Uses OCR (Tesseract) to extract text from scanned PDF pages.
    Converts each page to image and applies pytesseract.
    """
    text = ""
    try:
        images = convert_from_bytes(file_bytes)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
    except Exception as e:
        print("OCR failed on scanned PDF:", e)

    return text


def extract_text_from_image(file_bytes):
    """
    Extracts text from image bytes using pytesseract OCR.
    Supports PNG, JPG, JPEG.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
    except Exception as e:
        print("Image OCR failed:", e)
        return ""
