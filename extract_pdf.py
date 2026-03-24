import os
import re
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

def extract_text_from_pdf(filepath):
    """Extrae texto completo de un PDF."""
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text()
    return text

def extract_images_from_pdf(filepath, output_folder):
    """Extrae imágenes de un PDF usando PyMuPDF."""
    doc = fitz.open(filepath)
    image_count = 0
    image_map = {}
    
    os.makedirs(output_folder, exist_ok=True)
    
    for page_num, page in enumerate(doc, start=1):
        page_images = []
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            image_count += 1
            filename = f"page{page_num}_img{image_count}.{ext}"
            filepath = os.path.join(output_folder, filename)
            
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            page_images.append(filename)
        
        image_map[page_num] = page_images
    
    return image_map

def analyze_pdf_structure(text):
    """Analiza la estructura del PDF para identificar lecciones/temario."""
    structure = {}
    
    for page_num, content in text.items():
        if content:
            # Buscar patrones de lecciones/títulos
            lines = content.strip().split('\n')
            first_line = lines[0].strip() if lines else ""
            
            # Buscar números de lección
            lesson_match = re.search(r'(Lección|Leccion|Leção)\s*(\d+)', content, re.IGNORECASE)
            chapter_match = re.search(r'(Capítulo|Capítulo|Chapter)\s*(\d+)', content, re.IGNORECASE)
            
            if lesson_match:
                lesson_num = lesson_match.group(2)
                structure[page_num] = {
                    'type': 'lesson',
                    'number': lesson_num,
                    'title': first_line[:100]
                }
            elif chapter_match:
                chapter_num = chapter_match.group(2)
                structure[page_num] = {
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': first_line[:100]
                }
    
    return structure

def main():
    student_pdf = "suriname-history.pdf"
    teacher_pdf = "suriname-history-teacher-guide.pdf"
    
    print(" Extrayendo texto del PDF de estudiantes...")
    student_text = extract_text_from_pdf(student_pdf)
    print(f"  - {len(student_text)} páginas")
    
    print("\n Extrayendo texto del PDF del profesor...")
    teacher_text = extract_text_from_pdf(teacher_pdf)
    print(f"  - {len(teacher_text)} páginas")
    
    print(f"\nEstructura del PDF estudiante:")
    print(f"  Páginas: {len(student_text)}")
    print(f"  Primera página muestra: {list(student_text.values())[0][:200] if student_text else 'N/A'}...")
    
    print(f"\nEstructura del PDF profesor:")
    print(f"  Páginas: {len(teacher_text)}")
    print(f"  Primera página muestra: {list(teacher_text.values())[0][:200] if teacher_text else 'N/A'}...")
    
    # Guardar texto extraído para análisis
    with open("student_text.txt", "w", encoding="utf-8") as f:
        for pnum, content in student_text.items():
            f.write(f"\n=== Página {pnum} ===\n")
            f.write(content)
    
    with open("teacher_text.txt", "w", encoding="utf-8") as f:
        for pnum, content in teacher_text.items():
            f.write(f"\n=== Página {pnum} ===\n")
            f.write(content)
    
    print("\nTextos extraídos guardados en archivos .txt para análisis")

if __name__ == "__main__":
    main()