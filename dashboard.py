import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
import datetime
import os
print("Dossier actuel :", os.getcwd())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "exchange_rates.csv") 

### PARTIE TRAITEMENT DE DONNEES

# Charger les données
df = pd.read_csv(CSV_PATH, names=["Timestamp", "Rate"], parse_dates=["Timestamp"])

derniere_val = df["Rate"].iloc[-1] # on recupere la derniere valeure

# Vérifier que le dataframe a au moins 2 valeurs avant de comparer
if len(df) > 1 and df["Rate"].iloc[-1] > df["Rate"].iloc[-2]:
    graph_color = "red"  
else:
    graph_color = "green"  


latest_date = (df["Timestamp"].max()).date()

# Filter data for the latest full trading day
daily_df = df[df["Timestamp"].dt.date == latest_date]

if not daily_df.empty:
    # Compute daily report metrics
    open_price = daily_df["Rate"].iloc[0]
    close_price = daily_df["Rate"].iloc[-1]
    high_price = daily_df["Rate"].max()
    low_price = daily_df["Rate"].min()
    daily_volatility = ((high_price - low_price) / open_price) * 100
    daily_evolution = ((close_price - open_price) / open_price) * 100
else:
    open_price = close_price = high_price = low_price = daily_volatility = daily_evolution = None

report_date = latest_date.strftime("%Y-%m-%d")

### PARTIE DASHBOARD 

app = dash.Dash(__name__)
app.title = " Dashboard change EUR/USD"

app.layout = html.Div( # Dash apps are composed of two parts. The first part is the "layout", which describes what the app looks like
    
    style={
        "backgroundColor": " rgb(220, 154, 182)",
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
            })
        ]),


    html.Div(id="live-update-price", style={
            "fontSize": "50px",
            "fontWeight": "bold",
            "color": "#00FF00",  # Vert si positif
            "marginTop": "20px",
        }),

    html.P("ici on vous affiche l'évolution du taux de change pris toutes les 5min:", style={"marginTop": "20px", "color": "white"}),
    dcc.Graph(
        id='graph',
        figure={
            'data': [
                go.Scatter(x=df["Timestamp"], y=df["Rate"], mode='lines', name='EUR/USD')
            ],
            'layout': go.Layout(title='Taux de change EUR/USD', xaxis=dict(title='Temps'), yaxis=dict(title='Taux'))
        }
    ),


    html.H2(f"Daily Report - {report_date}", style={"marginTop": "20px", "textDecoration": "underline"}),

        html.Div([
            html.P(f" Open Price: {open_price:.4f} EUR/USD" if open_price else "📌 Open Price: Data not available"),
            html.P(f" Close Price: {close_price:.4f} EUR/USD" if close_price else "📌 Close Price: Data not available"),
            html.P(f" High Price: {high_price:.4f} EUR/USD" if high_price else "📌 High Price: Data not available"),
            html.P(f" Low Price: {low_price:.4f} EUR/USD" if low_price else "📌 Low Price: Data not available"),
            html.P(f" Daily Volatility: {daily_volatility:.2f}%" if daily_volatility else "📊 Daily Volatility: Data not available"),
            html.P(f" Daily Evolution: {daily_evolution:.2f}%" if daily_evolution else "📈 Daily Evolution: Data not available"),
        ], style={
            "border": "2px solid white",
            "padding": "15px",
            "borderRadius": "10px",
            "backgroundColor": "rgba(255, 255, 255, 0.2)",
            "display": "inline-block",
            "textAlign": "left"
        }),
])



# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
