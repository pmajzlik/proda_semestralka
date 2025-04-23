import arcpy
import math
import pandas as pd
import csv 
from pyproj import Transformer
import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

# Povolení přepsání existujících výstupů
arcpy.env.overwriteOutput = True

# Vstupy z toolboxu
populace = arcpy.GetParameterAsText(0)       # cesta k populačnímu rastru
sidla_cesta = arcpy.GetParameterAsText(1)         # cesta k shapefile sídel
network_dataset = arcpy.GetParameterAsText(2)    # cesta k síťovému datasetu silnic (např. z OSM)

# Funkce pro přiřazení rychlosti podle typu silnice
def speed_assignment(highway_type):
    """
    Přiřadí rychlostní limit na základě typu silnice.

    Tato funkce vrací hodnotu rychlosti v km/h pro různé typy silnic, jako jsou dálnice, 
    rychlostní silnice, hlavní a vedlejší silnice, obytné zóny a další. Pokud je zadaný 
    typ silnice neznámý, vrátí výchozí hodnotu 50 km/h.

    Parametry:
    highway_type (str): Typ silnice (např. 'motorway', 'trunk', 'primary', atd.).

    Návratová hodnota:
    float: Rychlostní limit pro zadaný typ silnice v km/h.
    """
    default_speeds = {
        'motorway': 130,        # dálnice
        'trunk': 110,           # rychlostní komunikace
        'primary': 90,          # hlavní silnice 1. třídy
        'secondary': 70,        # silnice 2. třídy
        'tertiary': 50,         # silnice 3. třídy / v obci
        'residential': 50,      # obytná zóna, standard v obci
        'service': 30,          # účelové komunikace
        'unclassified': 50,     # nerozlišené, obecná hodnota
        'track': 20             # polní/cesta pro zemědělce
    }
    return float(default_speeds.get(highway_type, 50))

# Přidání rychlosti do vrstvy silnic
network_layer = arcpy.MakeFeatureLayer_management(network_dataset, "network_layer")

# Přidání nového pole pro rychlost, pokud ještě neexistuje
fields = [f.name for f in arcpy.ListFields(network_layer)]
if "speed_kmh" not in fields:
    arcpy.AddField_management(network_layer, "speed_kmh", "DOUBLE")

# Aktualizace hodnot v poli speed_kmh
with arcpy.da.UpdateCursor(network_layer, ['highway', 'speed_kmh']) as cursor:
    for row in cursor:
        highway_type = row[0]
        speed = speed_assignment(highway_type)
        row[1] = float(speed)
        cursor.updateRow(row)

# Výpis zprávy
arcpy.AddMessage("Atribut 'speed_kmh' byl úspěšně přidán a naplněn podle typu silnice.")

# Filtrace sídel podle počtu obyvatel
pocet_obyvatel_threshold = 5000

# Vytvoření nového sloupce pro počet obyvatel
populace_field = "populace"
arcpy.AddField_management(sidla_cesta, populace_field, "LONG")

# Použití UpdateCursor pro převod hodnoty z textového pole na celé číslo
with arcpy.da.UpdateCursor(sidla_cesta, ['populati_3', populace_field]) as cursor:
    for row in cursor:
        try:
            if row[0].strip() == '':  # kontrola prázdného pole
                row[1] = 0
            else:
                row[1] = int(row[0])
            cursor.updateRow(row)
        except ValueError:
            row[1] = 0
            cursor.updateRow(row)

# Filtrace sídel podle nového sloupce
sql_expression = f"{populace_field} > {pocet_obyvatel_threshold}"

# Vytvoření vrstvy sídel podle výrazu
arcpy.MakeFeatureLayer_management(sidla_cesta, "sidla_layer")
arcpy.SelectLayerByAttribute_management("sidla_layer", "NEW_SELECTION", sql_expression)

# Uložení výsledné vrstvy
output_layer = "sidla_vyssi_5000"
arcpy.CopyFeatures_management("sidla_layer", output_layer)

# Výpis výsledku
arcpy.AddMessage(f"Byla vytvořena nová vrstva: {output_layer} obsahující sídla s více než {pocet_obyvatel_threshold} obyvateli.")

# === Výpočet TravelTime podle geometrie a rychlosti ===
travel_time_field = "TravelTime"

# Zkontroluj, zda pole existuje
if travel_time_field not in fields:
    arcpy.AddField_management(network_dataset, travel_time_field, "DOUBLE")
    arcpy.AddMessage(f"Pole '{travel_time_field}' bylo přidáno do vrstvy.")

# Výpočet délky v kilometrech a zápis do atributu 'length_km'
with arcpy.da.UpdateCursor(network_dataset, ["SHAPE@", "speed_kmh", "length_km", travel_time_field]) as cursor:
    for row in cursor:
        shape = row[0]
        speed = row[1]

        # Geodetická délka v metrech
        length_m = shape.getLength("GEODESIC", "METERS")
        length_km = length_m / 1000.0

        # Zápis délky do atributu 'length_km'
        row[2] = length_km

        if speed and speed > 0:
            travel_time = (length_km / speed) * 60.0  # v minutách
            row[3] = travel_time  # Uložení TravelTime do příslušného pole
        else:
            row[3] = None  # Pokud není platná rychlost, nastavíme TravelTime na None
        # Aktualizace řádku ve vrstvě
        cursor.updateRow(row)

# Zpráva o úspěšném dokončení
arcpy.AddMessage("Výpočet TravelTime podle geometrie a rychlosti byl úspěšně dokončen.")

# Cesta k geodatabázi
gdb_path = r"C:\Users\pavel\Documents\Škola\Gis-projekty\proda_semestralka\proda_semestralka.gdb"
feature_dataset_name = "silnice_network"
feature_dataset = os.path.join(gdb_path, feature_dataset_name)

# Definuj prostorový referenční systém – WGS 84 (EPSG:4326)
spatial_ref = arcpy.SpatialReference(4326)

# Vytvoření Feature Datasetu, pokud neexistuje
if not arcpy.Exists(feature_dataset):
    arcpy.CreateFeatureDataset_management(gdb_path, feature_dataset_name, spatial_ref)
    arcpy.AddMessage(f"Feature dataset '{feature_dataset_name}' byl vytvořen s projekcí: {spatial_ref.name}")
else:
    arcpy.AddMessage(f"Feature dataset '{feature_dataset_name}' již existuje.")

# Kopírování silnic do feature datasetu
output_fc = os.path.join(feature_dataset, "silnice")
if not arcpy.Exists(output_fc):
    arcpy.FeatureClassToFeatureClass_conversion("silnice", feature_dataset, "silnice")
    arcpy.AddMessage("Silnice byly úspěšně zkopírovány do Feature Datasetu.")
else:
    arcpy.AddMessage("Výstupní 'silnice' již existují a kopírování se přeskočil.")


# Cesty a vrstvy
gdb = r"C:\Users\pavel\Documents\Škola\Gis-projekty\proda_semestralka\proda_semestralka.gdb"
network_dataset = gdb + r"\silnice_network\network_dataset"
sidla_input = gdb + r"\sidla_vyssi_5000"
sidla_wgs = gdb + r"\sidla_wgs84"

# Převod vstupní vrstvy do souřadného systému WGS 84 (EPSG:4326)
if not arcpy.Exists(sidla_wgs):
    arcpy.management.Project(sidla_input, sidla_wgs, arcpy.SpatialReference(4326))
    arcpy.AddMessage("Vrstva 'sidla_vyssi_5000' byla reprojektována do WGS 84.")
else:
    arcpy.AddMessage("Vrstva 'sidla_wgs84' již existuje.")

# Vytvoření OD Cost Matrix vrstvy
od_layer = arcpy.na.MakeODCostMatrixLayer(
    in_network_dataset=network_dataset,
    out_network_analysis_layer="OD_CostMatrix",
    impedance_attribute="TravelTime",
    default_cutoff=None,
    default_number_destinations_to_find=1000, 
    output_path_shape="STRAIGHT_LINES"
).getOutput(0)

arcpy.AddMessage("OD Cost Matrix vrstva byla vytvořena s atributem TravelTime.")

# Získání subvrstev (Origins a Destinations)
sub_layers = arcpy.na.GetNAClassNames(od_layer)
origins_layer = sub_layers["Origins"]
destinations_layer = sub_layers["Destinations"]

# Přidání lokalit
arcpy.na.AddLocations(od_layer, origins_layer, sidla_wgs,
search_tolerance="100 Meters", match_type="MATCH_TO_CLOSEST")
arcpy.na.AddLocations(od_layer, destinations_layer, sidla_wgs,
search_tolerance="100 Meters", match_type="MATCH_TO_CLOSEST")

arcpy.AddMessage("Lokality byly přidány.")

# Vyřešení OD matice
arcpy.na.Solve(od_layer)
arcpy.AddMessage("OD Cost Matrix byl úspěšně vyřešen.")

# Získání názvů subvrstev jako dictionary
sub_layers = arcpy.na.GetNAClassNames(od_layer)
origins_path = od_layer.listLayers(sub_layers["Origins"])[0]
destinations_path = od_layer.listLayers(sub_layers["Destinations"])[0]

# Vytvoření feature layerů
orig_lyr = arcpy.management.MakeFeatureLayer(origins_path, "orig_lyr")
dest_lyr = arcpy.management.MakeFeatureLayer(destinations_path, "dest_lyr")

# Počty připojených lokalit
orig_count = int(arcpy.management.GetCount(orig_lyr)[0])
dest_count = int(arcpy.management.GetCount(dest_lyr)[0])

arcpy.AddMessage(f"Připojeno origin bodů: {orig_count}")
arcpy.AddMessage(f"Připojeno destination bodů: {dest_count}")

input_fc = "sidla_vyssi_5000"  # Vstupní vrstva s názvy sídel
input_fc = os.path.join(gdb_path, input_fc)  # Cesta k vrstvě v geodatabázi
output_excel = r"C:\Users\pavel\Desktop\teoreticke_casy.xlsx"

# Ověření souřadnicového systému
sr = arcpy.Describe(input_fc).spatialReference
print(f"Souřadnicový systém vrstvy: {sr.name}")

# Pokud je ve WGS84, transformujeme
transform_needed = sr.factoryCode == 4326
if transform_needed:
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)

fields = ["name", "SHAPE@X", "SHAPE@Y"]
data = []

# Získání a případná transformace souřadnic prvků do seznamu
with arcpy.da.SearchCursor(input_fc, fields) as cursor:
    for row in cursor:
        name, x, y = row
        if None in (x, y):
            print(f"Chybí souřadnice pro {name}, přeskočeno.")
            continue
        if transform_needed:
            try:
                x_m, y_m = transformer.transform(x, y)
            except Exception as e:
                print(f"Chyba při transformaci {name}: {e}")
                continue
        else:
            x_m, y_m = x, y
        data.append({"nazev": name, "x": x_m, "y": y_m})

# Výpočet teoretických časů
results = []
for origin in data:
    row_result = []
    for dest in data:
        dx = origin["x"] - dest["x"]
        dy = origin["y"] - dest["y"]
        vzdalenost_m = math.sqrt(dx ** 2 + dy ** 2)
        vzdalenost_km = vzdalenost_m / 1000.0
        cas_min = (vzdalenost_km / 120.0) * 60
        row_result.append(round(cas_min, 1))
    results.append(row_result)

# Export do Excelu
wb = Workbook()
ws = wb.active
ws.title = "Teoretické časy"

# Hlavička
header = ["OD \\ DO"] + [item["nazev"] for item in data]
ws.append(header)

# Tělo tabulky
for i, origin in enumerate(data):
    row = [origin["nazev"]] + results[i]
    ws.append(row)

# Uložení souboru
wb.save(output_excel)
print("Soubor s teoretickými časy byl vytvořen.")

teoreticke_casy = pd.read_excel(r"C:\Users\pavel\Desktop\NER_vypocet.xlsx", index_col=0)
skutecne_casy = pd.read_excel(r"C:\Users\pavel\Desktop\ROZŘAZENO\Proda\skutecny.xls", index_col=0)

# Načtení teoretických a skutečných časů z Excelu
arcpy.AddMessage("Načítám teoretické časy z Excelu...")
teoreticke_casy = pd.read_excel(r"C:\Users\pavel\Desktop\ROZŘAZENO\Proda\teoreticky.xlsx")
arcpy.AddMessage("Teoretické časy byly úspěšně načteny.")

arcpy.AddMessage("Načítám skutečné časy z Excelu...")
skutecne_casy = pd.read_excel(r"C:\Users\pavel\Desktop\ROZŘAZENO\Proda\skutecny.xls")
arcpy.AddMessage("Skutečné časy byly úspěšně načteny.")

# Vytvoření DataFrame pro NER
mesta = sorted(set(teoreticke_casy['Mesto1']).union(set(teoreticke_casy['Mesto2'])))
ner_data = pd.DataFrame(index=mesta, columns=mesta)

# Načtení shapefile a dat o populaci
shapefile_path2 = output_layer  # Aktualizuj cestu k shapefilu
arcpy.AddMessage(f"Načítám shapefile měst z {shapefile_path2}...")
mesta_layer = arcpy.MakeFeatureLayer_management(shapefile_path2, "mesta_layer")

mesto_pocet_obyvatel = {}
arcpy.AddMessage("Načítám data měst a jejich populace...")
with arcpy.da.SearchCursor(mesta_layer, ['name', 'populace']) as cursor:
    for row in cursor:
        mesto_pocet_obyvatel[row[0]] = row[1]
arcpy.AddMessage("Data o městech a populaci byla načtena.")

ner_vysledky = {}

# Iterace přes všechny unikátní města jako 'city_from' z teoretických časů
for city_from in teoreticke_casy['Mesto1'].unique():
    suma_citatel = 0  # Sčítání čitatele pro výpočet NER
    suma_jmenovatel = 0  # Sčítání jmenovatele pro výpočet NER
    pocet_paru = 0  # Počet validních párů (město-od, město-do)

    # Iterace přes všechna unikátní města jako 'city_to' z teoretických časů
    for city_to in teoreticke_casy['Mesto2'].unique():
        # Pokud jsou 'city_from' a 'city_to' stejné, přeskočíme tento pár
        if city_from == city_to:
            continue

        # Výběr odpovídajícího řádku z teoretických časů pro daný pár měst
        radek_teor = teoreticke_casy[
            (teoreticke_casy['Mesto1'] == city_from) & 
            (teoreticke_casy['Mesto2'] == city_to)
        ]
        # Výběr odpovídajícího řádku z skutečných časů pro daný pár měst
        radek_real = skutecne_casy[
            (skutecne_casy['Mesto1'] == city_from) & 
            (skutecne_casy['Mesto2'] == city_to)
        ]

        # Pokud existují data jak v teoretických, tak ve skutečných časech
        if not radek_teor.empty and not radek_real.empty:
            # Načítání teoretického a skutečného času z dat
            t_teor = radek_teor.iloc[0]['Teoreticky']
            t_real = radek_real.iloc[0]['TravelTime']
            # Získání počtu obyvatel pro město 'city_to'
            pop_to = mesto_pocet_obyvatel.get(city_to, 0)

            # Pokud je teoretický čas větší než 0 a počet obyvatel větší než 0, pokračujeme
            if t_teor > 0 and pop_to > 0:
                # Výpočet poměru skutečného a teoretického času
                pomer = t_real / t_teor
                # Sčítání hodnot pro čitatele a jmenovatele
                suma_citatel += pomer * pop_to
                suma_jmenovatel += pop_to
                pocet_paru += 1  # Zvyšování počtu validních párů

                # Výpis informací o aktuálním páru měst a jejich datech
                arcpy.AddMessage(
                    f"{city_from} ➡ {city_to} | teor: {t_teor}, real: {t_real}, pop_dest: {pop_to}, poměr: {pomer:.4f}"
                )

    # Pokud je součet jmenovatele větší než 0, vypočítáme NER
    if suma_jmenovatel > 0:
        ner = 1 / (suma_citatel / suma_jmenovatel)  # Výpočet NER
        ner_vysledky[city_from] = ner  # Uložení výsledku do slovníku
        arcpy.AddMessage(f"{city_from}: NER = {ner:.4f} z {pocet_paru} párů")  # Výpis výsledku pro město
    else:
        ner_vysledky[city_from] = None  # Pokud není co počítat, přiřadíme hodnotu None
        arcpy.AddMessage(f"{city_from}: NER nelze spočítat (žádná platná data)")  # Výpis chybového stavu
    
# Připravíme DataFrame pro výsledky
ner_vysledky_df = pd.DataFrame(list(ner_vysledky.items()), columns=['Město', 'NER'])

# uložení výsledků do Excelu
output_path = r"C:\Users\pavel\Desktop\NER_vysledky_final_.xlsx"
arcpy.AddMessage(f"Ukládám výsledky do Excelu: {output_path}...")
ner_vysledky_df.to_excel(output_path, index=False)
arcpy.AddMessage("Výsledky byly úspěšně uloženy do Excelu.")

