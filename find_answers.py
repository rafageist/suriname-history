from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text() or ""
    return text

teacher_text = extract_text_from_pdf("suriname-history-teacher-guide.pdf")

print("=== Buscando respuestas del profesor ===")
print(f"Página 29 (Tema 1, Lección 1):")
print(teacher_text.get(29, "")[:1000])
print("\n" + "="*50)
print(f"Página 31 (Tema 1, Lección 2):")
print(teacher_text.get(31, "")[:1000])