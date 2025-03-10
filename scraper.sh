#!/bin/bash

# Définir le dossier où enregistrer le fichier CSV (GitHub)
GIT_DIR="$HOME/OneDrive/Bureau/ESILV/A4/S8/Python/Projet_Git_Python_Linux"

# Vérifier si le dossier GitHub existe
if [ ! -d "$GIT_DIR" ]; then
    echo "Erreur : Le dossier GitHub n'existe pas ! Vérifiez le chemin."
    exit 1
fi

# Définir le fichier CSV dans le dossier GitHub
OUTPUT_FILE="$GIT_DIR/exchange_rates.csv"

# URL de la page à scraper
URL="https://www.investing.com/currencies/eur-usd"

# Scraping du taux de change
RATE=$(curl -s "$URL" | grep -oP '(?<=data-test="instrument-price-last">)[0-9]+\.[0-9]+')

# Vérifier si une valeur a été récupérée
if [[ -n "$RATE" ]]; then
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$TIMESTAMP,$RATE" >> "$OUTPUT_FILE"
    echo "[$TIMESTAMP] Taux de change EUR/USD : $RATE (enregistré dans $OUTPUT_FILE)"
else
    echo "Erreur : Impossible de récupérer le taux de change."
fi
