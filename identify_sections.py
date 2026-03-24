from PyPDF2 import PdfReader
import re
import os
from collections import defaultdict

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

def identify_sections(text_dict):
    """Identifica las secciones/temas/lecciones del PDF."""
    sections = []
    current_theme = None
    
    for page_num, content in sorted(text_dict.items()):
        if not content:
            continue
        
        # Buscar Tema
        theme_match = re.search(r'Thema\s*(\d+)\s*[-–]\s*([^\n]+)', content)
        if theme_match:
            current_theme = {
                'num': theme_match.group(1),
                'title': theme_match.group(2).strip()[:80]
            }
        
        # Buscar Les
        les_match = re.search(r'Les\s*(\d+)\s+([^\n]+)', content)
        if les_match and current_theme:
            sections.append({
                'page': page_num,
                'theme_num': current_theme['num'],
                'theme_title': current_theme['title'],
                'lesson_num': les_match.group(1),
                'lesson_title': les_match.group(2).strip()
            })
    
    return sections

def extract_pages_between_lessons(text_dict, start_page, end_page):
    """Extrae el contenido de páginas en un rango."""
    content = []
    for p in range(start_page, end_page + 1):
        if p in text_dict and text_dict[p]:
            content.append(text_dict[p])
    return content

# Cargar PDFs
print("Cargando PDFs...")
student_text = extract_text_from_pdf("suriname-history.pdf")
teacher_text = extract_text_from_pdf("suriname-history-teacher-guide.pdf")

print(f"PDF estudiante: {len(student_text)} páginas")
print(f"PDF profesor: {len(teacher_text)} páginas")

# Identificar lecciones
sections = identify_sections(student_text)
print(f"\n{len(sections)} lecciones identificadas:")

for s in sections:
    print(f"  Tema {s['theme_num']}: Lección {s['lesson_num']} - {s['lesson_title'][:50]}")

# Guardar estructura para siguiente script
import json
with open("structure.json", "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False)

print("\nEstructura guardada en structure.json")