
trasa = [
    [50.1, 15.1],  
    [50.2, 15.3],  
    [50.3, 15.9],  
    [50.4, 15.88], 
    [50.5, 15.7]   
]

trasa.append([50.6, 15.8])
print(trasa)

trasa.insert(3, [50.35, 15.5])
print(trasa)

serazena_trasa_desc = sorted(trasa, key=lambda bod: bod[1])
print(serazena_trasa_desc)

prumer_y = sum(bod[0] for bod in trasa) / len(trasa)
prumer_x = sum(bod[1] for bod in trasa) / len(trasa)

print(f"Průměrná hodnota y: {prumer_y}")
print(f"Průměrná hodnota x: {prumer_x}")