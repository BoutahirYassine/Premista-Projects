# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:44:33 2023

@author: yassine.boutahir
"""

import math
import random as rd 
from main import arrondi, tauxDebiteur, calculate_M


def test_arrondi():
    assert arrondi(3.5) == 4
    assert arrondi(2.3) == 2
    assert arrondi(7.8) == 8


def test_tauxDebiteur():
    assert tauxDebiteur(5, 'locataire') == 4.16/100/12
    assert tauxDebiteur(10, 'proprietaire') == 3.68/100/12
    assert tauxDebiteur(15, 'proprietaire') == 4.72/100/12


def test_calculate_M():
    n=rd.randint(0,90000000)
    m=rd.randint(0,90000000)
    for i in range(0,len(calculate_M(n, m, 'locataire'))):
        assert (calculate_M(n, m, 'locataire')[i]>0)
        
def test_Error():
    C0 = rd.randint(0,90000000)
    Revenu = rd.randint(0,90000000)
    nom=''
    if nom != 'proprietaire' and nom !='locataire':
        assert calculate_M(C0,Revenu,nom) == 'Erreur dans les choix ( locataire ou proprietaire )'
