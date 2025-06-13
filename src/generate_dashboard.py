from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

# Charger les données
def load_data(indicator):
    """Charge les données CSV de l’indicateur et ajoute une moyenne globale."""
    file_path = f"data/{indicator}.csv"
    try:
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])  # Assurer un bon format de date
        df["country"] = df["country"].astype(str)
        
        # Calculer la moyenne de l'indicateur pour tous les pays
        df_avg = df.groupby("date")["value"].mean().reset_index()
        df_avg["country"] = "Moyenne Asie"
        
        return pd.concat([df, df_avg])  # Ajouter la moyenne aux données
    except FileNotFoundError:
        print(f"❌ Fichier {file_path} introuvable.")
        return None

# Initialiser Dash avec un thème Bootstrap
app = Dash(__name__)

# Charger les datasets
df_gdp = load_data("gdp")
df_inflation = load_data("inflation")
df_unemployment = load_data("unemployment")

# Liste des pays disponibles pour le filtre interactif
available_countries = df_gdp["country"].unique()

# Mise en page du dashboard
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

    # Graphique PIB
    html.Div(children=[
        dcc.Graph(id="gdp-chart")
    ], style={"marginTop": "40px"}),

    # Graphique Inflation
    html.Div(children=[
        dcc.Graph(id="inflation-chart")
    ], style={"marginTop": "40px"}),

    # Graphique Chômage
    html.Div(children=[
        dcc.Graph(id="unemployment-chart")
    ], style={"marginTop": "40px"})
])

# Callback pour mettre à jour les graphiques dynamiquement
@app.callback(
    from dash.dependencies import Output, Input
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

# Lancer le serveur Dash
if __name__ == "__main__":
    app.run(debug=True)
