import os
import sys
import datetime
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


def str2pybuf(string,enc='base58'):#works
    if type(string) == 'str':
        string2 = bytes(string)

    if enc == 'base58':
        return base58.b58decode(string)


def encrypt(plaintext,key,iv,algo):
    iv = int(hexlify(iv).decode('utf-8'),16)
    if algo == 'aes-256-ctr':
        key = bytearray(key)
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        ciphertext = aes.encrypt(plaintext)
        return ciphertext

        
def decrypt(ciphertext,key,iv,algo):
    iv = int(hexlify(iv).decode('utf-8'),16)
    if algo == 'aes-256-ctr':
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        return aes.decrypt(ciphertext)


def getMAC(derivedKey,ciphertext):
    keccak256 = keccak.new(digest_bits=256)
    keccak256.update(derivedKey[16:32] + ciphertext)
    return keccak256.digest()





def create(params):
    keyBytes = params['keyBytes']
    ivBytes = params['ivBytes']
    
    def bifrostBlake2b(Buffer):
        blake = BLAKE2b.new(digest_bits=256)
        return blake.update(Buffer).digest()

    def curve25519KeyGen(randomBytes): # works
        seed = bifrostBlake2b(randomBytes)
        sk = curve.generatePrivateKey(seed)
        pk = curve.generatePublicKey(sk)
        return {
            'publicKey': pk,
            'privateKey': sk,
            'iv': bifrostBlake2b(get_random_bytes(keyBytes + ivBytes + keyBytes))[:ivBytes],
            'salt': bifrostBlake2b(get_random_bytes(keyBytes + ivBytes))
        }

    return curve25519KeyGen(get_random_bytes(keyBytes + ivBytes + keyBytes))



def deriveKey(password,salt,kdfParams):#creates a 44 byte key?
    if type(password) == 'undefined' or password == None or not salt:
        raise Exception("Must provide password and salt to derive a key")
    dkLen = kdfParams['dkLen']
    N = kdfParams['n']
    r = kdfParams['r']
    p = kdfParams['p']

    return scrypt(password,salt,dkLen,N,r,p,num_keys=1)



def marshal(derivedKey,keyObject,salt,iv,algo):
    if algo == 'aes-256-ctr':
        ciphertext = encrypt(keyObject['privateKey'],derivedKey,iv, 'aes-256-ctr')
        keyStorage = {
            'publicKeyId': base58.b58encode(keyObject['publicKey']),
            'crypto': {
                'cipher': algo,
                'cipherText': base58.b58encode(ciphertext),
                'cipherParams': {'iv': base58.b58encode(iv)},
                'mac': base58.b58encode(getMAC(derivedKey,ciphertext)),
                'kdf': 'scrypt',
                'kdfSalt': base58.b58encode(salt)
            }
        }
    return keyStorage


def dump(password,keyObject,options):
    try:
        kdfParams = options['kdfParams']
    except:
         kdfParams = options['scrypt']

    iv = keyObject['iv']
    salt = keyObject['salt']
    privateKey = keyObject['privateKey']
    publicKey = keyObject['publicKey']

    return marshal(deriveKey(password,salt,kdfParams),{'privateKey': privateKey,'publicKey':publicKey},salt,iv,options['cipher'])
    
    
def recover(password,keyStorage,kdfParams):
    
    def verifyAndDecrypt(derivedKey,iv,ciphertext,mac,algo):
        if getMAC(derivedKey,ciphertext) != mac:
            raise Exception("message authentication code mismatch")
        return decrypt(ciphertext,derivedKey,iv,algo)

    iv = str2pybuf(keyStorage['crypto']['cipherParams']['iv'])
    salt = str2pybuf(keyStorage['crypto']['kdfSalt'])
    ciphertext = str2pybuf(keyStorage['crypto']['cipherText'])
    mac = str2pybuf(keyStorage['crypto']['mac'])
    algo = keyStorage['crypto']['cipher']
   
    return verifyAndDecrypt(deriveKey(password,salt,kdfParams),iv, ciphertext, mac, algo)

   
def generateKeystoreFilename(publicKey):
    if type(publicKey) != type('string'):
        raise Exception('PublicKey must be given as a string for the filename')
    fileName = datetime.datetime.now().isoformat() + '-' + publicKey + '.json'
    return fileName.replace(':','-')


def byte2String(keyStorage):
    string = {'publicKeyId': keyStorage['publicKeyId'].decode('utf-8'),
            'crypto': {
            'cipher': keyStorage['crypto']['cipher'],
            'cipherText': keyStorage['crypto']['cipherText'].decode('utf-8'),
            'cipherParams': {'iv': keyStorage['crypto']['cipherParams']['iv'].decode('utf-8')},
            'mac': keyStorage['crypto']['mac'].decode('utf-8'),
            'kdf': keyStorage['crypto']['kdf'],
            'kdfSalt': keyStorage['crypto']['kdfSalt'].decode('utf-8')
            }
    }
    return string


def string2Bytes(keyStorage):
    Bytes = {'publicKeyId': keyStorage['publicKeyId'].encode('utf-8'),
            'crypto': {
            'cipher': keyStorage['crypto']['cipher'],
            'cipherText': keyStorage['crypto']['cipherText'].encode('utf-8'),
            'cipherParams': {'iv': keyStorage['crypto']['cipherParams']['iv'].encode('utf-8')},
            'mac': keyStorage['crypto']['mac'].encode('utf-8'),
            'kdf': keyStorage['crypto']['kdf'],
            'kdfSalt': keyStorage['crypto']['kdfSalt'].encode('utf-8')
            }
    }
    return Bytes


class KeyManager():

    def __init__(self, password, kwargs=''):
        try:
            self.password = password
        except:
            raise Exception('A password must be provided.')
        
        def initKeyStorage(keyStorage,password):
            self.pk = keyStorage['publicKeyId']
            self.isLocked = False
            self.password = password
            self.__keyStorage = keyStorage

            if self.pk: #check if public key exists
                self.__sk = recover(password, self.__keyStorage, self.constants['scrypt'])
        
        def generateKey(password):
            initKeyStorage(dump(password, create(self.constants), self.constants),password)

        def importFromFile(filePath,password):#TODO
            f = open(filePath)
            KeyStorage = json.loads(f.read())
            
            initKeyStorage(string2Bytes(KeyStorage),password)

        try:
            self.constants = params['constants']
        except:
            self.constants = defaultOptions

        initKeyStorage({'publicKeyId':'','crypto': {} }, '')

        if kwargs != '':
            try:
                importFromFile(kwargs['keyPath'],password)
            except:
                raise Exception('Error importing keyfile')
        else:
            generateKey(password)


    def verify(self,publicKey,message,signature):
        if curve.verifySignature(base58.b58decode(publicKey), message.encode('utf-8'), signature) == 0:#retunrs -1 if not verified 0 if verified
            return True
        return 'not verfied'

    def getKeyStorage(self):
        if self.isLocked:
            raise Exception('Key manager is currently locked. Please unlock and try again.')
        
        if not self.pk:
            raise Exception('A key must be initialized before using this key manager')
        
        return byte2String(self.__keyStorage)#WRAPO

    def lockKey(self):
        self.isLocked = True 

    def unlockKey(self, password):
        if not self.isLocked:
            raise Exception('The key is already unlocked')
        if password != self.password:
            raise Exception('Invalid password')
        self.isLocked = False
    
    def sign(self, message):
        if self.isLocked:
            raise Exception('The key is currently locked. Please unlock and try again.')
        return curve.calculateSignature(os.urandom(64), self.__sk, message.encode('utf-8'))

    def exportToFile(self, _keyPath):
        try:
            keyPath = _keyPath
        except:
            keyPath = 'keyfiles'
        #TODO change bytes objects to strings for export
        outfile = generateKeystoreFilename(self.pk.decode('utf-8'))
        JSON = json.dumps(self.getKeyStorage())
        outpath = os.path.join(keyPath,outfile)

        f = open(outpath, 'w')
        f.write(JSON)
        f.close()
        return outpath



















        









