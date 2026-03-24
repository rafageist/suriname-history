from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

teacher_text = extract_text_from_pdf("suriname-history-teacher-guide.pdf")

print("=== Tabla de Contenido PDF Profesor ===")
# La tabla de contenidos está en las primeras páginas
for p in range(1, 8):
    print(f"\n--- Página {p} ---")
    print(teacher_text[p][:1500])