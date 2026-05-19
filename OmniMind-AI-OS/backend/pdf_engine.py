from pypdf import PdfReader
import tempfile
import os
from backend.ai_engine import ask_ai

def process_pdf(pdf_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_content)
        tmp_path = tmp.name

    try:
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
                
        prompt = f"Summarize this document:\n\n{text[:5000]}"
        return ask_ai(prompt)
    finally:
        os.unlink(tmp_path)
