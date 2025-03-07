import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

import os
print("Dossier actuel :", os.getcwd())

import pandas as pd
import os
import os
import pandas as pd

# Assurez-vous que `BASE_DIR` est bien `Project/`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "exchange_rates.csv")  # Supprimez le double "Project"

print(f"📂 Chemin utilisé : {CSV_PATH}")  # Ajout d'un print pour vérifier

# Charger les données
df = pd.read_csv(CSV_PATH, names=["Timestamp", "Rate"], parse_dates=["Timestamp"])

# Créer l'application Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Évolution du taux de change EUR/USD"),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                go.Scatter(x=df["Timestamp"], y=df["Rate"], mode='lines', name='EUR/USD')
            ],
            'layout': go.Layout(title='Taux de change EUR/USD', xaxis=dict(title='Temps'), yaxis=dict(title='Taux'))
        }
    )
])

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
