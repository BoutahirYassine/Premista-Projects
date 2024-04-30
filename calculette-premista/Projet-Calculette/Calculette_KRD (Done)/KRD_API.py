import pandas as pd
from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def calcul_mensualite(capital_initial, duree_mois, taux_annuel):
    taux_mensuel = taux_annuel / (12 * 100)
    mensualite = (capital_initial * taux_mensuel) / (1 - (1 + taux_mensuel) ** (-duree_mois))
    return mensualite

def calcul_CRD(capital_initial, duree_mois, taux_annuel, duree):
    capital = capital_initial
    taux_mensuel = taux_annuel / (12 * 100)
    interets_list = []
    capital_restant_list = []
    amortissement_list = []
    mensualite = calcul_mensualite(capital_initial, duree_mois, taux_annuel)
    
    for i in range(duree):
        interet = capital * taux_mensuel
        amortissement = mensualite - interet
        capital -= amortissement

        interets_list.append(interet)
        capital_restant_list.append(capital)
        amortissement_list.append(amortissement)

    # Créer la DataFrame
    df = pd.DataFrame({
        'Période': range(1, duree + 1),
        'Intérêt': interets_list,
        'Capital Restant Dû': capital_restant_list,
        'Amortissement': amortissement_list
    })
    CRD = df['Capital Restant Dû'][duree-1]
    return df, CRD

# Données d'entrée
@app.route('/calculate', methods=['GET'])
def get_parameters():
    """
    Calculette : Rachat de crédits
    ---
    parameters:
      - name: capital_initial
        in: query
        type: number
        required: true
      - name: duree_mois
        in: query
        type: number
        required: true
      - name: taux_annuel
        in: query
        type: number
        required: true
      - name: Nombre_de_mois
        in: query
        type: integer
        required: true
        description : nombre de mensualités reglés
    responses:
      200:
        description: Successful operation
    """
    capital_initial = float(request.args.get('capital_initial'))
    duree_mois = float(request.args.get('duree_mois'))
    taux_annuel = float(request.args.get('taux_annuel'))
    Nombre_de_mois = int(request.args.get('Nombre_de_mois'))
    
    
    
    mensualite = calcul_mensualite(capital_initial, duree_mois, taux_annuel)
    df, CRD = calcul_CRD(capital_initial,duree_mois,taux_annuel,Nombre_de_mois)
    
    return jsonify({
        'CRD': CRD,
      'mensualite': mensualite
      #'tableau_amortissement': df.to_dict(orient='records')
    })


if __name__ == '__main__':
    print("Début de Calcul .... \n")
    app.run()
