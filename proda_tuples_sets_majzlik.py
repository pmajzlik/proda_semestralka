# Seznam českých měst se souřadnicemi a ekonomickou kategorií
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


def je_mesto_v_oblasti(mesto, bounding_box):
    
    #Ověří, zda se město nachází uvnitř daného bounding boxu.

    #param mesto: Tuple obsahující (název, šířka, délka), např. ("Praha", 50.0755, 14.4378)
    #param bounding_box: Tuple (min_lat, max_lat, min_lon, max_lon) definující hranice oblasti
    #return: True, pokud se město nachází v oblasti, jinak False
    
    lat, lon = mesto[1], mesto[2]  # Souřadnice jsou na indexech 1 a 2
    min_lat, max_lat, min_lon, max_lon = bounding_box

    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon


# Definice bounding boxu pro oblast Čech
bounding_box_cechy = (48.5, 50.5, 12.5, 15.5)

# Ověření všech měst 
for mesto in ceska_mesta:
    print(f"{mesto[0]}: {je_mesto_v_oblasti(mesto, bounding_box_cechy)}")


hranice_delky = 15.0

# Rozdělení pomocí list comprehension
zapadni_mesta = tuple([mesto for mesto in ceska_mesta if mesto[2] < hranice_delky])
vychodni_mesta = tuple([mesto for mesto in ceska_mesta if mesto[2] >= hranice_delky])

# Výstup
print() 
print("Západní města: ", zapadni_mesta)
print("Východní města: ", vychodni_mesta)