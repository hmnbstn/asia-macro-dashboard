import requests
import pandas as pd
import json  # Ajout pour éviter l’erreur avec print

API_URLS = {
    "GDP": "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json",
    "Inflation": "https://api.worldbank.org/v2/country/{}/indicator/FP.CPI.TOTL.ZG?format=json",
    "Unemployment": "https://api.worldbank.org/v2/country/{}/indicator/SL.UEM.TOTL.ZS?format=json",
    "Trade Balance": "https://api.oecd.org/data/trade",
    "Interest Rate": "https://api.imf.org/public/indicator/IR"
}

COUNTRIES = {
    "CN": "China",
    "IN": "India",
    "JP": "Japan",
    "SG": "Singapore",
    "KR": "South Korea"
}

def fetch_data(indicator, country_code):
    """Récupère les données et les enregistre en CSV."""
    url = API_URLS[indicator].format(country_code)
    response = requests.get(url)
    
    try:
        data = response.json()
        
        # Vérifier si l'API retourne une liste valide
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1])  # Transforme les données en tableau
            df.to_csv(f"data/{indicator.lower()}.csv", index=False)
        else:
            print(f"⚠️ Erreur : Format de réponse inattendu pour {indicator} ({country_code})")
    
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données pour {indicator} ({country_code}): {e}")

# Exécuter la récupération des données
for indicator in API_URLS:
    for country in COUNTRIES.keys():
        fetch_data(indicator, country)
