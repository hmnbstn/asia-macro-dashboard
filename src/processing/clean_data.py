import pandas as pd

def prepare_data(df, indicator):
    if "date" in df.columns and "value" in df.columns:
        df = df[["date", "value"]].dropna()
        df["date"] = pd.to_datetime(df["date"], format="%Y")
        df = df.sort_values("date")
        df.rename(columns={"value": indicator}, inplace=True)
    return df
