import os
import re

# Estructura del libro original (basada en el PDF)
ORIGINAL_STRUCTURE = {
    1: {"title": "Intro: Workers Stand Up for a Better Life", "type": "intro"},
    2: {"title": "Lesson 1: A Time of Crisis and Unemployment", "type": "lesson"},
    3: {"title": "Lesson 2: Workers and Unions", "type": "lesson"},
    4: {"title": "Lesson 3: Trade Unions and Trade Union Federations", "type": "lesson"},
    5: {"title": "Practice Exercises", "type": "exercises"},
    6: {"title": "Intro: Education in Our Country", "type": "intro"},
    7: {"title": "Lesson 1: How Was It in the Past", "type": "lesson"},
    8: {"title": "Lesson 2: Education Changes", "type": "lesson"},
    9: {"title": "Lesson 3: How Important Is Good Education", "type": "lesson"},
    10: {"title": "Practice Exercises", "type": "exercises"},
    11: {"title": "Intro: Different Cultures in Our Country", "type": "intro"},
    12: {"title": "Lesson 1: How We Came Together Here", "type": "lesson"},
    13: {"title": "Lesson 2: Experiencing Culture", "type": "lesson"},
    14: {"title": "Lesson 3: Our Country a Melting Pot of Cultures", "type": "lesson"},
    15: {"title": "Practice Exercises", "type": "exercises"},
    16: {"title": "Intro: Our Country During World War II", "type": "intro"},
    17: {"title": "Lesson 1: War with Germany", "type": "lesson"},
    18: {"title": "Lesson 2: Safety in Our Country", "type": "lesson"},
    19: {"title": "Lesson 3: The Bauxite Industry in Our Country", "type": "lesson"},
    20: {"title": "Practice Exercises", "type": "exercises"},
    21: {"title": "Intro: Development of Our Country After 1945", "type": "intro"},
    22: {"title": "Lesson 1: Development Aid to Our Country", "type": "lesson"},
    23: {"title": "Lesson 2: The Brokopondo Dam in the Suriname River", "type": "lesson"},
    24: {"title": "Lesson 3: Social Development", "type": "lesson"},
    25: {"title": "Practice Exercises", "type": "exercises"},
    26: {"title": "Intro: How Our Country Was Governed", "type": "intro"},
    27: {"title": "Lesson 1: The Governor and the Political Council", "type": "lesson"},
    28: {"title": "Lesson 2: Introduction of Voting Rights", "type": "lesson"},
    29: {"title": "Lesson 3: Boss in Your Own House", "type": "lesson"},
    30: {"title": "Practice Exercises", "type": "exercises"},
    31: {"title": "Intro: Our Country, an Independent Republic", "type": "intro"},
    32: {"title": "Lesson 1: The Independence of Our Country", "type": "lesson"},
    33: {"title": "Lesson 2: A Coup d'État in Our Country", "type": "lesson"},
    34: {"title": "Lesson 3: Changes in Government", "type": "lesson"},
    35: {"title": "Practice Exercises", "type": "exercises"},
}

def get_vault_files():
    """Obtiene todos los archivos del vault."""
    vault_files = []
    for root, dirs, files in os.walk("."):
        # Ignorar carpetas especiales
        if any(x in root for x in [".git", ".obsidian", ".temp", "_images", ".scripts"]):
            continue
        for f in files:
            if f.endswith(".md"):
                vault_files.append(os.path.join(root, f))
    return vault_files

def analyze_vault():
    """Analiza qué secciones existen en el vault."""
    vault_files = get_vault_files()
    
    print("=== ARCHIVOS EN EL VAULT ===\n")
    for f in sorted(vault_files):
        print(f"  {f}")
    
    print(f"\n\nTotal de archivos: {len(vault_files)}")
    
    # Analizar estructura actual
    print("\n\n=== ESTRUCTURA ACTUAL DEL VAULT ===\n")
    
    topics = {}
    for root, dirs, files in os.walk("."):
        if any(x in root for x in [".git", ".obsidian", ".temp", "_images", ".scripts"]):
            continue
        for d in dirs:
            if d.startswith("Topic"):
                topic_name = d
                topic_files = [f for f in os.listdir(d) if f.endswith(".md")]
                topics[topic_name] = topic_files
    
    for topic, files in sorted(topics.items()):
        print(f"\n{topic}:")
        for f in sorted(files):
            print(f"  - {f}")

def compare_with_original():
    """Compara el vault con la estructura original."""
    print("\n\n=== COMPARACIÓN CON ESTRUCTURA ORIGINAL ===\n")
    
    # Crear un mapeo de lo que debería existir
    expected_files = [
        "Topic 1 - Workers Stand Up for a Better Life/01 - Introduction - Workers Stand Up for a Better Life.md",
        "Topic 1 - Workers Stand Up for a Better Life/01 - Lesson 1 - A Time of Crisis and Unemployment.md",
        "Topic 1 - Workers Stand Up for a Better Life/01 - Practice Exercises.md",
        "Topic 2 - Education in Our Country/04 - Introduction - Education in Our Country.md",
        "Topic 2 - Education in Our Country/05 - Lesson 1 - How Was It in the Past.md",
        "Topic 2 - Education in Our Country/06 - Lesson 2 - Education Changes.md",
        "Topic 2 - Education in Our Country/07 - Lesson 3 - How Important Is Good Education.md",
        "Topic 3 - Different Cultures in Our Country/08 - Introduction - Different Cultures in Our Country.md",
        "Topic 3 - Different Cultures in Our Country/09 - Lesson 1 - How We Came Together Here.md",
        "Topic 3 - Different Cultures in Our Country/10 - Lesson 2 - Experiencing Culture.md",
        "Topic 3 - Different Cultures in Our Country/11 - Lesson 3 - Our Country a Melting Pot of Cultures.md",
        "Topic 4 - Our Country During World War II/12 - Introduction - Our Country During World War II.md",
        "Topic 4 - Our Country During World War II/13 - Lesson 1 - War with Germany.md",
        "Topic 4 - Our Country During World War II/14 - Lesson 2 - Safety in Our Country.md",
        "Topic 4 - Our Country During World War II/15 - Lesson 3 - The Bauxite Industry in Our Country.md",
        "Topic 5 - Development of Our Country After 1945/16 - Introduction - Development of Our Country After 1945.md",
        "Topic 5 - Development of Our Country After 1945/17 - Lesson 1 - Development Aid to Our Country.md",
        "Topic 5 - Development of Our Country After 1945/18 - Lesson 2 - The Brokopondo Dam in the Suriname River.md",
        "Topic 5 - Development of Our Country After 1945/19 - Lesson 3 - Social Development.md",
        "Topic 5 - Development of Our Country After 1945/20 - Practice Exercises.md",
        "Topic 6 - How Our Country Was Governed/21 - Introduction - How Our Country Was Governed.md",
        "Topic 6 - How Our Country Was Governed/22 - Lesson 1 - The Governor and the Political Council.md",
        "Topic 6 - How Our Country Was Governed/23 - Lesson 2 - Introduction of Voting Rights.md",
        "Topic 6 - How Our Country Was Governed/24 - Lesson 3 - Boss in Your Own House.md",
        "Topic 6 - How Our Country Was Governed/25 - Practice Exercises.md",
        "Topic 7 - Our Country, an Independent Republic/26 - Introduction - Our Country, an Independent Republic.md",
        "Topic 7 - Our Country, an Independent Republic/27 - Lesson 1 - The Independence of Our Country.md",
        "Topic 7 - Our Country, an Independent Republic/28 - Lesson 2 - A Coup d'État in Our Country.md",
        "Topic 7 - Our Country, an Independent Republic/29 - Lesson 3 - Changes in Government.md",
        "Topic 7 - Our Country, an Independent Republic/30 - Practice Exercises.md",
    ]
    
    existing = set()
    for root, dirs, files in os.walk("."):
        if any(x in root for x in [".git", ".obsidian", ".temp", "_images", ".scripts"]):
            continue
        for f in files:
            if f.endswith(".md"):
                existing.add(os.path.join(root, f).replace("\\", "/"))
    
    print("ARCHIVOS QUE FALTAN:")
    missing = []
    for expected in sorted(expected_files):
        if expected not in existing:
            print(f"  ❌ {expected}")
            missing.append(expected)
    
    if not missing:
        print("  ✓ Ninguno - todos los archivos existen")
    
    print(f"\nTotal esperado: {len(expected_files)}")
    print(f"Total existente: {len(existing)}")
    print(f"Faltantes: {len(missing)}")
    
    # Verificar archivos extra
    extra = existing - set(expected_files)
    if extra:
        print("\nARCHIVOS EXTRA (no esperados):")
        for e in sorted(extra):
            print(f"  + {e}")

if __name__ == "__main__":
    analyze_vault()
    compare_with_original()
