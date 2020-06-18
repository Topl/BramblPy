from Crypto.Hash import BLAKE2b
from Crypto.Hash import keccak
import axolotl_curve25519 as curve
import base58
import json


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

 


new = KeyManager({'password': 'pasz'})

print(new.constants)








        









