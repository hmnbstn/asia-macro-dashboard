import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

from src.api.fetch_data import fetch_indicator
from src.processing.clean_data import prepare_data

def run_dashboard():
    st.set_page_config(page_title="Asia Macro Dashboard", layout="wide")  # MUST be first Streamlit command

    # Logo display
    logo = Image.open("assets/logo.gif")
    st.image(logo, width=80)
    st.title("📈 Asia Macro Dashboard")

    country = st.sidebar.selectbox("Select a country", ["China", "Japan", "Hong Kong", "Singapore", "South Korea"])
    indicators = st.sidebar.multiselect(
        "Select macroeconomic indicators",
        ["gdp", "inflation", "unemployment", "interest_rate", "trade_balance"],
        default=["gdp"]
    )

    indicator_labels = {
        "gdp": "GDP (Billion USD)",
        "inflation": "Inflation (%)",
        "unemployment": "Unemployment Rate (%)",
        "interest_rate": "Interest Rate (%)",
        "trade_balance": "Trade Balance (Billion USD)"
    }

    for indicator in indicators:
        df = fetch_indicator(country, indicator)
        df = prepare_data(df, indicator)

        if not df.empty:
            label = indicator_labels[indicator]
            st.subheader(f"{label} — {country}")
            fig = px.line(
                df,
                x="date",
                y=indicator,
                title=label,
                template="plotly_dark",
                line_shape="linear"
            )
            fig.update_traces(line=dict(color="red"))  # Neon red-style
            st.plotly_chart(fig, use_container_width=True)
