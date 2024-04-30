# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:32:27 2023

@author: yassine.boutahir
"""
import json
import math
from datetime import datetime
import pandas as pd
import numpy as np


#---------------------------------------- Paramètre--------------------------------------------------

# Obtenir la date actuelle
current_date = datetime.now().date()
# Obtenir l'heure actuelle
current_time = datetime.now().time()

# Configurer les options d'affichage pour afficher tout le tableau
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#-----------------------------------------------------------------------------------------------------------------
#----------------------------------Récupération des listes de Produits--------------------------------------------
def getListProduits():
    with open('back-database/produitDB.json','r') as file:
        contenu = json.load(file)
    return contenu
#----------------------------------------------------------------------------------------------------------------
#---------------------------------Récupération des informations--------------------------------------------------
def getDataDF(parametre_entrant):
    currentdf = getListProduits()
    param_df = parametre_entrant
    
    #transformer Dataframe
    currentdf = pd.DataFrame(currentdf)
    param_df = pd.DataFrame.from_dict(param_df, orient='index').T
    
    #concatener
    param_df = pd.concat([param_df] * len(currentdf), ignore_index=True)  #etendre la liste param_df
    currentdf = pd.concat([currentdf, param_df],axis=1)
    currentdf = currentdf[currentdf['type_dossier'].str.contains(parametre_entrant['typologie_dossier'], case=False)]
    
    return currentdf
#---------------------------------------------------------------------------------------------------------
#-------------------------------------------Calcul le RAV de l'emprunteur------------------------------------------------
def getRAVaUtiliser(currentdf):
    currentdf['ravProduitAUtiliser'] = currentdf.apply(lambda row: 
        row.loc['reste_a_vivre1'] if row.loc['nb_personne_dans_le_foyer'] == 1 else
        row.loc['reste_a_vivre2'] if row.loc['nb_personne_dans_le_foyer'] == 2 else
        row.loc['reste_a_vivre3'] if row.loc['nb_personne_dans_le_foyer'] == 3 else
        row.loc['reste_a_vivre4'] if row.loc['nb_personne_dans_le_foyer'] == 4 else
        row.loc['reste_a_vivre5'] if row.loc['nb_personne_dans_le_foyer'] == 5 else
        row.loc['reste_a_vivre5'] + ((row.loc['nb_personne_dans_le_foyer'] - 5) * row.loc['reste_a_vivre_supp']) if row.loc['nb_personne_dans_le_foyer'] > 5 else 0, axis=1)
    currentdf=currentdf.fillna(0)
    return currentdf
#---------------------------------------------------------------------------------------------------------------
#-------------------------------------------Calcul du MAF maximum et RAV Maximum------------------------------------------------
def getMAFetRAVMaximum(currentdf):
    currentdf['mensualiteMaximum'] = (
        (currentdf['endettement_apres_ac'] / 100) * currentdf['revenuTotal']
        - currentdf[['charges', 'mensualiteCharge']].sum(axis=1)
    )
    currentdf['mafMaximum'] = (
        currentdf['mensualiteMaximum']
        * (((1 + (currentdf['taux_nominal'] / 12) / 100) ** currentdf['duree_max']) - 1)
        / (((currentdf['taux_nominal'] / 12) / 100)
           * ((1 + (currentdf['taux_nominal'] / 12) / 100) ** currentdf['duree_max']))
    )
    currentdf['ravMaximum'] = (currentdf['revenuTotal'] - currentdf[['charges', 'mensualiteCharge', 'mensualiteMaximum']].sum(axis=1)
    )
    return currentdf
#---------------------------------------------------------------------------------------------------------------
#------------------------------Récuperer la trésorerie max par produits---------------------------------------
def getTresoMaxCRD(current):
    current['maxCRD'] = np.where(current['datascience_treso_crd'].astype(float) == -1,0,
         (current['crd_conso'].astype(float) + current['crd_immo'].astype(float)).sum() * (current['datascience_treso_crd'].astype(float)) / 100)
    
    current['maxMAF'] = np.where(current['datascience_treso_maf'].astype(float) == -1,0,
        current['montant_a_financer'].astype(float) * current['datascience_treso_maf'].astype(float) / 100)
    
    current['maxTresorerie'] = current[['maxCRD', 'maxMAF', 'datascience_treso_max']].astype(float).apply(lambda x: x[x > 0].min(), axis=1)
    current=current.fillna(0)
    return current
#------------------------------------------------------------------------------------------------------------
#------------------------------Récupère la dernière mensualité de montant maximum---------------------------------------
def getCorrectMensualite(currentdf):
    res = []
    for i in range(currentdf.shape[0]):
        row = currentdf.iloc[i]
        if row['ravProduitAUtiliser'] > row['ravMaximum']:
            nouvelleMensualite = np.sum([float(row['revenuTotal']), -float(row['ravProduitAUtiliser']),
                                         -float(row['charges']), -float(row['mensualiteCharge'])])
        else:
            nouvelleMensualite = row['mensualiteMaximum']
            
        nouvelleMAF = nouvelleMensualite * (((1 + ((float(row['taux_nominal']) / 12) / 100)) ** float(row['duree_max'])) - 1) / \
                      (((float(row['taux_nominal']) / 12) / 100) * ((1 + ((float(row['taux_nominal']) / 12) / 100)) ** float(row['duree_max'])))
        
        tresoreriePossible = nouvelleMAF - float(row['montant_a_financer'])
        tresoreriePossibleMaximum = min(float(row['maxTresorerie']), tresoreriePossible) if min(float(row['maxTresorerie']), tresoreriePossible) > 0 else 0
        
        row.loc['nouvelleMensualite'] = nouvelleMensualite
        row.loc['nouvelleMAF'] = nouvelleMAF
        row.loc['tresoreriePossible'] = tresoreriePossible
        row.loc['tresoreriePossibleMaximum'] = tresoreriePossibleMaximum
        res.append(row)
    return pd.DataFrame(res)
#------------------------------------------------------------------------------------------------------------
#------------------------------Rassembler tout les Calculs------------------------------------------------

def Calculs(parametre_entrant):
    currentdf = getDataDF(parametre_entrant)
    currentdf = getRAVaUtiliser(currentdf)
    currentdf = getMAFetRAVMaximum(currentdf)
    currentdf = getTresoMaxCRD(currentdf)
    currentdf = getCorrectMensualite(currentdf)
    return currentdf

#------------------------------------------------------------------------------------------------------------
#-------------------------------------Verifier tous les champs pour detecter les erreurs--------------------------------

def checkError(parametre_entrant):
    revenu = parametre_entrant['revenuTotal']
    crd_conso = parametre_entrant['crd_conso']
    mensualite_conso = parametre_entrant['mensualite_conso']
    mensualite_conso_conserver = parametre_entrant['mensualite_conso_conserver']
    crd_immo = parametre_entrant['crd_immo']
    mensualite_immo = parametre_entrant['mensualite_immo']
    mensualite_immo_conserver = parametre_entrant['mensualite_immo_conserver']
    charges = parametre_entrant['charges']
    nb_personne_dans_le_foyer = parametre_entrant['nb_personne_dans_le_foyer']
    typologie_dossier = parametre_entrant['typologie_dossier']
    montant_a_financer = parametre_entrant['montant_a_financer']


    if checkString(typologie_dossier)==True or checkNumber(revenu) == True or checkNumber(crd_conso) == True or checkNumber(mensualite_conso) == True or checkNumber(mensualite_conso_conserver) == True or checkNumber(crd_immo) == True or checkNumber(mensualite_immo) == True or checkNumber(mensualite_immo_conserver) == True or checkNumber(charges) == True or checkNumber(nb_personne_dans_le_foyer) == True or checkNumber(montant_a_financer):
        return True
    else:
        return False

#---------------------------------------------------------------------------------------------------------
#------------------------------Tester si les champs sont valides------------------------------------------------
def checkNumber(champs):
    if champs is None or (not isinstance(champs, float) and not isinstance(champs, int)) or champs < 0 :
        return True
    else:
        return False

def checkString(champs):
    if champs not in ['proprietaire', 'locataire']:
        return True
    else:
        return False
#------------------------------------------------------------------------------------------------------------
#---------------------------------------------Test------------------------------------------------------



#-------------------------------------------------------------------------------------------------------
#---------------------------------------------Parametre Entrant------------------------------------------------------
parametre_entrant = {
'revenuTotal': 5000,
'crd_conso': 15000,
'mensualite_conso': 200,
'mensualite_conso_conserver': 50,
'crd_immo': 20000,
'mensualite_immo': 450,
'mensualite_immo_conserver': 50,
'charges': 10,
'nb_personne_dans_le_foyer': 1,
'typologie_dossier': 'proprietaire',
'montant_a_financer': 300000,
'montant_treso': 0,
'mensualiteCharge': 100}
#-------------------------------------------------------------------------------------------------------
    
    

