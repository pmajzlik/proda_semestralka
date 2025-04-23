ceska_mesta = (
    ("Praha", 50.0755, 14.4378, "Administrativní"),
    ("Brno", 49.1951, 16.6068, "Průmyslové"),
    ("Ostrava", 49.8209, 18.2625, "Těžební"),
    ("Plzeň", 49.7475, 13.3776, "Průmyslové"),
    ("Liberec", 50.7671, 15.0562, "Turistické"),
    ("Olomouc", 49.5938, 17.2509, "Univerzitní"),
    ("České Budějovice", 48.9747, 14.4743, "Průmyslové"),
    ("Hradec Králové", 50.2092, 15.8328, "Univerzitní"),
    ("Zlín", 49.2264, 17.6706, "Průmyslové"),
    ("Karlovy Vary", 50.2310, 12.8711, "Lázeňské"),
)

hranice_delky = 15.0

# Pouze názvy měst a kategorie pro západ a východ
zapadni_mesta = {(mesto[0], mesto[3]) for mesto in ceska_mesta if mesto[2] < hranice_delky}
vychodni_mesta = [(mesto[0], mesto[3]) for mesto in ceska_mesta if mesto[2] >= hranice_delky]

# Procházení východních měst a kontrola, zda kategorie existuje v západním setu
for mesto, kategorie in vychodni_mesta:
    if any(kategorie == kategorie_zapad for _, kategorie_zapad in zapadni_mesta):
        print(f"Kategorie města {mesto} existuje v západním setu.")
    else:
        print(f"Kategorie města {mesto} neexistuje v západním setu.")


# Unikátní kategorie
unikatni_kategorie_zapad = {kategorie for _, kategorie in zapadni_mesta}

# Procházení unikátních kategorií a zjištění, která města do nich spadají
for kategorie in unikatni_kategorie_zapad:
    print(f"\nKategorie: {kategorie}")
    for mesto, kategorie_mesto in zapadni_mesta:
        if kategorie_mesto == kategorie:
            print(f"  - {mesto}")