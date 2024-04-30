# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:25:43 2023

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

    return mensualite, cout_total_interets


def calcul_Capacite_Emprunt(mensualite, taux_interet_annuel, duree):
    taux_mensuel = taux_interet_annuel / 12 / 100
    duree_en_mois = duree * 12

    montant_emprunte = (mensualite * (1 - (1 + taux_mensuel) ** -duree_en_mois)) / taux_mensuel

    return arrondi(montant_emprunte)

###################################      Vos  Revenus    ####################################
#-----------------Vous Concernant----------------------------
mensualite1 = 3000
prime_anuelle1 = 0
#-----------------Co-emprunteur------------------------------
mensualite2 = 0
prime_anuelle2 = 0
#-----------------Autres revenus mensuels (loyers bruts perçus, revenus financiers)-----------
Autres_revenus_mensuels = 0
##############################      Votre apport personnel    ################################

Apport = 0

###################################      Vos  Charges    #####################################

loyer_mensuel = 0
Remboursement_mensuel_de_Credits = 0

#############################      Durée d'emprunt souhaitée    ##############################
##############################################################################################
def taux_interet_annuel(n):                                                             ######
    dict={7:3.5,10:3.5,12:3.5,15:3.6,20:4.11,25:4.29,30:4.11}                            ######
    return dict[n]                                                                      ######
                                                                                        ######
##############################################################################################
#4.172

######################################   CALCUL  #############################################

mensualite = (mensualite1 + mensualite2 - (loyer_mensuel + Remboursement_mensuel_de_Credits) + Autres_revenus_mensuels + ((prime_anuelle1 + prime_anuelle2) /12))*0.33
duree = 20
taux_interet_annuel = taux_interet_annuel(duree)

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

montant_emprunte = calcul_Capacite_Emprunt(mensualite, taux_interet_annuel, duree) + Apport
mensualite, cout_total_interets = calcul_Mensualite(montant_emprunte, Apport, taux_interet_annuel, duree)


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

print("Le montant d'emprunt est :", round(montant_emprunte, 2), "€")
print("Vous aurez à rembourser", round(mensualite, 2), "€ par mois.")
print("Le coût total des intérêts est de", round(cout_total_interets, 2), "€ (+", round((cout_total_interets / montant_emprunte) * 100, 2), "%) sur les", montant_emprunte, "€.")
