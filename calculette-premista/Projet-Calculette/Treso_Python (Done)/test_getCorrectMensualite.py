# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:59:00 2023

@author: yassine.boutahir
"""
from fonctionCalculette import *
import pytest
currentdf = getDataDF(parametre_entrant)
currentdf = getRAVaUtiliser(currentdf)
currentdf = getMAFetRAVMaximum(currentdf)
currentdf = getTresoMaxCRD(currentdf)
currentdf = getCorrectMensualite(currentdf)


def est_positif(nombre):
    return nombre >= 0

def test_nouvelleMensualiteF():
    assert (est_positif(currentdf['nouvelleMensualite']) == True).all()

    if (currentdf['ravProduitAUtiliser'] > currentdf['ravMaximum']).all():
        assert (currentdf['nouvelleMensualite']==currentdf['revenuTotal']-currentdf['ravProduitAUtiliser']-currentdf['charges']-currentdf['mensualiteCharge']).all()
    else:
        assert (currentdf['nouvelleMensualite']==currentdf['mensualiteMaximum']).all()

def test_nouvelleMAF():
    assert(currentdf['nouvelleMAF'] ==
    currentdf['nouvelleMensualite'] * (((1 + ((currentdf['taux_nominal'] / 12) / 100)) ** currentdf['duree_max']) - 1) / \
              (((currentdf['taux_nominal'] / 12) / 100) * ((1 + ((currentdf['taux_nominal'] / 12) / 100)) ** currentdf['duree_max']))).all()

def test_tresoreriePossiblem():
    #assert(est_positif(currentdf['tresoreriePossible']).all())
    assert(currentdf['tresoreriePossible'] == currentdf['nouvelleMAF'] - currentdf['montant_a_financer']).all()

def test_tresoreriePossibleMaximum():
    #assert((currentdf['tresoreriePossibleMaximum']==0).all() or (currentdf['tresoreriePossibleMaximum']==currentdf['maxTresorerie']).all() or (currentdf['tresoreriePossibleMaximum']==currentdf['tresoreriePossible']).all())
    if min(currentdf['maxTresorerie'].all(),currentdf['tresoreriePossible'].all()) > 0 :
        assert (currentdf['tresoreriePossibleMaximum']==min(currentdf['maxTresorerie'].all(),currentdf['tresoreriePossible'].all()))
    else:
        assert(currentdf['tresoreriePossibleMaximum'].all()==0)
    assert(est_positif(currentdf['tresoreriePossibleMaximum']).all())
    


