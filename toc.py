from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

# Buscar la tabla de contenido en página 3
student_text = extract_text_from_pdf("suriname-history.pdf")
content_page = student_text[3]

print("=== Tabla de Contenido PDF Estudiante ===")
print(content_page)

# También ver página 4
print("\n=== Página 4 ===")
print(student_text[4])