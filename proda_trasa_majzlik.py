import math

profil_trasy = [
    [50, 0, 230],   
    [52, 1, 288],  
    [54, 3, 233],  
    [56, 4, 247],   
    [58, 5, 199]    
]

for cislo,bod in enumerate(profil_trasy, start=1):
    print(f"{cislo}. Souřadnice: {bod[0]}, {bod[1]}, Výška: {bod[2]} m")

prumerna_nadmomrska_vyska = sum([bod[2] for bod in profil_trasy]) / len(profil_trasy)
print(prumerna_nadmomrska_vyska)

vyssi_nez_prumer = [bod[2] for bod in profil_trasy if bod[2] > prumerna_nadmomrska_vyska]
print(vyssi_nez_prumer)

# Funkce pro výpočet sklony mezi dvěma body
def spocitej_sklon(bod1, bod2):
    x1, y1, z1 = bod1
    x2, y2, z2 = bod2
    horizontalni_vzdalenost = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    sklon = (z2 - z1) / horizontalni_vzdalenost
    return sklon

# Spočítáme sklony mezi sousedními body
sklony = []
for i in range(len(profil_trasy) - 1):
    sklon = spocitej_sklon(profil_trasy[i], profil_trasy[i + 1])
    sklony.append(sklon)

# Výpis výsledků
print("Sklony mezi sousedními body:")
for i, sklon in enumerate(sklony):
    print(f"Sklon mezi bodem {i+1} a bodem {i+2}: {sklon:.2f}")