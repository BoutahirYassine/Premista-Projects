# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 12:54:22 2023

@author: yassine.boutahir
"""
from fonctionCalculette import *


currentdf = getDataDF(parametre_entrant)
currentdf = getRAVaUtiliser(currentdf)
currentdf = getMAFetRAVMaximum(currentdf)

def test_mensualiteMaximum():
    assert(currentdf['mensualiteMaximum'].all()>=0)
    assert currentdf.apply(lambda row: row['mensualiteMaximum'] == (row['endettement_apres_ac'] / 100) * row['revenuTotal'] - (row['charges'] + row['mensualiteCharge']), axis=1).all()
    
    
def test_mafMaximum():
    assert (currentdf['mafMaximum'] == (
        currentdf['mensualiteMaximum']
        * (((1 + (currentdf['taux_nominal'] / 12) / 100) ** currentdf['duree_max']) - 1)
        / (((currentdf['taux_nominal'] / 12) / 100) * ((1 + (currentdf['taux_nominal'] / 12) / 100) ** currentdf['duree_max']))
    )).all()    
    
    
def test_ravMaximum():
    assert (currentdf['ravMaximum'] == (currentdf['revenuTotal'] - currentdf[['charges', 'mensualiteCharge', 'mensualiteMaximum']].sum(axis=1))).all() 
    
    