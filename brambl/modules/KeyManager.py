import os
from Crypto.Hash import BLAKE2b
from Crypto.Hash import keccak
from Crypto.Protocol.KDF import scrypt
import axolotl_curve25519 as curve
import base58
import json
from binascii import hexlify


defaultOptions = {
    'cipher': 'aes-256-ctr',
    'ivBytes': 16,
    'keyBytes': 32,
    'scrypt': {
        'dkLen': 32,
        'n': 2**18,
        'r': 8,
        'p': 1
    }
}


def isFunction(f):
    return callable(f)

def str2pybuf(string,enc):
    if type(string) == 'str':
        string2 = bytes(string)

    if enc == 'base58':
        return base58.b58decode(string)


def getMAC(derivedKey,ciphertext):
    keccak256 = keccak.new(digest_bits=256)
    keccak256.update(derivedKey[16:]+str2pybuf(ciphertext,'base58'))
    return keccak256.digest()

key = scrypt('password','salt',32,N=2**14,r=8,p=1)

MUC = getMAC(key,'ststsadf')
print(hexlify(MUC))

class KeyManager():

    def __init__(self,params):
        self.params = params
        try:
            self.password = params['password']
        except:
            raise Exception('A password must be provided.')

        def initKeyStorage(keyStorage,password):
            self.pk = keyStorage['publicKeyId']
            self.isLocked = False
            self.password = password
            self.keyStorage = keyStorage
            #add recover if statement

        try:
            self.constants = params['constants']
        except:
            self.constants = defaultOptions

    def verify(self,publicKey,message,signature,cb):
        

        if  not isFunction(cb):
            return curve.verifySignature(publicKey,message,signature)#returns 0 if verified
        cb(curve.verifySignature(publicKey,message,signature))
        
    

new = KeyManager({'password': 'pasz'})









        









