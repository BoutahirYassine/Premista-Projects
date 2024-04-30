# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:25:43 2023

@author: yassine.boutahir
"""

from fonctions import *

#---------------------------------- Exemple d'utilisation------------------------------------------------------
Revenu=4000
montant_Projet = 150000
montant_CreditImmo = 15000
montant_CreditConso = 0
#nom = 'locataire'
nom = 'proprietaire'
total_mensualites = 500
ok = False  #Je souhaite renégocier mon crédit immobilier dans le cadre de mon projet 


if ok ==True :
    c0= montant_Projet + montant_CreditImmo + montant_CreditConso #Montant total
else:
    c0= montant_Projet + montant_CreditConso #Montant total

#------------------------------------------Resultat-------------------------------------------------------------
result = calculate_M(c0,Revenu,nom)
RAV = Revenu - total_mensualites

print(result)
print("Avant renégociation _ reste à vivre :", RAV)
for key in result:
    result[key]= Revenu - result[key]
print("Après renégociation _ reste à vivre :", result)
#---------------------------------------------------------------------------------
