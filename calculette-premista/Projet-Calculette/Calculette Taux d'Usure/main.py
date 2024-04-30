# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:02:15 2023

@author: yassine.boutahir
"""

from fonctions import *
import scipy 

#______________________________________________________Donnees_____________________________________________________________________________


taux_dusure = 6.85

ressources = 3500                                #3
charges_restantes_apres_intervention = 0         #4
norme_endettement = 40                           #5
pret_Immo = 0                               #6
val_Hypo = 0                                #7
ratio_Hypo = 90 /100                             #8
pret_Conso = 80000                              #9
decouvert = 0                                    #10
treso = 0                                     #11
frais_dossier = 1800                          #12
frais_garantie = 0                             #13
autre_frais = 0                              #14 non financé
taux_debiteur = 5.37                             #15
taux_assurance = 00.0189                            #16
duree = 120                                  #17


#______________________________________________________Calcul_______________________________________________________________________________


# Calcul du total des prêts en prenant en compte différents types de prêts
total_des_prets = total_pret(pret_Immo, pret_Conso, treso, decouvert)

# Calcul du besoin de financement global en incluant les frais de dossier et de garantie
besoin_de_financement = besoin_financement(total_des_prets, frais_dossier, frais_garantie, 0)

# Calcul de la valeur hypothécaire en fonction de la valeur de l'hypothèque et d'un ratio
val_immo = val_Hypo * ratio_Hypo

# Calcul des frais de mandat en fonction du besoin de financement
frais_mandat_potentiel  = 0

# Recalcul du besoin de financement en incluant les frais de mandat
besoin_de_financement = besoin_financement(total_des_prets, frais_dossier, frais_garantie, frais_mandat_potentiel )

frais_mandat_max = calcul_frais_mandat_max(besoin_de_financement)
# Calcul de la mensualité du prêt en fonction du besoin de financement, taux d'intérêt et durée
mensualite = calcul_mensualite(besoin_de_financement, taux_debiteur, duree)

# Calcul du taux d'endettement après intervention en pourcentage des ressources
endettement_apres = ((mensualite + charges_restantes_apres_intervention) / ressources) * 100
if endettement_apres > norme_endettement :
    endettement_apres = norme_endettement
    mensualite = ((endettement_apres/100)*ressources) - charges_restantes_apres_intervention
    
# Calcul de la mensualité incluant l'assurance du prêt
mensualite_assurance = mensualite_assurance_calcul(mensualite, taux_assurance , besoin_de_financement)

# Calcul du Taux Annuel Effectif Global (TAEG) en prenant en compte divers frais
taeg = calculTAEG(total_des_prets, mensualite_assurance, duree , autre_frais)

#Calcul des frais de mandat potentiel
while taux_dusure - taeg > 0.0009966485145165294 :
    frais_mandat_potentiel +=1
    # Recalcul du besoin de financement en incluant les frais de mandat
    besoin_de_financement = besoin_financement(total_des_prets, frais_dossier, frais_garantie, frais_mandat_potentiel )
    
    # Calcul de la mensualité du prêt en fonction du besoin de financement, taux d'intérêt et durée
    mensualite = calcul_mensualite(besoin_de_financement, taux_debiteur, duree)
    
    # Calcul du taux d'endettement après intervention en pourcentage des ressources
    endettement_apres = ((mensualite + charges_restantes_apres_intervention) / ressources) * 100
    if endettement_apres > norme_endettement :
        endettement_apres = norme_endettement
        mensualite = ((endettement_apres/100)*ressources) - charges_restantes_apres_intervention
        
    # Calcul de la mensualité incluant l'assurance du prêt
    mensualite_assurance = mensualite_assurance_calcul(mensualite, taux_assurance , besoin_de_financement)
    
    # Calcul du Taux Annuel Effectif Global (TAEG) en prenant en compte divers frais
    taeg = calculTAEG(total_des_prets, mensualite_assurance, duree , autre_frais)
    
frais_mandat = calcul_frais_mandat(frais_mandat_max ,frais_mandat_potentiel ,besoin_de_financement,val_immo)
    
#______________________________________________________Resultats____________________________________________________________________________

if(taux_dusure >= taeg):
    print("1. Total des prêts:               {}".format(total_des_prets))
    print("2. Frais de dossier:              {}".format(frais_dossier))
    print("3. Frais de garantie:             {}".format(frais_garantie))
    print("4. Frais de mandat:               {}".format(frais_mandat))
    print("5. Besoin de financement:         {}".format(besoin_de_financement))
    print("6. Taux débiteur:                 {}".format(taux_debiteur))
    print("7. TAEG:                         "                       , taeg)
    print("8. Taux d'usure:                  {:.3f}".format(taux_dusure))
    print("9. Valeur immobilière:            {}".format(val_immo))
    print("10. Mensualité:                  ",mensualite)
    print("11. Endettement après:            {:.2f}".format(endettement_apres))
    
else:
     print("Impossible le TAEG est supérieur au taux d'usure. Veuillez réduire le taux débiteur ou diminuer les frais")


print("\n Pour information : ")
print("Frais de mandat max (8%) :           ",frais_mandat_max)
print("Frais de mandat potentiel (usure) :  ",frais_mandat_potentiel )


