from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input
import ast  # Pour convertir les strings JSON en dictionnaires Python

def clean_data(file_path):
    """Charge et nettoie un fichier CSV en extrayant les bonnes colonnes."""
    try:
        df = pd.read_csv(file_path)

        # Extraire les valeurs des colonnes mal formatées
        df["indicator"] = df["indicator"].apply(lambda x: ast.literal_eval(x)["value"] if isinstance(x, str) else x)
        df["country"] = df["country"].apply(lambda x: ast.literal_eval(x)["value"] if isinstance(x, str) else x)

        # Conserver uniquement les colonnes essentielles
        df = df[["date", "country", "value"]]

        # Transformer la date en format correct
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        return df
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage de {file_path} : {e}")
        return None

# Initialiser Dash
app = Dash(__name__)

# Nettoyer et charger les fichiers CSV
df_gdp = clean_data("data/gdp.csv")
df_inflation = clean_data("data/inflation.csv")
df_unemployment = clean_data("data/unemployment.csv")

# Ajouter une moyenne asiatique
for df in [df_gdp, df_inflation, df_unemployment]:
    if df is not None:
        df_avg = df.groupby("date")["value"].mean().reset_index()
        df_avg["country"] = "Moyenne Asie"
        df = pd.concat([df, df_avg])

# Liste des pays disponibles
available_countries = df_gdp["country"].unique()

# Interface du Dashboard
app.layout = html.Div(style={"backgroundColor": "#000", "color": "#FFF", "padding": "20px"}, children=[
    html.H1("📊 Dashboard Macroéconomique Asiatique", style={"textAlign": "center", "color": "#FF3131"}),

    # Sélecteur de pays
    html.Label("Sélectionnez un pays :", style={"color": "#FFF"}),
    dcc.Dropdown(
        id="country-filter",
        options=[{"label": country, "value": country} for country in available_countries],
        value="Moyenne Asie",
        style={"width": "50%", "margin": "auto", "color": "#000"}
    ),

    # Graphiques
    html.Div(children=[dcc.Graph(id="gdp-chart")], style={"marginTop": "40px"}),
    html.Div(children=[dcc.Graph(id="inflation-chart")], style={"marginTop": "40px"}),
    html.Div(children=[dcc.Graph(id="unemployment-chart")], style={"marginTop": "40px"})
])

# Callback pour mettre à jour les graphiques
@app.callback(
    [Output("gdp-chart", "figure"),
     Output("inflation-chart", "figure"),
     Output("unemployment-chart", "figure")],
    [Input("country-filter", "value")]
)
def update_graphs(selected_country):
    """Met à jour les graphiques selon le pays sélectionné."""
    
    # Filtrer les données pour le pays sélectionné ou la moyenne
    df_gdp_filtered = df_gdp[df_gdp["country"] == selected_country]
    df_inflation_filtered = df_inflation[df_inflation["country"] == selected_country]
    df_unemployment_filtered = df_unemployment[df_unemployment["country"] == selected_country]

    # Création des graphiques stylisés
    fig_gdp = px.line(df_gdp_filtered, x="date", y="value", title="Évolution du PIB",
                      line_shape="spline", color_discrete_sequence=["#FF3131"])
    
    fig_inflation = px.line(df_inflation_filtered, x="date", y="value", title="Inflation annuelle",
                            line_shape="spline", color_discrete_sequence=["#FF3131"])
    
    fig_unemployment = px.line(df_unemployment_filtered, x="date", y="value", title="Taux de chômage",
                               line_shape="spline", color_discrete_sequence=["#FF3131"])

    return fig_gdp, fig_inflation, fig_unemployment

# Lancer le dashboard
if __name__ == "__main__":
    app.run(debug=True)
