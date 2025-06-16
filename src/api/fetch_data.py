import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = "data"
API_URLS = {
    "gdp": "http://api.worldbank.org/v2/country/{country}/indicator/NY.GDP.MKTP.CD?format=json&per_page=100",
    "inflation": "http://api.worldbank.org/v2/country/{country}/indicator/FP.CPI.TOTL.ZG?format=json&per_page=100",
    "unemployment": "http://api.worldbank.org/v2/country/{country}/indicator/SL.UEM.TOTL.ZS?format=json&per_page=100",
    "interest_rate": "https://api.api-ninjas.com/v1/interestrate?country={country_name}",
    "trade_balance": "http://api.worldbank.org/v2/country/{country}/indicator/NE.EXP.GNFS.CD?format=json&per_page=100"
}

COUNTRY_CODES = {
    "China": "CN",
    "Japan": "JP",
    "Hong Kong": "HK",
    "Singapore": "SG",
    "South Korea": "KR"
}

COUNTRY_NAMES = {
    "China": "China",
    "Japan": "Japan",
    "Hong Kong": "Hong Kong",
    "Singapore": "Singapore",
    "South Korea": "South Korea"
}

API_KEY = os.getenv("NINJA_API_KEY", "YLp1GfgZ1gSpSfq7FRQ3dg==dt3X4lGNY5ljnjiV")  # fallback to actual key if .env missing

def fetch_indicator(country, indicator):
    cache_file = f"{CACHE_DIR}/{country}_{indicator}.csv"
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)
    
    if indicator == "interest_rate":
        url = API_URLS[indicator].format(country_name=COUNTRY_NAMES[country])
        headers = {"X-Api-Key": API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        df = pd.DataFrame(data)
    else:
        url = API_URLS[indicator].format(country=COUNTRY_CODES[country])
        response = requests.get(url)
        json_data = response.json()
        records = json_data[1] if len(json_data) > 1 else []
        df = pd.DataFrame(records)

    os.makedirs(CACHE_DIR, exist_ok=True)
    df.to_csv(cache_file, index=False)
    return df
