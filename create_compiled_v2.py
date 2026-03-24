#!/usr/bin/env python3
"""
Script mejorado para crear un compilado Markdown del libro de estudiantes y guía del profesor.
Incluye las respuestas del profesor en cada lección.
"""
import os
import re
import shutil
from PyPDF2 import PdfReader
import fitz

# ==================== CONFIGURACIÓN ====================
STUDENT_PDF = "suriname-history.pdf"
TEACHER_PDF = "suriname-history-teacher-guide.pdf"
OUTPUT_DIR = "lecciones"

# Mapeo directa de lección a página de respuestas del profesor
# (theme_num, lesson_num, title, start_student, end_student, answer_page)
LESSONS = [
    # Tema 1
    (1, 1, "Een tijd van crisis en werkloosheid", 13, 15, 29),
    (1, 2, "Louis Doedel en Anton de Kom", 16, 18, 31),
    (1, 3, "Vakbonden en vakcentrales", 19, 22, 33),
    
    # Tema 2
    (2, 1, "Hoe was het vroeger?", 27, 30, 44),
    (2, 2, "Het onderwijs verandert", 31, 33, 46),
    (2, 3, "Hoe belangrijk is goed onderwijs?", 34, 36, 48),
    
    # Tema 3
    (3, 1, "Hoe wij hier ook samenkwamen", 41, 44, 57),
    (3, 2, "Het beleven van cultuur", 45, 47, 59),
    (3, 3, "Ons land, een smeltkroes van culturen", 48, 50, 61),
    
    # Tema 4
    (4, 1, "Oorlog met Duitsland", 55, 57, 76),
    (4, 2, "De veiligheid in ons land", 58, 60, 78),
    (4, 3, "De bauxietindustrie in ons land", 61, 63, 80),
    
    # Tema 5
    (5, 1, "Ontwikkelingshulp aan ons land", 67, 69, 91),
    (5, 2, "De stuwdam in de Surinamerivier", 70, 72, 93),
    (5, 3, "Sociale ontwikkeling", 73, 75, 95),
    
    # Tema 6
    (6, 1, "De gouverneur en de Politieke Raad", 79, 81, 106),
    (6, 2, "Invoering van kiesrecht", 82, 84, 108),
    (6, 3, "Baas in eigen huis!", 85, 88, 110),
    
    # Tema 7
    (7, 1, "De onafhankelijkheid van ons land", 93, 95, 120),
    (7, 2, "Een staatsgreep in ons land", 96, 98, 122),
    (7, 3, "Veranderingen in het bestuur", 99, 101, 124),
]

# Páginas de introducciones (temas)
INTROS = {
    1: (11, 12),
    2: (25, 26),
    3: (39, 40),
    4: (53, 54),
    5: (65, 66),
    6: (77, 78),
    7: (91, 92),
}

# Páginas de ejercicios
EXERCISES = {
    1: (23, 23),
    2: (37, 37),
    3: (51, 51),
    4: (64, 64),
    5: (76, 76),
    6: (89, 89),
    7: (102, 102),
}

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
    reader = PdfReader(filepath)
    text = {}
    for i, page in enumerate(reader.pages):
        text[i + 1] = page.extract_text() or ""
    return text

def extract_images_from_pdf(filepath, output_folder):
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

def get_pages_range(text_dict, start, end):
    content = []
    for p in range(start, end + 1):
        if p in text_dict and text_dict[p]:
            content.append(clean_text(text_dict[p]))
    return "\n\n---\n\n".join(content)

def create_markdown(theme_num, lesson_type, title, student_content, teacher_content, images):
    """Crea el contenido Markdown."""
    
    if lesson_type == "intro":
        type_name = "Introducción"
        folder_name = f"tema{theme_num}_introduccion"
    elif lesson_type == "exercise":
        type_name = "Ejercicios"
        folder_name = f"tema{theme_num}_ejercicios"
    else:
        type_name = f"Lección {lesson_type}"
        folder_name = f"tema{theme_num}_leccion{lesson_type}"
    
    md = f"""# {THEMES[theme_num]}

## {type_name}: {title}

---

### Contenido del Libro de Estudiantes

{student_content}

---

### Imágenes de la Lección

"""
    
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
    print("CREANDO COMPILADO MARKDOWN COMPLETO")
    print("=" * 60)
    
    # Crear directorio de salida
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Extraer texto
    print("\n1. Extrayendo texto...")
    student_text = extract_text_from_pdf(STUDENT_PDF)
    teacher_text = extract_text_from_pdf(TEACHER_PDF)
    print(f"   - Estudiante: {len(student_text)} páginas")
    print(f"   - Profesor: {len(teacher_text)} páginas")
    
    # Extraer imágenes
    print("\n2. Extrayendo imágenes...")
    image_output = os.path.join(OUTPUT_DIR, "images")
    image_map = extract_images_from_pdf(STUDENT_PDF, image_output)
    total_images = sum(len(v) for v in image_map.values())
    print(f"   - {total_images} imágenes extraídas")
    
    # Crear lecciones
    print("\n3. Creando lecciones...")
    for theme_num, lesson_num, title, start, end, answer_page in LESSONS:
        print(f"   - Tema {theme_num}, Lección {lesson_num}: {title[:35]}...")
        
        # Contenido estudiante
        student_content = get_pages_range(student_text, start, end)
        
        # Contenido profesor (respuestas)
        teacher_content = get_pages_range(teacher_text, answer_page, answer_page + 1)
        
        # Imágenes
        lesson_images = []
        for p in range(start, end + 1):
            if p in image_map:
                lesson_images.extend(image_map[p])
        
        folder_name, md = create_markdown(
            theme_num, lesson_num, title,
            student_content, teacher_content, lesson_images
        )
        
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        filepath = os.path.join(folder_path, "README.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        
        # Copiar imágenes a la carpeta de la lección
        if lesson_images:
            lesson_image_dir = os.path.join(folder_path, "images")
            os.makedirs(lesson_image_dir, exist_ok=True)
            for img in lesson_images:
                src = os.path.join(image_output, img)
                if os.path.exists(src):
                    dst = os.path.join(lesson_image_dir, img)
                    shutil.copy2(src, dst)
    
    # Ejercicios
    print("\n4. Creando ejercicios...")
    for theme_num in range(1, 8):
        start, end = EXERCISES[theme_num]
        print(f"   - Tema {theme_num}: Ejercicios")
        
        student_content = get_pages_range(student_text, start, end)
        teacher_content = "Ejercicios de práctica para el tema."
        
        folder_name, md = create_markdown(
            theme_num, "exercise", f"Ejercicios - {THEMES[theme_num]}",
            student_content, teacher_content, []
        )
        
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        filepath = os.path.join(folder_path, "README.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
    
    print(f"\n5. ¡Completado!")
    print(f"   - Carpeta: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()