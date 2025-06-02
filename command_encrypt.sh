#!/bin/bash

# Exécution du script Python avec Python 3
PYTHON_SCRIPT="./SESSION8/bin/hybrid_encrypt.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Exécution du script Python : $PYTHON_SCRIPT"
    python3 "$PYTHON_SCRIPT ./message.txt ./.ssh/keyPublic.pem /.ssh/keyPrivateSign.der /.ssh/keyPublicSign.pem"
else
    echo "Erreur : Le fichier $PYTHON_SCRIPT n'existe pas dans le répertoire courant."
    exit 1
fi
