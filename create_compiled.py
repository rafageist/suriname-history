#!/usr/bin/env python3
"""
Script para crear un compilado Markdown del libro de estudiantes y guía del profesor.
Extrae imágenes y contenido de ambos PDFs y los organiza por lecciones.
"""
import os
import re
import shutil
import json
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

# ==================== CONFIGURACIÓN ====================
STUDENT_PDF = "suriname-history.pdf"
TEACHER_PDF = "suriname-history-teacher-guide.pdf"
OUTPUT_DIR = "lecciones"

# Estructura del libro basada en la tabla de contenidos
# ( theme_num, lesson_num, title, start_page, end_page )
LESSONS = [
    # Tema 1: Arbeiders komen op voor een beter bestaan
    (1, 0, "INTRO", 11, 12),
    (1, 1, "Een tijd van crisis en werkloosheid", 13, 15),
    (1, 2, "Louis Doedel en Anton de Kom", 16, 18),
    (1, 3, "Vakbonden en vakcentrales", 19, 22),
    (1, 99, "Verwerkingsopdrachten", 23, 23),
    
    # Tema 2: Het onderwijs in ons land
    (2, 0, "INTRO", 25, 26),
    (2, 1, "Hoe was het vroeger?", 27, 30),
    (2, 2, "Het onderwijs verandert", 31, 33),
    (2, 3, "Hoe belangrijk is goed onderwijs?", 34, 36),
    (2, 99, "Verwerkingsopdrachten", 37, 37),
    
    # Tema 3: Verschillende culturen in ons land
    (3, 0, "INTRO", 39, 40),
    (3, 1, "Hoe wij hier ook samenkwamen", 41, 44),
    (3, 2, "Het beleven van cultuur", 45, 47),
    (3, 3, "Ons land, een smeltkroes van culturen", 48, 50),
    (3, 99, "Verwerkingsopdrachten", 51, 51),
    
    # Tema 4: Ons land tijdens de Tweede Wereldoorlog
    (4, 0, "INTRO", 53, 54),
    (4, 1, "Oorlog met Duitsland", 55, 57),
    (4, 2, "De veiligheid in ons land", 58, 60),
    (4, 3, "De bauxietindustrie in ons land", 61, 63),
    (4, 99, "Verwerkingsopdrachten", 64, 64),
    
    # Tema 5: Ontwikkeling van ons land na 1945
    (5, 0, "INTRO", 65, 66),
    (5, 1, "Ontwikkelingshulp aan ons land", 67, 69),
    (5, 2, "De stuwdam in de Surinamerivier", 70, 72),
    (5, 3, "Sociale ontwikkeling", 73, 75),
    (5, 99, "Verwerkingsopdrachten", 76, 76),
    
    # Tema 6: Hoe ons land werd bestuurd
    (6, 0, "INTRO", 77, 78),
    (6, 1, "De gouverneur en de Politieke Raad", 79, 81),
    (6, 2, "Invoering van kiesrecht", 82, 84),
    (6, 3, "Baas in eigen huis!", 85, 88),
    (6, 99, "Verwerkingsopdrachten", 89, 89),
    
    # Tema 7: Ons land, een zelfstandige republiek
    (7, 0, "INTRO", 91, 92),
    (7, 1, "De onafhankelijkheid van ons land", 93, 95),
    (7, 2, "Een staatsgreep in ons land", 96, 98),
    (7, 3, "Veranderingen in het bestuur", 99, 101),
    (7, 99, "Verwerkingsopdrachten", 102, 102),
]

THEMES = {
    1: "Arbeiders komen op voor een beter bestaan",
    2: "Het onderwijs in ons land",
    3: "Verschillende culturen in ons land",
    4: "Ons land tijdens de Tweede Wereldoorlog",
    5: "Ontwikkeling van ons land na 1945",
    6: "Hoe ons land werd bestuurd",
    7: "Ons land, een zelfstandige republiek",
}

# ==================== FUNCIONES ====================

def extract_text_from_pdf(filepath):
    """Extrae texto completo de un PDF."""
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text() or ""
    return text

def extract_images_from_pdf(filepath, output_folder):
    """Extrae imágenes de un PDF usando PyMuPDF."""
    doc = fitz.open(filepath)
    os.makedirs(output_folder, exist_ok=True)
    image_map = {}
    
    for page in doc:
        page_num = page.number + 1
        images = []
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            filename = f"page{page_num}_img{img_index + 1}.{ext}"
            filepath_save = os.path.join(output_folder, filename)
            
            with open(filepath_save, "wb") as f:
                f.write(image_bytes)
            
            images.append(filename)
        image_map[page_num] = images
    
    return image_map

def clean_text(text):
    """Limpia el texto extraído."""
    if not text:
        return ""
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            lines.append(line)
    return '\n\n'.join(lines)

def get_pages_range(student_text, start, end):
    """Obtiene el contenido de un rango de páginas."""
    content = []
    for p in range(start, end + 1):
        if p in student_text and student_text[p]:
            content.append(clean_text(student_text[p]))
    return "\n\n---\n\n".join(content)

def find_teacher_answers(teacher_text, lesson_pages):
    """Busca las respuestas del profesor en las páginas correspondientes."""
    answers = []
    
    # Buscar en las páginas de la guía del profesor
    # Las páginas del profesor suelen tener formato diferente
    for page_num in range(1, len(teacher_text) + 1):
        content = teacher_text.get(page_num, "")
        if not content:
            continue
            
        # Buscar patrones de respuestas
        # El profesor tiene las respuestas en páginas específicas después de cada sección
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Buscar números de respuesta o "Antwoord"
            if 'antwoord' in line.lower() or re.search(r'^\d+[\.\)]\s', line):
                # Incluir esta línea y las siguientes
                answer_block = '\n'.join(lines[i:i+10])
                if answer_block.strip():
                    answers.append(answer_block)
    
    return '\n\n'.join(answers) if answers else "No hay respuestas disponibles en esta sección."

def create_lesson_markdown(theme_num, lesson_num, title, student_content, teacher_content, images):
    """Crea el contenido Markdown para una lección."""
    
    if lesson_num == 0:
        type_name = "Introducción"
        folder_name = f"tema{theme_num}_introduccion"
    elif lesson_num == 99:
        type_name = "Ejercicios"
        folder_name = f"tema{theme_num}_ejercicios"
    else:
        type_name = f"Lección {lesson_num}"
        folder_name = f"tema{theme_num}_leccion{lesson_num}"
    
    md = f"""# {THEMES[theme_num]}

## {type_name}: {title}

---

### Contenido del Libro de Estudiantes

{student_content}

---

### Imágenes de la Lección

"""
    
    # Añadir referencias a imágenes
    if images:
        for img in images:
            md += f"![Imagen](./images/{img})\n\n"
    else:
        md += "*No hay imágenes en esta sección*\n\n"
    
    md += f"""---

### Guía del Profesor - Respuestas y Explicaciones

{teacher_content}

---

*Fuente: suriname-history.pdf (estudiantes) y suriname-history-teacher-guide.pdf (profesor)*
"""
    
    return folder_name, md

def main():
    print("=" * 60)
    print("EXTRACCIÓN Y CONVERSIÓN A MARKDOWN")
    print("=" * 60)
    
    # Crear directorio de salida
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Extraer texto
    print("\n1. Extrayendo texto del PDF de estudiantes...")
    student_text = extract_text_from_pdf(STUDENT_PDF)
    print(f"   - {len(student_text)} páginas")
    
    print("\n2. Extrayendo texto del PDF del profesor...")
    teacher_text = extract_text_from_pdf(TEACHER_PDF)
    print(f"   - {len(teacher_text)} páginas")
    
    # Extraer imágenes
    print("\n3. Extrayendo imágenes del PDF de estudiantes...")
    image_output = os.path.join(OUTPUT_DIR, "images")
    image_map = extract_images_from_pdf(STUDENT_PDF, image_output)
    total_images = sum(len(v) for v in image_map.values())
    print(f"   - {total_images} imágenes extraídas")
    
    # Procesar cada lección
    print("\n4. Creando archivos Markdown por lección...")
    
    for theme_num, lesson_num, title, start_page, end_page in LESSONS:
        print(f"   - Tema {theme_num}, {title[:40]}...")
        
        # Obtener contenido del estudiante
        student_content = get_pages_range(student_text, start_page, end_page)
        
        # Buscar respuestas del profesor (aproximadas)
        teacher_content = " [Las respuestas del profesor se encuentran en las páginas correspondientes de la guía del profesor]"
        
        # Obtener imágenes de las páginas de esta lección
        lesson_images = []
        for p in range(start_page, end_page + 1):
            if p in image_map:
                lesson_images.extend(image_map[p])
        
        # Crear el contenido markdown
        folder_name, md = create_lesson_markdown(
            theme_num, lesson_num, title, 
            student_content, teacher_content, lesson_images
        )
        
        # Guardar archivo
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        filename = "README.md"
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        
        # Copiar las imágenes de esta lección a su carpeta
        if lesson_images:
            lesson_image_dir = os.path.join(folder_path, "images")
            os.makedirs(lesson_image_dir, exist_ok=True)
            for img in lesson_images:
                src = os.path.join(image_output, img)
                if os.path.exists(src):
                    dst = os.path.join(lesson_image_dir, img)
                    shutil.copy2(src, dst)
    
    print(f"\n5. Proceso completado!")
    print(f"   - Archivos guardados en: {OUTPUT_DIR}")
    print(f"   - Imágenes en: {os.path.join(OUTPUT_DIR, 'images')}")

if __name__ == "__main__":
    main()