import pandas as pd

def prepare_data(df, indicator):
    if "date" in df.columns and "value" in df.columns:
        df = df[["date", "value"]].dropna()
        df["date"] = pd.to_datetime(df["date"], format="%Y")
        df = df.sort_values("date")

        if indicator in ["gdp", "trade_balance"]:
            df[indicator] = df["value"] / 1_000_000_000  # convert to billions
        elif indicator in ["inflation", "unemployment", "interest_rate"]:
            df[indicator] = df["value"].round(2)
        else:
            df[indicator] = df["value"]

        df = df[["date", indicator]]
    return df
    
#       __
#    <(o )___      .---.
#     (  ._> /    / $$$ \\
#      `---'     |  ~~~  |
#     /|  |\\     \\_____/
#   hmnbstn © 2025
