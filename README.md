
# asia-macro-dashboard/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── fetch_data.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── clean_data.py
│   └── dashboard.py
├── data/
├── assets/
├── main.py
├── requirements.txt
└── README.md

"""
# 🌏 Asia Macro Dashboard

Streamlit dashboard to track real-time macroeconomic indicators:
- Countries: China, Japan, Hong Kong, Singapore, South Korea
- Indicators: GDP, Inflation, Unemployment, Interest Rate, Trade Balance

## ⚙️ How to run the project

```bash
pip install -r requirements.txt
streamlit run main.py
```

## ☁️ Deployment
Deployable on Streamlit Cloud: [https://streamlit.io/cloud](https://streamlit.io/cloud)

Add your API key `NINJA_API_KEY` in a `.env` file for interest rate data.

"""
