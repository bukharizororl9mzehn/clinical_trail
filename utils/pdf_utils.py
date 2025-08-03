import pdfplumber

def extract_text_from_pdf(file) -> str:
    all_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() or ""
    return all_text
