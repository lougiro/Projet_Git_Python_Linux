#!/bin/bash

SESSION_NAME="dashboard_session"
SCRIPT_PATH="/home/ubuntu/Projet_Git_Python_Linux/dashboard.py"
HOST="0.0.0.0"
PORT="8050"

# ici on verifie que la session tmux existe et si oui, on la kill
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? == 0 ]; then
    # kill l'ancienne session tmux
    tmux kill-session -t $SESSION_NAME
fi

# on démarre ensuite une nouvelle session tmux et on lance le script Python
echo "Lancement du dashboard dans une nouvelle session tmux"
tmux new-session -d -s $SESSION_NAME "python3 $SCRIPT_PATH --host=$HOST --port=$PORT"
