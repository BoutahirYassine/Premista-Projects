# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 09:25:17 2023

@author: yassine.boutahir
"""

import requests
import json
from flask import Flask, request, jsonify
import math
import json 
import copy
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)




@app.route('/api', methods=['GET'])
def get_info():
    """
    API : Ville_Région
    ---
    parameters:
      - name: Ville
        in: query
        type: string
        required: true
        description: Nom de la ville.
    responses:
      200:
        description: Successful operation
    """
    
    ville = request.args.get('Ville')
    url = "https://api-adresse.data.gouv.fr/search/?q=" + ville + "&limit=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        context = data['features'][0]['properties']['context']
        return context
    
if __name__ == '__main__':
    app.run()