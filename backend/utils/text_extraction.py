import pdfplumber
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_image(image_path):
    """Extracts text from an image using OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def extract_text_from_pdf_with_ocr(pdf_path):
    """Extracts text from a scanned PDF using OCR."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
            else:
                # Convert PDF page to image for OCR
                img = page.to_image()
                img_byte_array = io.BytesIO()
                img.save(img_byte_array, format="PNG")
                text += pytesseract.image_to_string(Image.open(img_byte_array)) + "\n"
    return text.strip()
