import os
from Crypto.Cipher import AES
import axolotl_curve25519 as curve
import base58
import json

#curve25519 Test
class keyPair():
    def __init__(self):
        self.privateKey = curve.generatePrivateKey(os.urandom(32))#32 bit key
        self.publicKey = curve.generatePublicKey(self.privateKey)

def signData(privKey,message):
    return curve.calculateSignature(os.urandom(64),privKey,base58.b58encode(message))
            

def verify(pubKey,message, signature):
    verified = curve.verifySignature(pubKey,base58.b58encode(message),signature)
    if verified == 0:#return 0 if verified
        return True
    else:
        return False

#AES Test
def gencipher(algorithm,key, message):
    if algorithm != 'aes-256-ctr':
        raise Exception('Algorithm not supported')

    cipher = AES.new(key,AES.MODE_CTR)#create AES object
    data = message.encode('utf-8')#change to byte format
    ct_bytes = cipher.encrypt(data)

    nonce = base58.b58encode(cipher.nonce).decode('utf-8')#nonce must be JSON serializable
    ct = base58.b58encode(ct_bytes).decode('utf-8')

    result = json.dumps({'nonce':nonce,'ciphertext':ct})#JSON to send over web
    return result


def genDecipher(key,cipher):
    b58 = json.loads(cipher)
    nonce = base58.b58decode(b58['nonce'])#decode to original 
    ct = base58.b58decode(b58['ciphertext'])

    decipher = AES.new(key,AES.MODE_CTR,nonce=nonce)#new Cipher object
    pt = (decipher.decrypt(ct)).decode('utf-8')#decrypt message, change to string
    return pt

