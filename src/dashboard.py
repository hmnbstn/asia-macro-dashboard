import streamlit as st
import pandas as pd
import plotly.express as px

from src.api.fetch_data import fetch_indicator
from src.processing.clean_data import prepare_data

def run_dashboard():
    st.set_page_config(page_title="Asia Macro Dashboard", layout="wide")
    st.title("📈 Asia Macro Dashboard")

    country = st.sidebar.selectbox("Select a country", ["China", "Japan", "Hong Kong", "Singapore", "South Korea"])
    indicators = st.sidebar.multiselect("Select macroeconomic indicators", ["gdp", "inflation", "unemployment", "interest_rate", "trade_balance"], default=["gdp"])

    for indicator in indicators:
        df = fetch_indicator(country, indicator)
        df = prepare_data(df, indicator)

        if not df.empty:
            st.subheader(f"{indicator.capitalize()} - {country}")
            fig = px.line(df, x="date", y=indicator, title=f"{indicator.capitalize()} Over Time")
            st.plotly_chart(fig, use_container_width=True)
