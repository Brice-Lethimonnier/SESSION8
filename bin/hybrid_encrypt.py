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
from Crypto.Util.Padding import pad
import base64

#----------------------------Fonction jsonfile-------------------
#permet de mettre en forme le fichier JSON
#Argument : ciphertext : text chiffré, enc_key : clée AES chiffré,enc_iv : iv chiffré,pubkey_hash cle haché , signature : signature du text chiffré , pubkey_signature : clée publique de signature
#-----------------------------------------------------------------
def jsonfile(ciphertext,enc_key,enc_iv,pubkey_hash,signature,pubkey_signature):
    jso = json.dumps({"ciphertext" : ciphertext,"enc_key" : enc_key,"enc_iv" : enc_iv,"pubkey_hash" : pubkey_hash,"signature" : signature, "pubkey_signature" : pubkey_signature, "algos": {"symmetric": "AES-256-GCM","asymmetric": "RSA-2048","hash": "SHA-256"}}, indent=4)
    with open("secure_message.json","w") as file:
        file.write(jso)


#----------------------------chiffr_fich-------------------
#permet de chiffrer le contenu du fichier
#parametre le fichier a chiffrer
#retourne : la clé de chiffrement AES, iv ,les données chiffrées et le tag
#-----------------------------------------------------------------
def Chiffr_fich(input_file):
    key = os.urandom(32)
    iv = os.urandom(AES.block_size)
    #print(key,iv)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        padded_plaintext = pad(plaintext,AES.block_size)
        ciphertext, tag = cipher.encrypt_and_digest(padded_plaintext)
        return key, iv,[ciphertext,tag]
    except Exception as e:
        print(f"Defaut lors du chiffrement : {e}")
        return None, None,None


#----------------------------chiffr_key_iv-------------------
#permet de chiffrer la clée et iv
#parametre la clé de chiffrement AES et iv et le fichierde la clé public de chiffrement RSA
#retourne : la clé AES chiffrée et l'iv chiffré
#-----------------------------------------------------------------
def Chiffr_key_iv(key,iv,file_keyPublic):
    key_pub = RSA.importKey(open(file_keyPublic).read())
    cipher = PKCS1_OAEP.new(key_pub)
    cipherkey = cipher.encrypt(key)
    cipheriv = cipher.encrypt(iv)
    return cipherkey,cipheriv


#----------------------------Hash_pubkey-------------------
#permet de hacher la clé public
#parametre le fichier de la clé public
#retourne : le hash de la clé public en base64
#-----------------------------------------------------------------
def Hash_pubkey(file_KP):
    with open(file_KP,"rb") as file:
        key_pub = file.read()
        sha_sign = SHA256.new(key_pub)
        return _base64(bytearray(sha_sign.digest()))

#----------------------------Gener_key()-------------------
#permet de générer les clées
#parametre
#retourne : 
#-----------------------------------------------------------------
def Gener_Key():
    rng = Random.new().read
    RSAKey = RSA.generate(2048)
    f = open("keyPrivateSign.der","wb")
    f.write(RSAKey.exportKey())
    f.close()
    f = open("keyPublicSign.pem","wb")
    f.write(RSAKey.publickey().exportKey("PEM"))
    f.close()
    
#----------------------------sign()-------------------
#permet de signer le hash avec la clé priver de siganture
#parametre les données chiffrées et la clé privée de signature
#retourne : la signature du hash avec la clé privée
#-----------------------------------------------------------------
def sign(cip_test,keypriv):
    sha_ciper_text = SHA256.new(cip_test)
    #print(cip_test)
    key_priv = RSA.import_key(open(keypriv).read())
    return pss.new(key_priv).sign(sha_ciper_text)

def hybrid_encrypt(file, KeyPub,keyPri,KeyPubSign) :
    if os.path.exists(file):
        with open(file, "r") as fich:
            print ("le fichier existe")
    else:
        print('fichier n\'existe pas !!')
        return(exit(1))

def _base64(donnee):
    basStr = base64.b64encode(donnee)
    return basStr.decode('utf-8')


def PubKeySign(pubKS):
    with open(pubKS,"rb") as file:
        encodeFPKS = _base64(file.read())
    return encodeFPKS

#----------------------------fonction principale-------------------
#permet de chiffrer la clée et iv
#parametre les arguments : argument 0 : fichier a chiffrer,
#retourne : la clé AES chiffrée et l'iv chiffré,clé public, clé privée de signature et la clée publique de signature
#-----------------------------------------------------------------
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 2 :
        hybrid_encrypt(args[0],args[1],args[2],args[3])
        val1,val2,[val3,tag] = Chiffr_fich(args[0])
        key,iv = Chiffr_key_iv(val1,val2,args[1])
        jsonfile(_base64(val3+b'tag='+tag),_base64(key),_base64(iv),Hash_pubkey(args[1]),_base64(sign(val3+b'tag='+tag,args[2])),PubKeySign(args[3]))
        print('fichier JSON créé : secure_message.json')
        
    else:
        if len(args) == 1:
            print("un seul argument la gestion des clées sera faites ici!")
            val = Chiffr_fich(args[0])
            #print(val)
            #Gener_Key()
        else:
            print('Défaut d\'arguments merci de fournir en argument le fichier a chiffrer !! arret')
            exit(1)
