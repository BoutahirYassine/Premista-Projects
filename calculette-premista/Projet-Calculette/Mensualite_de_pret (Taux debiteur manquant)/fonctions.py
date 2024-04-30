# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:17:59 2023

@author: yassine.boutahir
"""

import math

#------------------------------------Calculer l'arrondi d'un nombre-------------------------------------------

def arrondi(N):
    if N - int(N)>=0.5:
        return math.ceil(N)
    else:
        return int(N)

#------------------------------------------- Taux Debiteur --------------------------------------------------
def tauxDebiteur(i, nom):
    Dict1 = {4: 3.95, 5: 4.16, 6: 4.32, 7: 4.59, 8: 4.79, 9: 4.95, 10: 5.07, 11: 5.17, 12: 5.17, 13: 5.33, 14: 5.33, 15: 5.45}
    Dict2 = {5: 4.53, 6: 4.53, 7: 4.53, 8: 4.53, 9: 4.53, 10: 4.53, 11: 4.53, 12: 4.53, 13: 4.53, 14: 4.53, 15: 4.53, 16: 4.53, 17: 5.18, 18: 5.18, 19: 5.18, 20: 5.18, 21: 5.18, 22: 5.18, 23: 5.18, 24: 5.18, 25: 5.18}
    if nom == "locataire" or nom == 'proprietaire':
        if nom == 'proprietaire':
            return (Dict2[i]) / 100 / 12
        else:
            return (Dict1[i]) / 100 / 12

#------------------------------------------- Fonction Calcul --------------------------------------------------
def calculate_M(C0,Revenu,nom):
    resultat={}
    if nom == 'proprietaire':
        i=range(5,26)
    else:
        if nom == 'locataire':
            i=range(4,16)
        else:
            return 'Erreur dans les choix ( locataire ou proprietaire )'
    for i in i:
        taux_Debiteur = tauxDebiteur(i,nom)   #modifier ici le taux debiteur !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        N=i*12
        num = C0 * taux_Debiteur * (1 + taux_Debiteur)**N
        den = ((1 + taux_Debiteur)**N) - 1
        M = num / den
        M=arrondi(M)
        if M <= 0.45 * Revenu:
            Dict={i:M}
            resultat.update(Dict)
    return resultat