import os
from Crypto.Hash import BLAKE2b
from Crypto.Hash import keccak
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import axolotl_curve25519 as curve
import base58
import json
from binascii import hexlify
import pyaes

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


def encrypt(plaintext,key,iv,algo):
    if algo == 'aes-256-ctr':
        cipher = pyaes.AESModeOfOperationCTR
        #cipher = pyaes.AESModeOfOperationCTR


def getMAC(derivedKey,ciphertext):
    keccak256 = keccak.new(digest_bits=256)
    keccak256.update(derivedKey[16:]+str2pybuf(ciphertext,'base58'))
    return keccak256.digest()

def create(params,cb):
    keyBytes = params['keyBytes']
    ivBytes = params['ivBytes']
    
    def bifrostBlake2b(Buffer):
        blake = BLAKE2b.new(32)
        return blake.update(Buffer).digest()

    def curve25519KeyGen(randomBytes):
        sk = curve.generatePrivateKey
        pk = curve.generatePublicKey(sk)
        return {
            'publicKey': pk,
            'privateKey': sk,
            'iv': bifrostBlake2b(get_random_bytes(keyBytes + ivBytes + keyBytes)[0:ivBytes]),
            'salt': bifrostBlake2b(get_random_bytes(keyBytes+iv))
        }

    if not isFunction(cb):
        return curve25519KeyGen(get_random_bytes(keyBytes+ivBytes+keyBytes))

    randomBytes = get_random_bytes(keyBytes+ivBytes+keyBytes)
    cb(curve25519KeyGen(randomBytes))

def deriveKey(password,salt,kdfParams,cb):
    if type(password) == 'undefined' or password == None or not salt:
        raise Exception("Must provide password and salt to derive a key")

    dkLen = kdfParams['dkLen']
    N = kdfParams['n']
    r = kdfParams['r']
    p = kdfParams['p']


    if not isFunction(cb):
        return scrypt(password,salt,dkLen,N,r,p,num_keys=1)

    cb(scrypt(password,salt,dkLen,N,r,p,num_keys=1))

def marshal(derivedKey,keyObject,salt,iv,algo):
    pass
    




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







        









