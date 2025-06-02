var_path=`pwd`
echo $var_path

# Exécution du script Python avec Python 3
PYTHON_SCRIPT="$var_path/bin/verify.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Exécution du script Python : $PYTHON_SCRIPT"
    python3 "$PYTHON_SCRIPT"
else
    echo "Erreur : Le fichier $PYTHON_SCRIPT n'existe pas dans le répertoire courant."
    exit 1
fi
