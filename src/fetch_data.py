import requests
import pandas as pd
import json

API_URLS = {
    "GDP": "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json",
    "Inflation": "https://api.worldbank.org/v2/country/{}/indicator/FP.CPI.TOTL.ZG?format=json",
    "Unemployment": "https://api.worldbank.org/v2/country/{}/indicator/SL.UEM.TOTL.ZS?format=json",
    "Trade Balance": "https://api.worldbank.org/v2/country/{}/indicator/TX.VAL.MRCH.CD.WT?format=json",  # Banque Mondiale
    "Interest Rate": "https://api.worldbank.org/v2/country/{}/indicator/FR.INR.RINR?format=json"  # Banque Mondiale
}

COUNTRIES = ["CN", "IN", "JP", "SG", "KR"]

def fetch_data(indicator, country_code):
    """Récupère les données macroéconomiques et les enregistre en CSV."""
    url = API_URLS[indicator].format(country_code)
    response = requests.get(url)

    try:
        # Afficher le statut de la requête API
        print(f"\n🔍 [{indicator} - {country_code}] Statut de la requête : {response.status_code}")

        # Vérifier si la requête API est réussie
        if response.status_code != 200:
            print(f"❌ Erreur API {indicator} ({country_code}) : Code {response.status_code}")
            return

        data = response.json()

        # Afficher la réponse brute pour analyse
        print(f"\n⚠️ Réponse brute API {indicator} ({country_code}) :")
        print(json.dumps(data, indent=4))

        # Vérifier si la réponse contient bien des données exploitables
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1])
            df.to_csv(f"data/{indicator.lower()}.csv", index=False)
            print(f"✅ Données enregistrées pour {indicator} ({country_code})")
        else:
            print(f"⚠️ Format inattendu ou données absentes pour {indicator} ({country_code})")

    except json.JSONDecodeError:
        print(f"❌ Impossible de décoder JSON pour {indicator} ({country_code}) → Vérifie l'API !")
    except Exception as e:
        print(f"❌ Erreur inattendue pour {indicator} ({country_code}) : {e}")

# Exécuter les appels API
for indicator in API_URLS:
    for country in COUNTRIES:
        fetch_data(indicator, country)
