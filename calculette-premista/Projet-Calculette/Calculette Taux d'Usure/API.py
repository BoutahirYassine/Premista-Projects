# -*- coding: utf-8 -*-
"""
Créé le Ven Août 4 11:02:15 2023

Auteur: yassine.boutahir
"""
from flask import Flask, request, jsonify
from flasgger import Swagger


from fonctions import *
import scipy

app = Flask(__name__)
swagger = Swagger(app)

#______________________________________________________Calculs_______________________________________________________________________________

# Définition d'une fonction pour effectuer les calculs
@app.route('/effectuer_calculs', methods=['GET'])
def effectuer_calculs():
    # Calculs...
    
    """
    Calculette : Taux d'usure'
    ---
    parameters:
      - name: taux_dusure
        in: query
        type: number
        required: true
      - name: ressources
        in: query
        type: number
        required: true
      - name: charges_restantes_apres_intervention
        in: query
        type: number
        required: true
      - name: norme_endettement
        in: query
        type: number
        required: true
      - name: pret_Immo
        in: query
        type: number
        required: true
      - name: val_Hypo
        in: query
        type: number
        required: true
      - name: ratio_Hypo
        in: query
        type: number
        required: true
      - name: pret_Conso
        in: query
        type: number
        required: true   
      - name: decouvert
        in: query
        type: number
        required: true
      - name: treso
        in: query
        type: number
        required: true
      - name: frais_dossier
        in: query
        type: number
        required: true
      - name: frais_garantie
        in: query
        type: number
        required: true
      - name: autre_frais
        in: query
        type: number
        required: true
      - name: taux_debiteur
        in: query
        type: number
        required: true
      - name: taux_assurance
        in: query
        type: number
        required: true
      - name: duree
        in: query
        type: integer
        required: true
        
    responses:
      200:
        description: Successful operation
    """
    taux_dusure = float(request.args.get('taux_dusure'))
    ressources = float(request.args.get('ressources'))                               #3
    charges_restantes_apres_intervention = float(request.args.get('charges_restantes_apres_intervention'))         #4
    norme_endettement = float(request.args.get('norme_endettement'))                            #5
    pret_Immo = float(request.args.get('pret_Immo'))                                #6
    val_Hypo = float(request.args.get('val_Hypo'))                                #7
    ratio_Hypo = float(request.args.get('ratio_Hypo'))                              #8
    pret_Conso = float(request.args.get('pret_Conso'))                                #9
    decouvert = float(request.args.get('decouvert'))                                    #10
    treso = float(request.args.get('treso'))                                    #11
    frais_dossier = float(request.args.get('frais_dossier'))                            #12
    frais_garantie = float(request.args.get('frais_garantie'))                             #13
    autre_frais = float(request.args.get('autre_frais'))                               #14 non financé
    taux_debiteur = float(request.args.get('taux_debiteur'))                               #15
    taux_assurance = float(request.args.get('taux_assurance'))                            #16
    duree = int(request.args.get('duree'))                                 #17
    

    
    total_des_prets = total_pret(pret_Immo, pret_Conso, treso, decouvert)
    besoin_de_financement = besoin_financement(total_des_prets, frais_dossier, frais_garantie, 0)
    val_immo = val_Hypo * ratio_Hypo
    frais_mandat = calcul_frais_mandat(besoin_de_financement, val_immo)
    besoin_de_financement = besoin_financement(total_des_prets, frais_dossier, frais_garantie, frais_mandat)
    mensualite = calcul_mensualite(besoin_de_financement, taux_debiteur, duree)
    endettement_apres = ((mensualite + charges_restantes_apres_intervention) / ressources) * 100
    if endettement_apres > norme_endettement:
        endettement_apres = norme_endettement
        mensualite = ((endettement_apres / 100) * ressources) - charges_restantes_apres_intervention
    mensualite_assurance = mensualite_assurance_calcul(mensualite, besoin_de_financement, taux_assurance)
    taeg = calculTAEG(total_des_prets, mensualite_assurance, duree, autre_frais)
    
    
    response_data = {
        "Total des prêts": round(total_des_prets, 2),
        "Frais de dossier": round(frais_dossier, 2),
        "Frais de garantie": round(frais_garantie, 2),
        "Frais de mandat": round(frais_mandat, 2),
        "Besoin de financement": round(besoin_de_financement, 2),
        "Taux débiteur": round(taux_debiteur, 2),
        "TAEG": round(taeg, 2),
        "Taux d'usure": round(taux_dusure, 2),
        "Valeur immobilière": round(val_immo, 2),
        "Mensualité": round(mensualite, 2),
        "Endettement après": round(endettement_apres, 2)
    }

# Return the results as JSON response
    return jsonify(response_data)


if __name__ == '__main__':
    print("Début de Calcul .... \n")
    app.run()  