# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:23:23 2023

@author: yassine.boutahir
"""

from fonctionCalculette import *



def est_positif(nombre):
    return nombre >= 0

def test_getRAVaUtiliser1():
    parametre_entrant['nb_personne_dans_le_foyer'] = 1
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre1']).all()
    assert (est_positif(currentdf['ravProduitAUtiliser']) == True).all()
#test_getRAVaUtiliser1()

def test_getRAVaUtiliser2():
    parametre_entrant['nb_personne_dans_le_foyer'] = 2
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre2']).all()
    assert (est_positif(currentdf['ravProduitAUtiliser']) == True).all()

    
def test_getRAVaUtiliser3():
    parametre_entrant['nb_personne_dans_le_foyer'] = 3
    
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre3']).all()
    assert (est_positif(currentdf['ravProduitAUtiliser'] ) == True).all()
    
def test_getRAVaUtiliser4():
    parametre_entrant['nb_personne_dans_le_foyer'] = 4
    
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre4']).all()
    assert (est_positif(currentdf['ravProduitAUtiliser'] ) == True).all()
    
def test_getRAVaUtiliser5():
    parametre_entrant['nb_personne_dans_le_foyer'] = 5
    
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre5']).all()
    assert (est_positif(currentdf['ravProduitAUtiliser'] ) == True).all()
    
def test_getRAVaUtiliser6():
    parametre_entrant['nb_personne_dans_le_foyer'] = 6
    
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)
    assert (currentdf['ravProduitAUtiliser'] == currentdf['reste_a_vivre5'] + ((currentdf['nb_personne_dans_le_foyer'] - 5) * currentdf['reste_a_vivre_supp'])).all()
    assert (est_positif(currentdf['ravProduitAUtiliser'] ) == True).all()
    
    
def test_getRAVaUtiliser0():
    parametre_entrant['nb_personne_dans_le_foyer'] = 0
    currentdf = getDataDF(parametre_entrant)
    getRAVaUtiliser(currentdf)

    assert (currentdf['ravProduitAUtiliser'] == 0).all()
    assert (est_positif(currentdf['ravProduitAUtiliser'] ) == True).all()