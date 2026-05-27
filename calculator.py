def calculer_tva(prix_ht: float) -> float:
    return prix_ht *1.20

def convertir_euros_dollars(montant_euros: float) -> float:
    return montant_euros *1.08

prix_ttc = calculer_tva(100)
print(f"Prix TTC :{prix_ttc}")