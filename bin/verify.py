import sys
import os
import json

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Signature import pss
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad,unpad
import base64


def pad_message(message):
  while len(message) % 32 != 0:
    message = message + " "
  return message

def read_bytes(file_path):
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except:
        print(f"Error reading file {file_path}")
        sys.exit(1)

def write_bytes(file_path, data):
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except:
        print(f"Error writing to file {file_path}")
        sys.exit(1)


#-----------------------------verif_sign------------------------
#permet de vérifier la signature
#parametre : le fichier JSON
#retourne : vrai si la signature est vérifiée sinon faux
def verif_sign(fichJson):
    jsonFile = open(fichJson,'r').read()
    donnees = json.loads(jsonFile)
    rsakeyP = RSA.importKey(_base64_dec(donnees['pubkey_signature']).decode('utf-8'))
    has = SHA256.new(_base64_dec(donnees['ciphertext']))
    verif = pss.new(rsakeyP)
    try:
        verif.verify(has,_base64_dec(donnees['signature']))
        print('Signature authentique')
        return True
    except(ValueError):
        print('Erreur de verification')
        return False

#-------------decod_fich-----------------------------
#permet de dechiffrer le text chiffré
#parametre : le fichier JSON, la clé privée permetant de retrouver la clé de chifrement du text , le fichier de sortie 
#
def decod_fich(JsonFile,KeyPrivate,fileOut):
    json_file = open(JsonFile,'r').read()
    donnees = json.loads(json_file) # lecture JSON
    key_priv = RSA.importKey(read_bytes(KeyPrivate)) # lecutre de la private key
    cipher = PKCS1_OAEP.new(key_priv)
    key = cipher.decrypt(_base64_dec(donnees['enc_key']))
    iv = cipher.decrypt(_base64_dec(donnees['enc_iv']))
    cipher = AES.new(key, AES.MODE_GCM, iv)
    Message_tag = cipher.decrypt(_base64_dec(donnees['ciphertext']))
    indDebTag = _base64_dec(donnees['ciphertext']).find(b"tag=")  # récuperer le tag du chiffrement AES
    Message = Message_tag[0:indDebTag - (len(_base64_dec(donnees['ciphertext']))+4)]
    print(_base64_dec(donnees['ciphertext'])[indDebTag:])
    write_bytes(fileOut,Message)


#---------_base64_dec---------------------------------------------------
# permet de décoder les données base64
#parametre : les données
#
def _base64_dec(donneCod64):
    basDec = donneCod64.encode('utf-8')
    return base64.b64decode(basDec)


#--------------fichier principale
#
#
if __name__ == '__main__':
    if verif_sign('.\\secure_message.json'):
        decod_fich('.\\secure_message.json','keyPrivate.der','messageO.txt')
