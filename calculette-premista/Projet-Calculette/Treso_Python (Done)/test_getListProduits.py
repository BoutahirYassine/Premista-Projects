# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:39:54 2023

@author: yassine.boutahir
"""

# test_produit.py


import json
from fonctionCalculette import getListProduits

def test_getListProduits():
    # Prepare
    with open('back-database/produitDB.json','r') as file:
        contenu = json.load(file)

    # Act
    result = getListProduits()

    # Assert
    assert result == contenu