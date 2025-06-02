#!/bin/bash

# Vérification ou création des clés SSH
KEY_PATH1="./SESSION8/.ssh/key"

if [ ! -f "$KEY_PATH1" ]; then
    echo "Clé SSH non trouvée. Création d'une nouvelle paire de clés..."
    ssh-keygen -t rsa -b 2048 -f "$KEY_PATH1" -N ""
    echo "Clé SSH générée avec succès : $KEY_PATH1"
else
    echo "Clé SSH déjà existante : $KEY_PATH1"
fi

# Vérification ou création des clés SSH
KEY_PATH_Sig="./SESSION8/.ssh/keySign"

if [ ! -f "$KEY_PATH2" ]; then
    echo "Clé SSH non trouvée. Création d'une nouvelle paire de clés..."
    ssh-keygen -t rsa -b 2048 -f "$KEY_PATH2" -N ""
    echo "Clé SSH générée avec succès : $KEY_PATH2"
else
    echo "Clé SSH déjà existante : $KEY_PATH2"
fi

# Exécution du script Python avec Python 3
PYTHON_SCRIPT="./SESSION8/bin/hybrid_encrypt.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Exécution du script Python : $PYTHON_SCRIPT"
    python3 "$PYTHON_SCRIPT "
else
    echo "Erreur : Le fichier $PYTHON_SCRIPT n'existe pas dans le répertoire courant."
    exit 1
fi
