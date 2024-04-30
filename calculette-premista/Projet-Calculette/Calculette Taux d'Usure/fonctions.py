# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:00:59 2023

@author: yassine.boutahir

"""
import math
import pandas as pd
import scipy

# Fonction pour arrondir un nombre
def arrondi(N):
    if N - int(N) >= 0.5:
        return math.ceil(N)
    else:
        return int(N)

# Fonction pour calculer la mensualité d'un prêt
def calcul_mensualite(montant_emprunte, taux_interet_annuel, duree):
    taux_mensuel = taux_interet_annuel / 12 / 100
    duree_en_mois = duree

    mensualite = ((montant_emprunte) * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_en_mois)
    cout_total_interets = (mensualite * duree_en_mois) - montant_emprunte

    return mensualite

# Fonction pour calculer le montant total des prêts
def total_pret(pret_Immo, pret_Conso, treso, decouvert):
    return pret_Conso + pret_Immo + treso + decouvert

# Fonction pour calculer le besoin de financement
def besoin_financement(total_des_prets, frais_dossier, frais_garantie, frais_mandat):
    return total_des_prets + frais_dossier + frais_garantie + frais_mandat

# Fonction pour calculer le TAEG
def calculTAEG(capital_emprunte, mensualite, duree, autre_frais):
    def equation(x):
        capital = capital_emprunte - autre_frais
        return capital - (mensualite * ((1 - (1 + x) ** -duree) / x))
    
    r = scipy.optimize.root(equation, 0.01)
    t = r['x'][0]
    taeg = ((1 + t) ** 12) - 1 
    return taeg * 100

# Fonction pour calculer la mensualité avec assurance
def mensualite_assurance_calcul(mensualite, taux_assurance, total_des_prets):
    return ((taux_assurance / 100) * total_des_prets * (1 / 12)) + mensualite

# Fonction pour calculer les frais de mandat
def calcul_frais_mandat_max(besoin_de_financement):
    fm1=(besoin_de_financement*0.08)/(1-0.08)
    return round(fm1)

def calcul_frais_mandat(fm1,fm2,besoin_de_financement,val_immo):
    if(besoin_de_financement < val_immo):
        frais_mandat = -1
    elif fm2<fm1:
        frais_mandat = fm2
    else :
        frais_mandat = fm1
    return round(frais_mandat)