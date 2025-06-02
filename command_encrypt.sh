#!/bin/bash

# Vérification ou création des clés SSH
var_path=`pwd`
echo $var_path
KEY_PATH1="$var_path/.ssh/key"
KEY_PATH="$var_path/.ssh/"
BIN_PATH="$var_path/bin/"
if [ ! -f "$KEY_PATH1" ]; then
    echo "Clé SSH non trouvée. Création d'une nouvelle paire de clés..."
    ssh-keygen -t rsa -b 2048 -f "$KEY_PATH1" -N ""
    echo "Clé SSH générée avec succès : $KEY_PATH1"
else
    echo "Clé SSH déjà existante : $KEY_PATH1"
fi

# Vérification ou création des clés SSH
KEY_PATH_Sig="$var_path/.ssh/keySign"

if [ ! -f "$KEY_PATH_Sig" ]; then
    echo "Clé SSH non trouvée. Création d'une nouvelle paire de clés..."
    ssh-keygen -t rsa -b 2048 -f "$KEY_PATH_Sig" -N ""
    echo "Clé SSH générée avec succès : $KEY_PATH_Sig"
else
    echo "Clé SSH déjà existante : $KEY_PATH_Sig"
fi

# Exécution du script Python avec Python 3
PYTHON_SCRIPT="$var_path/bin/hybrid_encrypt.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Exécution du script Python : $PYTHON_SCRIPT $var_path/message.txt $KEY_PATH/keyPublic.pem $KEY_PATH/keyPrivateSign.der  $KEY_PATH/keyPublicSign.pem"
    python3 "$PYTHON_SCRIPT"
else
    echo "Erreur : Le fichier $PYTHON_SCRIPT n'existe pas dans le répertoire courant."
    exit 1
fi
