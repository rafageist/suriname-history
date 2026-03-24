import os
import re
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from collections import defaultdict

def extract_text_from_pdf(filepath):
    """Extrae texto completo de un PDF."""
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

def extract_images_from_pdf(filepath, output_base="images"):
    """Extrae imágenes de un PDF usando PyMuPDF."""
    doc = fitz.open(filepath)
    os.makedirs(output_base, exist_ok=True)
    image_map = defaultdict(list)
    
    for page_num in doc:
        page = doc.load_page(page_num.number)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            filename = f"page{page_num.number + 1}_img{img_index + 1}.{ext}"
            filepath_save = os.path.join(output_base, filename)
            
            with open(filepath_save, "wb") as f:
                f.write(image_bytes)
            
            image_map[page_num.number + 1].append(filename)
    
    return dict(image_map)

def find_lesson_starts(text_dict):
    """Encuentra dónde empiezan las lecciones en el texto."""
    lesson_patterns = [
        r'^Les\s*(\d+)',
        r'^Les \d+ ',
        r'Thema \d+',
        r'INLEIDING',
        r'Verwerkingsopdrachten',
        r'Kopieerblad',
        r'KWARTAAL',
    ]
    
    lessons = []
    current_theme = None
    current_lesson = None
    
    for page_num, content in sorted(text_dict.items()):
        if not content:
            continue
            
        lines = content.strip().split('\n')
        first_line = lines[0].strip() if lines else ""
        
        # Detectar tema
        theme_match = re.search(r'Thema\s*(\d+)\s*[-–]\s*(.+?)(?:THEMA|$)', content)
        if theme_match:
            current_theme = (theme_match.group(1), theme_match.group(2).strip())
        
        # Detectar lección
        lesson_match = re.search(r'Les\s*(\d+)\s*(.+?)(?:\n|$)', content)
        if lesson_match:
            current_lesson = (lesson_match.group(1), lesson_match.group(2).strip())
            lessons.append({
                'page': page_num,
                'theme': current_theme,
                'lesson': current_lesson,
                'title': lesson_match.group(2).strip()
            })
    
    return lessons

def main():
    student_pdf = "suriname-history.pdf"
    teacher_pdf = "suriname-history-teacher-guide.pdf"
    output_dir = "lecciones"
    
    print("Extrayendo imágenes del PDF de estudiantes...")
    image_map = extract_images_from_pdf(student_pdf, "images")
    print(f"  - {sum(len(v) for v in image_map.values())} imágenes extraídas")
    
    print("\nExtrayendo texto...")
    student_text = extract_text_from_pdf(student_pdf)
    teacher_text = extract_text_from_pdf(teacher_pdf)
    
    print(f"  - PDF estudiante: {len(student_text)} páginas")
    print(f"  - PDF profesor: {len(teacher_text)} páginas")
    
    # Encontrar lecciones
    lessons = find_lesson_starts(student_text)
    print(f"\nLecciones encontradas: {len(lessons)}")
    for l in lessons:
        print(f"  Tema {l['theme'][0]}: Lección {l['lesson'][0]} - {l['title'][:50]}")
    
    # Guardar info
    print(f"\nImágenes por página: {dict(image_map)}")

if __name__ == "__main__":
    main()