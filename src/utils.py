import json
import os
import pandas as pd

CACHE_FILE = "cache.json"

def save_cache(data):
    """Sauvegarde les données en cache pour éviter les requêtes inutiles."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_cache():
    """Charge les données du cache si disponible."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def clean_data(df):
    """Nettoie et reformate les valeurs des données API."""
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = df["value"].astype(float)
    return df

def format_value(value):
    """Formate les valeurs numériques pour les rendre lisibles."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} M"
    return f"{value:.2f}"
