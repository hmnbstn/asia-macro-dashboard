import requests
import pandas as pd
import json

API_URLS = {
    "GDP": "https://api.worldbank.org/v2/country/{}/indicator/NY.GDP.MKTP.CD?format=json",
    "Inflation": "https://api.worldbank.org/v2/country/{}/indicator/FP.CPI.TOTL.ZG?format=json",
    "Unemployment": "https://api.worldbank.org/v2/country/{}/indicator/SL.UEM.TOTL.ZS?format=json",
    "Trade Balance": "https://api.oecd.org/data/trade",
    "Interest Rate": "https://www.imf.org/external/datamapper/api/v1/IR"  # Nouvelle URL IMF
}

COUNTRIES = ["CN", "IN", "JP", "SG", "KR"]

def fetch_data(indicator, country_code):
    """Récupère les données macroéconomiques depuis l'API et les enregistre en CSV."""
    url = API_URLS[indicator].format(country_code)
    response = requests.get(url)

    try:
        data = response.json()
        
        # Afficher la réponse brute pour analyse
        print(f"\n🔍 Réponse API {indicator} ({country_code}) :")
        print(json.dumps(data, indent=4))  # Formatage JSON pour lecture facile

        # Vérifier si la réponse contient bien une liste exploitable
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1])
            df.to_csv(f"data/{indicator.lower()}.csv", index=False)
            print(f"✅ Données enregistrées pour {indicator} ({country_code})")
        else:
            print(f"⚠️ Format inattendu ou données introuvables pour {indicator} ({country_code})")

    except json.JSONDecodeError:
        print(f"❌ Impossible de récupérer {indicator} ({country_code}) → Vérifie l'URL API !")
    except Exception as e:
        print(f"❌ Erreur inattendue pour {indicator} ({country_code}) : {e}")

# Exécuter les appels API
for indicator in API_URLS:
    for country in COUNTRIES:
        fetch_data(indicator, country)
