from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

student_text = extract_text_from_pdf("suriname-history.pdf")

print("=== Estructura del PDF Estudiante (primeras líneas de cada página) ===\n")
for page_num in range(1, 105):
    content = student_text.get(page_num, "")
    lines = content.strip().split('\n')[:5]
    print(f"Pag {page_num}: {lines[:3]}")