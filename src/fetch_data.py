response = requests.get(url)
data = response.json()

# Ajoute cette ligne pour voir la réponse brute
print(json.dumps(data, indent=4))  # Affiche le JSON formaté

df = pd.DataFrame(data[1])  # <-- Ici, le problème peut venir si [1] n'existe pas

import requests
import pandas as pd

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
    data = response.json()
    df = pd.DataFrame(data[1])
    df.to_csv(f"data/{indicator.lower()}.csv", index=False)

for indicator in API_URLS:
    for country in COUNTRIES.keys():
        fetch_data(indicator, country)
