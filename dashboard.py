import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "exchange_rates.csv") 

now = datetime.datetime.now() # date d'ajd
ajd = now.date() # en bon format
hier = ajd - datetime.timedelta(days=1) # date d'hier en enlevant 1j

### PARTIE TRAITEMENT DE DONNEES

# Charger les données
df = pd.read_csv(CSV_PATH, names=["Timestamp", "Rate"], parse_dates=["Timestamp"])

derniere_val = df["Rate"].iloc[-1] # on recupere la derniere valeure pour afficher la derniere valeur recupérée

if now.hour < 20 :
    derniere_date = hier # on prend les données d'hier pour le rapport si il est avant 20h
else:
    derniere_date = ajd # a partir de 20h on prend celles d'ajd


df_du_dernier_jour = df[(df["Timestamp"].dt.date == derniere_date) & (df["Timestamp"].dt.hour < 20)] # et ici on récupere toutes les données de cette derniere date (sur toute la journée)
# dt.date sert converti end ate sans heure
print(df_du_dernier_jour)
if not df_du_dernier_jour.empty: # si le fichier n'est pas vide
    # Compute daily report metrics
    open_price = df_du_dernier_jour["Rate"].iloc[0] # on prend le prix d'ouverture (prmeier prix du jour)
    close_price = df_du_dernier_jour["Rate"].iloc[-1] # et le dernier prix du jour
    rates = df_du_dernier_jour["Rate"].astype(float).to_numpy()
    mean_rate = sum(rates) / len(rates)
    variance = sum((r - mean_rate)**2 for r in rates) / len(rates)
    daily_volatility = (variance**0.5) * 100  # écart-type "manuel" et *100 pour etre en pourcentage et qu'on le voit aussi
    daily_evolution = ((close_price - open_price) / open_price) * 100
else:
    open_price = close_price  = daily_volatility = daily_evolution = None

date_dernier_jour_joli = derniere_date.strftime("%Y-%m-%d")

heure_derniere_prise = df["Timestamp"].iloc[-1].strftime("%H:%M:%S") # heure de la derniere prise


### PARTIE DASHBOARD 

app = dash.Dash(__name__)
app.title = " Dashboard change EUR/USD"

app.layout = html.Div( # Dash apps are composed of two parts. The first part is the "layout", which describes what the app looks like
    
    style={
        "backgroundColor": " rgb(220, 154, 182)", # rose
        #"color": "light grey",
        #"fontFamily": "Aptos",
        "padding": "15px",
        #"textAlign": "center"
    },

    children=[
    # on met ici notre titre
    html.H1("Évolution du taux de change EUR/USD avec une récupération toutes les 5 minutes ", style = {"color" : "white", 
                "textAlign": "center", "textDecoration": "underline"}),

    html.Div([
            html.H3("Taux de change actuel :", style={"marginTop": "20px", "color": "white"}),
            html.Div(f"{derniere_val:.4f} EUR/USD", id="current-price", style={
                "fontSize": "60px",
                "fontWeight": "bold",
                "color": "white", 
                "marginTop": "10px",
                "textAlign": "center",
                "border": "3px solid white",  
                "borderRadius": "10px"
            }),
            html.P(f"Dernière mise à jour : {heure_derniere_prise}", style={ # on affiche aussi l'heure de la derniere prise
                "marginTop": "10px",
                "color": "white",
                "fontStyle": "italic"
            })
        ]),

    html.P("ici on vous affiche le graphe de l'évolution du taux de change pris toutes les 5min:", style={"marginTop": "20px", "color": "white","fontSize": "20px"}),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                go.Scatter(x=df["Timestamp"], y=df["Rate"], mode='lines', name='EUR/USD')
            ],
            'layout': go.Layout(title='Taux de change EUR/USD', xaxis=dict(title='Temps'), yaxis=dict(title='Taux'))
        }
    ),


    html.H2(f"Rapport journalier - {date_dernier_jour_joli}", style={"marginTop": "20px", "textDecoration": "underline"}),

        html.Div([
            html.P(f" Open Price: {open_price:.4f} EUR/USD" ), # on affiche les prix correpondant
            html.P(f" Close Price: {close_price:.4f} EUR/USD" ), # fermeture
            html.P(f" Daily Volatility: {daily_volatility:.2f}%"), # la vol
            html.P(f" Daily Evolution: {daily_evolution:.2f}%"), # l'evolution
        ], style={
            "border": "2px solid white",
            "padding": "15px", 
            "borderRadius": "10px", # arrondie
            "backgroundColor": "rgba(255, 255, 255, 0.2)",
            "display": "inline-block",
            "textAlign": "left"
        }),
])



# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
