import pdfplumber
from PyPDF2 import PdfReader
from io import BytesIO
import re

def extract_text_pdfplumber(byte_content: bytes):
    try:
        with pdfplumber.open(BytesIO(byte_content)) as pdf:
            return "\n".join([(p.extract_text() or "") for p in pdf.pages])
    except:
        return ""

def extract_text_pypdf2(byte_content: bytes):
    try:
        reader = PdfReader(BytesIO(byte_content))
        return "\n".join([(p.extract_text() or "") for p in reader.pages])
    except:
        return ""

def clean_text(text: str):
    text = text.replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()

def read_resume(file):
    try:
        raw = file.read()
        if file.name.endswith(".pdf"):
            text = extract_text_pdfplumber(raw)
            if len(text) < 30:
                text = extract_text_pypdf2(raw)
            return clean_text(text)
        else:
            return clean_text(raw.decode("utf-8", errors="ignore"))
    except:
        return ""
