# Příklad bodu zájmu
bod_zajmu = {
    "id": "1",
    "nazev": "Letná",
    "souradnice": (14.4158122, 50.0976897),
    "typ": "stadion",
    "oteviraci_doba": {
        "pondeli": "zavreno",
        "utery": "zavreno",
        "streda": "zavreno",
        "ctvrtek": "zavreno",
        "patek": "zavreno",
        "sobota": "10:00-18:00",
        "nedele": "10:00-18:00",
    }
}

print(bod_zajmu)

# Seznam bodů zájmu
body_zajmu = [
    {"id": 1, "nazev": "Restaurace U Zlaté hvězdy", "typ": "restaurace"},
    {"id": 2, "nazev": "Městská knihovna", "typ": "knihovna"},
    {"id": 3, "nazev": "Pizzerie Roma", "typ": "restaurace"},
    {"id": 4, "nazev": "Park Stromovka", "typ": "park"},
    {"id": 5, "nazev": "Kavárna Slunce", "typ": "kavárna"}
]

# Hledaný typ
hledany_typ = "restaurace"

# Procházení seznamu bodů zájmu a výpis názvů bodů daného typu
for bod in body_zajmu:
    if bod["typ"] == hledany_typ:
        print("-", bod["nazev"])

# Přidání hodnocení (pro každý druhý bod)
for i, bod in enumerate(body_zajmu):
    if i % 2 == 1:  # Každý druhý bod dostane hodnocení
        bod["hodnoceni"] = (i + 1) * 2  # Příklad hodnocení
    else:
        bod["hodnoceni"] = None  # Pro ostatní None

# Seřazení podle hodnocení (None na poslední místo)
body_zajmu.sort(key=lambda x: (-x["hodnoceni"] if x["hodnoceni"] is not None else float('inf')))

# Výpis seřazeného seznamu bodů zájmu s hodnocením
print("\nSeznam bodů zájmu s hodnocením:")
for bod in body_zajmu:
    nazev = bod["nazev"]
    typ = bod["typ"]
    hodnoceni = bod.get("hodnoceni", "Neznámé")
    if hodnoceni is None:
        hodnoceni = "Neznámé"
    print(f"- {nazev.ljust(25)} ({typ.ljust(10)}) | Hodnocení: {hodnoceni}")

# Převedení seznamu na slovník podle id (pouze pro body s hodnocením > 3)
body_podle_id = {bod["id"]: bod for bod in body_zajmu if bod["hodnoceni"] is not None and bod["hodnoceni"] > 3}

# Výpis slovníku
print("\nSlovník bodů zájmu s hodnocením vyšším než 3:")
print(body_podle_id)

import copy, json
# Mělká kopie (shallow copy)
body_zajmu_melka = copy.copy(body_zajmu)

# Hluboká kopie (deep copy)
body_zajmu_hluboka = copy.deepcopy(body_zajmu)

# Změníme hodnotu vnořeného objektu ve mělké kopii
body_zajmu_melka[0]["hodnoceni"] = 10

# Změníme hodnotu vnořeného objektu v hluboké kopii
body_zajmu_hluboka[1]["hodnoceni"] = 8

# Výpis pro kontrolu
print()
print("Původní seznam bodů zájmu:")
print(body_zajmu)

print("\nMělká kopie (po změně hodnocení):")
print(body_zajmu_melka)

print("\nHluboká kopie (po změně hodnocení):")
print(body_zajmu_hluboka)

# Uložení do JSON souboru
with open('body_zajmu_MAJZLIK.json', 'w', encoding='utf-8') as file:
    json.dump(body_zajmu, file, ensure_ascii=False, indent=4)

print("Seznam bodů zájmu byl úspěšně uložen do souboru 'body_zajmu_MAJZLIK.json'")