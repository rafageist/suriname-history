from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text() or ""
    return text

teacher_text = extract_text_from_pdf("suriname-history-teacher-guide.pdf")

# Pages where answers are (based on table of contents)
answer_pages = list(range(21, 137))

print("=== Buscando TODAS las páginas con VRAGEN EN ANTWOORDEN ===")

for p in answer_pages:
    content = teacher_text.get(p, "")
    if content and "VRAGEN EN ANTWOORDEN" in content:
        print(f"\n*** Página {p} ***")
        # Print first 500 chars
        print(content[:600])
        print("...")