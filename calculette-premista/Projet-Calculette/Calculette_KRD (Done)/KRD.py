import pandas as pd


def calcul_mensualite(capital_initial, duree_mois, taux_annuel):
    taux_mensuel = taux_annuel / (12 * 100)
    mensualite = (capital_initial * taux_mensuel) / (1 - (1 + taux_mensuel) ** (-duree_mois))
    return mensualite

def calcul_CRD(capital_initial, duree_mois, taux_annuel, duree):
    capital = capital_initial
    taux_mensuel = taux_annuel / (12 * 100)
    interets_list = []
    capital_restant_list = []
    amortissement_list = []
    mensualite = calcul_mensualite(capital_initial, duree_mois, taux_annuel)
    for i in range(duree):
        interet = capital * taux_mensuel
        amortissement = mensualite - interet
        capital -= amortissement

        interets_list.append(interet)
        capital_restant_list.append(capital)
        amortissement_list.append(amortissement)

    # Créer la DataFrame
    df = pd.DataFrame({
        'Période': range(1, duree + 1),
        'Intérêt': interets_list,
        'Capital Restant Dû': capital_restant_list,
        'Amortissement': amortissement_list
    })
    CRD = df['Capital Restant Dû'][duree-1]
    return df,CRD

# Données d'entrée

capital_initial = 300000
duree_mois = 180
taux_annuel = 3.5
Nombre_de_mois = 180

# Appel de la fonction pour calcul :
    
mensualite = calcul_mensualite(capital_initial, duree_mois, taux_annuel)
df, CRD = calcul_CRD(capital_initial,duree_mois,taux_annuel,Nombre_de_mois)

#affichage : 
    
print(df)  # Tableau d'amortissement

print("Mensualité : {:.2f} euros".format(mensualite)) #mensualite
print("Capitaux Restant : {:.2f} euros".format(CRD))  #capitaux restant