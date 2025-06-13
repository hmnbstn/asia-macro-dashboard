
""logo à ajouter""

# Asia Macro Dashboard

This project is a dynamic dashboard that tracks and visualizes key macroeconomic indicators for major Asian economies using Python.

## Features
- Real-time data fetching from public APIs (IMF, World Bank, TradingEconomics, etc.)
- Interactive charts using Plotly
- Clean layout using Dash (or Streamlit)

## Target Economies
- China 🇨🇳
- Singapore 🇸🇬
- Japan 🇯🇵
- India 🇮🇳
- South Korea 🇰🇷

## Indicators Tracked
- GDP Growth
- Inflation (CPI)
- Interest Rates
- Trade Balance
- Manufacturing/PMI Index

## Data Sources
- IMF (World Economic Outlook)
- World Bank
- Trading Economics
- Asian Development Bank
- Central Banks of respective countries

## Structure
asia-macro-dashboard/
│
├── src/                  # Python source code
│   └── main.py           # Main script to launch the dashboard
│
├── data/                 # Static or cached datasets
│   └── indicators.csv    # Optional local backup
│
├── docs/                 # Screenshots / documentation
│   └── screenshot.png
│
├── README.md             # Project overview

## Setup
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the dashboard: `python src/main.py`

## Author
[@hmnbstn](https://github.com/hmnbstn)
