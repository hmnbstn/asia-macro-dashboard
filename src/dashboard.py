import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

from src.api.fetch_data import fetch_indicator
from src.processing.clean_data import prepare_data

def run_dashboard():
    st.set_page_config(page_title="Asia Macro Dashboard", layout="wide")

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

    if indicators:
        st.markdown("### Latest Indicators")
        cols = st.columns(len(indicators))
        for i, indicator in enumerate(indicators):
            df = fetch_indicator(country, indicator)
            df = prepare_data(df, indicator)

            if not df.empty:
                latest_value = df[indicator].iloc[-1]
                latest_year = df["date"].dt.year.iloc[-1]
                label = indicator_labels[indicator]
                formatted_value = f"{latest_value:,.2f}" if indicator in ["gdp", "trade_balance"] else f"{latest_value:.2f}%"
                cols[i].metric(label, formatted_value, f"Year: {latest_year}")

        st.markdown("---")

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
            fig.update_traces(line=dict(color="red"))
            st.plotly_chart(fig, use_container_width=True)

    # Optional: Show regional map for one selected indicator
    if len(indicators) == 1 and st.checkbox("Show Map", value=False):
        indicator = indicators[0]
        values, iso3, lats, lons = [], [], [], []

        iso_mapping = {
            "China": ("CHN", 35.0, 103.0),
            "Japan": ("JPN", 36.0, 138.0),
            "Hong Kong": ("HKG", 22.3, 114.2),
            "Singapore": ("SGP", 1.3, 103.8),
            "South Korea": ("KOR", 37.6, 127.8)
        }

        for country_name in iso_mapping:
            df = fetch_indicator(country_name, indicator)
            df = prepare_data(df, indicator)
            if not df.empty:
                val = df[indicator].iloc[-1]
                code, lat, lon = iso_mapping[country_name]
                values.append(val)
                iso3.append(code)
                lats.append(lat)
                lons.append(lon)

        map_df = pd.DataFrame({
            "iso3": iso3,
            "value": values,
            "lat": lats,
            "lon": lons
        })

        st.subheader(f"Regional View — {indicator_labels[indicator]}")
        fig_map = px.scatter_geo(
            map_df,
            lat="lat",
            lon="lon",
            text="iso3",
            size="value",
            color="value",
            color_continuous_scale="reds",
            projection="natural earth",
            title="Asian Macro Indicator Map"
        )
        fig_map.update_geos(
            showland=True,
            landcolor='rgb(20, 20, 20)',
            showocean=True,
            oceancolor='rgb(10, 10, 40)',
            showlakes=True,
            lakecolor='rgb(20, 20, 60)',
            showcountries=True,
            bgcolor='rgb(0, 0, 0)',
            fitbounds="locations"
        )
        fig_map.update_layout(
            geo=dict(projection_type="natural earth"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <img src='assets/logo.gif' width='40'><br>
        <sub>Data from <a href='https://data.worldbank.org' target='_blank'>World Bank</a>,
        <a href='https://fred.stlouisfed.org/' target='_blank'>FRED</a>,
        and <a href='https://api-ninjas.com/api/interestrate' target='_blank'>API Ninjas</a></sub><br>
        <sub><b>hmnbstn</b></sub>
    </div>
    """, unsafe_allow_html=True)
