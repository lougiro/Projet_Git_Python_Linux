#!/bin/bash

# defini le dossier ou on va enregistrer le csv
GIT_DIR = "/home/ubuntu/Projet_Git_Python_Linux"

# fichier csv avec toutes les données
OUTPUT_FILE = "$GIT_DIR/exchange_rates.csv"

#^page à scraper
URL = "https://www.investing.com/currencies/eur-usd"

# taux de change ave ccurl et grep
RATE = $(curl -s "$URL" | grep -oP '(?<=data-test="instrument-price-last">)[0-9]+\.[0-9]+')

# Vérifier si une valeur a été récupérée
if [[ -n "$RATE" ]]; then
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP,$RATE" >> "$OUTPUT_FILE"
    echo "[$TIMESTAMP] Taux de change EUR/USD : $RATE (enregistré dans $OUTPUT_FILE)"
else
    echo "Erreur : Impossible de récupérer le taux de change."
fi
