import requests

# The base URL where the Flask API is running
BASE_URL = 'http://localhost:5000'  # Replace with the appropriate URL if the API is running on a different server/port

def calculate():
    # Sample data for the API request
    data = {
        'revenu': 5000,
        'crd_conso': 2000,
        'mensualite_conso': 150,
        'mensualite_conso_conserver': 100,
        'crd_immo': 300000,
        'mensualite_immo': 1000,
        'mensualite_immo_conserver': 800,
        'charges': 200,
        'nb_personne_dans_le_foyer': 3,
        'typologie_dossier': 'locataire',
        'montant_a_financer': 1 
    }

    # Endpoint for the 'calculate' route
    url = f"{BASE_URL}/calculate"

    try:
        # Sending a POST request to the 'calculate' endpoint with the JSON data
        response = requests.post(url, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            result = response.json()
            print("Calculation result:", result)
        else:
            # Print the error message if the request was not successful
            print("Error:", response.json())
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)

if __name__ == "__main__":
    calculate()
