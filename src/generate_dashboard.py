import pandas as pd

TEMPLATE = """
<html>
<head>
    <title>Asia Macro Dashboard</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <h1>Asia Macro Dashboard</h1>
    <img src="assets/logo.gif" width="150">
    <h2>Indicateurs Macroéconomiques</h2>
    {tables}
</body>
</html>
"""

def generate_dashboard():
    """Génère un fichier HTML contenant les indicateurs économiques."""
    tables_html = ""
    for file in ["gdp.csv", "inflation.csv", "unemployment.csv", "trade_balance.csv", "interest_rate.csv"]:
        df = pd.read_csv(f"data/{file}")
        tables_html += f"<h3>{file.replace('.csv', '').upper()}</h3>"
        tables_html += df.to_html()

    html_content = TEMPLATE.replace("{tables}", tables_html)
    with open("index.html", "w") as f:
        f.write(html_content)

generate_dashboard()
