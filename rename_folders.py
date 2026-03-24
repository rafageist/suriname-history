import os

RENAME_MAP = {
    # Tema 1
    "tema1_introduccion": "01 - Arbeiders komen op voor een beter bestaan",
    "tema1_leccion1": "01 - Les 1 - Een tijd van crisis en werkloosheid",
    "tema1_leccion2": "01 - Les 2 - Louis Doedel en Anton de Kom",
    "tema1_leccion3": "01 - Les 3 - Vakbonden en vakcentrales",
    "tema1_ejercicios": "01 - Verwerkingsopdrachten",
    
    # Tema 2
    "tema2_introduccion": "02 - Het onderwijs in ons land",
    "tema2_leccion1": "02 - Les 1 - Hoe was het vroeger",
    "tema2_leccion2": "02 - Les 2 - Het onderwijs verandert",
    "tema2_leccion3": "02 - Les 3 - Hoe belangrijk is goed onderwijs",
    "tema2_ejercicios": "02 - Verwerkingsopdrachten",
    
    # Tema 3
    "tema3_introduccion": "03 - Verschillende culturen in ons land",
    "tema3_leccion1": "03 - Les 1 - Hoe wij hier ook samenkwamen",
    "tema3_leccion2": "03 - Les 2 - Het beleven van cultuur",
    "tema3_leccion3": "03 - Les 3 - Ons land een smeltkroes van culturen",
    "tema3_ejercicios": "03 - Verwerkingsopdrachten",
    
    # Tema 4
    "tema4_introduccion": "04 - Ons land tijdens de Tweede Wereldoorlog",
    "tema4_leccion1": "04 - Les 1 - Oorlog met Duitsland",
    "tema4_leccion2": "04 - Les 2 - De veiligheid in ons land",
    "tema4_leccion3": "04 - Les 3 - De bauxietindustrie in ons land",
    "tema4_ejercicios": "04 - Verwerkingsopdrachten",
    
    # Tema 5
    "tema5_introduccion": "05 - Ontwikkeling van ons land na 1945",
    "tema5_leccion1": "05 - Les 1 - Ontwikkelingshulp aan ons land",
    "tema5_leccion2": "05 - Les 2 - De stuwdam in de Surinamerivier",
    "tema5_leccion3": "05 - Les 3 - Sociale ontwikkeling",
    "tema5_ejercicios": "05 - Verwerkingsopdrachten",
    
    # Tema 6
    "tema6_introduccion": "06 - Hoe ons land werd bestuurd",
    "tema6_leccion1": "06 - Les 1 - De gouverneur en de Politieke Raad",
    "tema6_leccion2": "06 - Les 2 - Invoering van kiesrecht",
    "tema6_leccion3": "06 - Les 3 - Baas in eigen huis",
    "tema6_ejercicios": "06 - Verwerkingsopdrachten",
    
    # Tema 7
    "tema7_introduccion": "07 - Ons land een zelfstandige republiek",
    "tema7_leccion1": "07 - Les 1 - De onafhankelijkheid van ons land",
    "tema7_leccion2": "07 - Les 2 - Een staatsgreep in ons land",
    "tema7_leccion3": "07 - Les 3 - Veranderingen in het bestuur",
    "tema7_ejercicios": "07 - Verwerkingsopdrachten",
}

def rename_folders(base_dir):
    changes = []
    for old_name, new_name in RENAME_MAP.items():
        old_path = os.path.join(base_dir, old_name)
        new_path = os.path.join(base_dir, new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            changes.append(f"OK {old_name} -> {new_name}")
        else:
            changes.append(f"MISSING: {old_name}")
    
    return changes

if __name__ == "__main__":
    base_dir = "lecciones"
    print("Renombrando carpetas...\n")
    
    results = rename_folders(base_dir)
    for r in results:
        print(r)
    
    ok_count = len([r for r in results if r.startswith("OK")])
    print(f"\n{ok_count}/{len(results)} carpetas renombradas")