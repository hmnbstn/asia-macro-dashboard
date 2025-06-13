import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Charger les données
def load_data(indicator):
    """Charge les données CSV de l’indicateur spécifié."""
    file_path = f"data/{indicator}.csv"
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"❌ Fichier {file_path} introuvable.")
        return None

# Initialiser l’application Dash
app = dash.Dash(__name__)

# Charger les données principales
df_gdp = load_data("gdp")
df_inflation = load_data("inflation")
df_unemployment = load_data("unemployment")

# Créer la mise en page du dashboard
app.layout = html.Div([
    html.H1("📊 Dashboard Macroéconomique Asiatique"),
    
    dcc.Graph(
        id="gdp-chart",
        figure=px.line(df_gdp, x="date", y="value", color="country", title="Évolution du PIB")
    ),

    dcc.Graph(
        id="inflation-chart",
        figure=px.line(df_inflation, x="date", y="value", color="country", title="Inflation annuelle")
    ),

    dcc.Graph(
        id="unemployment-chart",
        figure=px.line(df_unemployment, x="date", y="value", color="country", title="Taux de chômage")
    )
])

# Lancer le serveur Dash
if __name__ == "__main__":
    app.run_server(debug=True)
