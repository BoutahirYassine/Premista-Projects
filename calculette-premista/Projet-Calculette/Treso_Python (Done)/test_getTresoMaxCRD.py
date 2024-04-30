# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:08:18 2023

@author: yassine.boutahir
"""
from fonctionCalculette import *


parametre_entrant = {
'revenuTotal': 5000,
'crd_conso': 15000,
'mensualite_conso': 200,
'crd_immo': 20000,
'mensualite_immo': 450,
'charges': 10,
'nb_personne_dans_le_foyer': 2,
'typologie_dossier': 'proprietaire',
'montant_a_financer': 300000,
'montant_treso': 0,
'mensualiteCharge': sum([float(200), float(450)], 0)}
currentdf = getDataDF(parametre_entrant)
currentdf = getRAVaUtiliser(currentdf)
currentdf = getMAFetRAVMaximum(currentdf)
currentdf = getTresoMaxCRD(currentdf)

def testmaxCRD():
    # print(currentdf['maxCRD'])
    # print(np.where(currentdf['datascience_treso_crd'].astype(float) == -1,0,
    #      (currentdf['crd_conso'].astype(float) + currentdf['crd_immo'].astype(float)).sum()
    #      * (currentdf['datascience_treso_crd'].astype(float)) / 100))
    assert (currentdf['maxCRD'] == np.where(currentdf['datascience_treso_crd'].astype(float) == -1,0,
         (currentdf['crd_conso'].astype(float) + currentdf['crd_immo'].astype(float)).sum() * 
         (currentdf['datascience_treso_crd'].astype(float)) / 100)).all()
    
#testmaxCRD()  
  
def testmaxMAF():
    assert (currentdf['maxMAF'] == np.where(currentdf['datascience_treso_maf'].astype(float) == -1,0,
            currentdf['montant_a_financer'].astype(float) *
            currentdf['datascience_treso_maf'].astype(float) / 100)).all()
    
def testmaxTresorerie():
    maxTreso = currentdf[['maxCRD', 'maxMAF', 'datascience_treso_max']].astype(float).apply(lambda x: x[x > 0].min(), axis=1)
    maxTreso = maxTreso.fillna(0)
    print(maxTreso)
    assert (currentdf['maxTresorerie'] == maxTreso).all()
