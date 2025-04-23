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

# Vytvoření dvou prázdných setů
turisticke_atrakce = set()
prirodni_rezervace = set()

def pridej_do_setu(mesto):
    
   
    #Funkce přidá město do setu turistických atrakcí nebo přírodních rezervací podle jeho kategorie.
    
   # Parametr mesto: Tuple obsahující (název města, šířka, délka, kategorie)
    nazev, x, y, kategorie = mesto
    if kategorie == "Turistické" or kategorie == "Univerzitní":
        turisticke_atrakce.add((x, y))  # Přidáme souřadnice jako tuple
    elif kategorie == "Lázeňské" or kategorie == "Administrativní" or kategorie == "Průmyslové":
        prirodni_rezervace.add((x, y))  # Přidáme souřadnice jako tuple
    

for mesto in ceska_mesta:
    pridej_do_setu(mesto)

print("Turistické atrakce:", turisticke_atrakce)
print("Přírodní rezervace:", prirodni_rezervace)

turisticke_nebo_prirodni = turisticke_atrakce | prirodni_rezervace

turisticke_i_prirodni = turisticke_atrakce & prirodni_rezervace

turisticke_ale_ne_prirodni = turisticke_atrakce - prirodni_rezervace

turisticke_nebo_prirodni_ne_obojim = (turisticke_atrakce | prirodni_rezervace) - (turisticke_atrakce & prirodni_rezervace)

print("Turisticke nebo prirodni:", turisticke_nebo_prirodni)
print("Turisticke i prirodni:", turisticke_i_prirodni)
print("Turisticke ale ne prirodni:", turisticke_ale_ne_prirodni)
print("Turisticke nebo prirodni ne obojim:", turisticke_nebo_prirodni_ne_obojim)