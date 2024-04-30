from flask import Flask, request, jsonify
import math
import json 
import copy
import warnings
from flasgger import Swagger
from fonctionCalculette import *

app = Flask(__name__)
swagger = Swagger(app)


Error = False

def Calcul(revenu, crd_conso, mensualite_conso, mensualite_conso_conserver, crd_immo, mensualite_immo, mensualite_immo_conserver, charges, nb_personne_dans_le_foyer, typologie_dossier, montant_a_financer):
    global Error
    parametre_entrant = {
        'revenuTotal': revenu,
        'crd_conso': crd_conso,
        'mensualite_conso': mensualite_conso,
        'mensualite_conso_conserver': mensualite_conso_conserver,
        'crd_immo': crd_immo,
        'mensualite_immo': mensualite_immo,
        'mensualite_immo_conserver': mensualite_immo_conserver,
        'charges': charges,
        'nb_personne_dans_le_foyer': nb_personne_dans_le_foyer,
        'typologie_dossier': typologie_dossier,
        'montant_a_financer': montant_a_financer,
        'montant_treso': 0,
        'mensualiteCharge': sum([float(mensualite_conso_conserver), float(mensualite_immo_conserver)], 0)
    }
    Resultat_Calcul = {}
    Error = checkError(parametre_entrant)
    if Error == False:
        Resultat_Calcul = Calculs(parametre_entrant)
    return Resultat_Calcul

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate API
    ---
    parameters:
      - name: revenu
        in: formData
        type: number
        required: true
      - name: crd_conso
        in: formData
        type: number
        required: true
      - name: mensualite_conso
        in: formData
        type: number
        required: true
      - name: mensualite_conso_conserver
        in: formData
        type: number
        required: true
      - name: crd_immo
        in: formData
        type: number
        required: true
      - name: mensualite_immo
        in: formData
        type: number
        required: true
      - name: mensualite_immo_conserver
        in: formData
        type: number
        required: true
      - name: charges
        in: formData
        type: number
        required: true
      - name: nb_personne_dans_le_foyer
        in: formData
        type: number
        required: true
      - name: typologie_dossier
        in: formData
        type: string
        required: true
      - name: montant_a_financer
        in: formData
        type: number
        required: true
    responses:
      200:
        description: Successful calculation
      400:
        description: Error in the parameters
      500:
        description: Internal server error
    """
    try:
        revenu = float(request.form.get('revenu'))
        crd_conso = float(request.form.get('crd_conso'))
        mensualite_conso = float(request.form.get('mensualite_conso'))
        mensualite_conso_conserver = float(request.form.get('mensualite_conso_conserver'))
        crd_immo = float(request.form.get('crd_immo'))
        mensualite_immo = float(request.form.get('mensualite_immo'))
        mensualite_immo_conserver = float(request.form.get('mensualite_immo_conserver'))
        charges = float(request.form.get('charges'))
        nb_personne_dans_le_foyer = int(request.form.get('nb_personne_dans_le_foyer'))
        typologie_dossier = request.form.get('typologie_dossier')
        montant_a_financer = float(request.form.get('montant_a_financer'))

        result = Calcul(revenu,crd_conso,mensualite_conso,mensualite_conso_conserver,crd_immo,mensualite_immo,mensualite_immo_conserver,charges,nb_personne_dans_le_foyer,typologie_dossier,montant_a_financer)
        
        if Error:
            return jsonify({'error': 'Erreur dans les paramètres'}), 400
        else:
            # Convert the DataFrame to a list of dictionaries
            result_json = result.to_dict(orient='records') if isinstance(result, pd.DataFrame) else result
            return jsonify(result_json), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ignorer tous les Warning
    warnings.filterwarnings("ignore")

    print("Début de Calcul .... \n")
    
    app.run()
