# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:39:45 2023

@author: yassine.boutahir
"""
import math

def arrondi(N):
    if N - int(N)>=0.5:
        return math.ceil(N)
    else:
        return int(N)


def calcul_Mensualite(montant_emprunte, Apport, taux_interet_annuel, duree):
    taux_mensuel = taux_interet_annuel / 12 / 100
    duree_en_mois = duree * 12

    mensualite = ((montant_emprunte - Apport) * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_en_mois)
    cout_total_interets = (mensualite * duree_en_mois) - montant_emprunte

    return arrondi(mensualite), cout_total_interets

mensualite, cout_total_interets = calcul_Mensualite(1500000, 0, 3.95, 19)
print(mensualite)