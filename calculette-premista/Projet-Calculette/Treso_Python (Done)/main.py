# -*- coding: utf-8 -*-

#------------------------------------------ Fonction MAIN -----------------------------------------------
"""
Created on Tue Jun 13 09:17:12 2023

@author: yassine.boutahir
"""
import json
import re
from fonctionCalculette import *
import warnings


Error = False
#-------------------------------------------------------------------------------------------------------
#-------------------------------------fonction De Calcul------------------------------------------------

def Calcul(revenu, crd_conso,
           mensualite_conso , mensualite_conso_conserver, crd_immo, mensualite_immo, mensualite_immo_conserver, 
           charges, nb_personne_dans_le_foyer, typologie_dossier,
           montant_a_financer):
    global Error
    parametre_entrant = {
    'revenuTotal': revenu,
    'crd_conso': crd_conso,
    'mensualite_conso': mensualite_conso,
    'mensualite_conso_conserver': mensualite_conso_conserver,
    'crd_immo': crd_immo,
    'mensualite_immo': mensualite_immo,
    'mensualite_immo_conserver': mensualite_immo_conserver,
    'charges': charges,
    'nb_personne_dans_le_foyer': nb_personne_dans_le_foyer,
    'typologie_dossier': typologie_dossier,
    'montant_a_financer': montant_a_financer,
    'montant_treso': 0,
    'mensualiteCharge': sum([float(mensualite_conso_conserver), float(mensualite_immo_conserver)], 0)}
    Resultat_Calcul={}
    Error = checkError(parametre_entrant)
    if Error == False:
        Resultat_Calcul = Calculs(parametre_entrant)
    return Resultat_Calcul

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------Affichage Consol--------------------------------------------

# # Ignorer tous les Warning
warnings.filterwarnings("ignore")

print("Début de Calcul .... \n")
Resultat = Calcul(5000,15000,200,200,20000,450,160,50,2,'proprietaire',300000)
print(Error)
if Error ==False:
    print("Voici le Résultat du Calcul : \n")
    print(Resultat)
    print("\n\n")
    print("Calcul terminé avec succés\n\n")
else :
    print("Erreur dans les paramètres \n")


#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
