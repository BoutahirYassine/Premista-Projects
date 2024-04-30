# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:08:25 2023

@author: yassine.boutahir
"""

from flask import Flask, request, jsonify
import math
import json 
import copy
from flasgger import Swagger
from fonctions import *

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/calculate', methods=['GET'])
def calculate():
    """
    Calculette : Rachat de crédits
    ---
    parameters:
      - name: Revenu
        in: query
        type: number
        required: true
      - name: montant_Projet
        in: query
        type: number
        required: true
      - name: montant_CreditImmo
        in: query
        type: number
        required: true
      - name: montant_CreditConso
        in: query
        type: number
        required: true
      - name: Type
        in: query
        type: string
        enum: [locataire, proprietaire]
        required: true
      - name: total_mensualites
        in: query
        type: number
        required: true
      - name: Renégocier mon crédit
        in: query
        type: boolean
        required: true
    responses:
      200:
        description: Successful operation
    """
    try:
        Revenu = float(request.args.get('Revenu'))
        montant_Projet = float(request.args.get('montant_Projet'))
        montant_CreditImmo = float(request.args.get('montant_CreditImmo'))
        montant_CreditConso = float(request.args.get('montant_CreditConso'))
        Type = request.args.get('Type')
        total_mensualites = float(request.args.get('total_mensualites'))

        ok = bool(request.args.get('Renégocier mon crédit')) #Je souhaite renégocier mon crédit immobilier dans le cadre de mon projet 


        if ok ==True :
            c0= montant_Projet + montant_CreditImmo + montant_CreditConso #Montant total
        else:
            c0= montant_Projet + montant_CreditConso #Montant total

        result = calculate_M(c0, Revenu, Type)
        RAV = Revenu - total_mensualites

        result2 = copy.deepcopy(result)

        for key in result2:
            result2[key] = Revenu - result2[key]

        response = {
            'RAV_avant_renegociation': RAV,
            'RAV_apres_renegociation': result2,
            'Mensualite': result
        }

        return jsonify(response)
    except (ValueError, TypeError) as e:
        error_response = {
            'error': 'Données d-entrée non valides. Veuillez vérifier les types de données des paramètres d-entrée.'
        }
        return jsonify(error_response), 400



if __name__ == "__main__":
    app.run()
