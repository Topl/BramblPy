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
import jks

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

def str2pybuf(string,enc='base58'):
    if type(string) == 'str':
        string2 = bytes(string)

    if enc == 'base58':
        return base58.b58decode(string)


def encrypt(plaintext,key,iv,algo):
    if algo == 'aes-256-ctr':
        key = bytearray(key)
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        ciphertext = aes.encrypt(plaintext)
        return ciphertext
        
def decrypt(ciphertext,key,iv,algo):
    if algo == 'aes-256-ctr':
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        return aes.decrypt(ciphertext).decode('utf-8')

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
    if algo == 'aes-256-ctr':
        ciphertext = encrypt(keyObject['privateKey'],derivedKey,iv)
        keyStorage = {
            'publicKeyId': base58.b58encode(keyObject['privateKey']),
            'crypto': {
                'cipher': algo,
                'ciphertext': base58.b58encode(ciphertext),
                'cipherParams': {'iv': base58.b58encode(iv)},
                'mac': base58.b58encode(getMAC(derivedKey,ciphertext)),
                'kdf': 'scrypt',
                'kdfSalt': base58.b58encode(salt)
            }
        }
    return keyStorage

def dump(password,keyObject,options,cb):
    kdfParams = option['kdfParams'] or options['scrypt']
    iv = str2pybuf(keyObject['iv'])
    salt = str2pybuf(keyObject['salt'])
    privateKey = str2pybuf(keyObject['privateKey'])
    publicKey = str2pybuf(keyObject['publicKey'])
    if not isFunction(cb):
        return marshal(deriveKey(password,salt,kdfParams),{'privateKey': privateKey,'publicKey':publicKey},salt,iv,options['cipher'])
    
    return cb(marshal(deriveKey(password,salt,kdfParams),{'privateKey': privateKey,'publicKey':publicKey},salt,iv,options['cipher']))


def recover(password,keyStorage,kdfParams,cb):
    
    def verifyAndDecrypt(derivedKey,iv,ciphertext,mac,algo):
        if getMAC(derivedKey,ciphertext) != mac:
            raise Exception("message authentication code mismatch")
        return decrypt(ciphertext,derivedKey,iv,algo)

    iv = str2pybuf(keyStorage['crypto']['cipherParams']['iv'])
    salt = str2pybuf(keyStorage['crypto']['kdfSalt'])
    ciphertext = str2pybuf(keyStorage['crypto']['cipherText'])
    mac = str2pybuf(keyStorage['crypto']['mac'])
    algo = str2pybuf(keyStorage['crypto']['cipher'])

    if not isFunction(cb):
        return verifyAndDecrypt(deriveKey(password,salt,kdfParams),iv, ciphertext, mac, algo)

    return cb(verifyAndDecrypt(deriveKey(password,salt,kdfParams),iv, ciphertext, mac, algo))

def generateKeystoreFilename(publicKey):
    pass
    #TODO: I am unsure how to  implement the python javascripy key module
    
 
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
            #add sk
            #add recover if statement


        try:
            self.constants = params['constants']
        except:
            self.constants = defaultOptions

    def verify(self,publicKey,message,signature,cb):
        if  not isFunction(cb):
            return curve.verifySignature(publicKey,message,signature)#returns 0 if verified
        cb(curve.verifySignature(publicKey,message,signature))

    def lockKey():
        self.isLocked = True 
    
    def sign(message):
        if self.isLocked:
            raise Exception('The key is currently locked. Please unlock and try again.')
        return curve.calculateSignature(os.urandom(64),sk,message)







        









