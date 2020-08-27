"""
KeyManager.py
====================================
Create, import, and export Topl Bifrost keys.
Also allows for signing of transactions

Based on the keythereum library from Jack Peterson
https://github.com/Ethereumjs/keythereum
"""
# Dependencies
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



# Default options for key generation as of 2020.08.01
defaultOptions = {
    # Symmetric cipher for private key encryption
    #--- anything from crypto.getCipher() is eligible
    'cipher': 'aes-256-ctr',

    # Initialization vector size in bytes
    'ivBytes': 16,

    # Private key size in bytes
    'keyBytes': 32,

    # Key derivation function parameters
    'scrypt': {
        'dkLen': 32,
        'n': 2**18, # cost (as given in bifrost)
        'r': 8, # blocksize
        'p': 1 # parallelization
    }
}

# Generic key methods


def str2pybuf(string,enc='base58'):#works
    """
    Convert a string to a Buffer.  If encoding is not specified, bae58-encoding
    will be used if the input is valid base58.  If the input is valid base64 but
    not valid hex, base64 will be used.  Otherwise, utf8 will be used.

    :param str: String to be converted.
    :param enc: Encoding of the input string (optional), defaults to base58.
    :type str: string  
    :type enc: string
    :return: An object containing the input data.
    :rtype: bytes
    """
    if type(string) == 'str':
        string2 = bytes(string)

    if enc == 'base58':
        return base58.b58decode(string)


def encrypt(plaintext,key,iv,algo):
    """
    Symmetric private key encryption using secret (derived) key.

    :param plaintext: Data to be encrypted.
    :param key: A secret key
    :param iv: initialization vector
    :param algo: Encryption algorithm (aes-256-ctr is currently supported)
    :type plaintext: string
    :type key: string
    :type iv: number
    :type algo: string
    :return: encrypted data
    :rtype: bytes

    """
    iv = int(hexlify(iv).decode('utf-8'),16)
    if algo == 'aes-256-ctr':
        key = bytearray(key)
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        ciphertext = aes.encrypt(plaintext)
        return ciphertext


def decrypt(ciphertext,key,iv,algo):
    """
    Symmetric private key decryption using secret (derived) key.

    :param ciphertext: Data to be decrypted.
    :param key: A secret key.
    :param iv: Initialization vector
    :param algo: Encryption algorithm (aes-256-ctr is currently supported)
    :type ciphertext: bytes
    :type key: string
    :type iv: number
    :type algo: string
    :return: Decrypted data
    :rtype: string

    """ 
    iv = int(hexlify(iv).decode('utf-8'),16)
    if algo == 'aes-256-ctr':
        aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
        return aes.decrypt(ciphertext)

def getMAC(derivedKey,ciphertext):
    """
    Calculate message authentication code from secret (derived) key and
    encrypted text. The MAC is the keccak-256 hash of the byte array
    formed by concatenating the second 16 bytes of the derived key with
    the ciphertext key's contents.

    :param derivedKey: Secret key derived from password
    :param ciphertext: ciphertext Text encrypted with secret key.
    :type derivedKey: string
    :type ciphertext: bytes string
    :return: Base58-encoded MAC
    :rtype: string

    """
    keccak256 = keccak.new(digest_bits=256)
    keccak256.update(derivedKey[16:32] + ciphertext)
    return keccak256.digest()


def create(params):
    """
    Generate random numbers for private key, initialization vector,
    and salt (for key derivation).

    :param params: Encryption options.
    :param params['keyBytes']: Private key size in bytes.
    :param params['ivBytes']: Initialization vector size in bytes.
    :type params: dictionary
    :type params['keyBytes']: number
    :type params['ivBytes']: number
    :return: Keys, IV and salt.
    :rtype: dictionary

    """
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

def deriveKey(password,salt,kdfParams):
    """
    Derive secret key from password with key derivation function.

    :param password: User-supplied password.
    :param salt: Randomly generated salt.
    :param kdfParams: key-derivation parameters
    :type password: string
    :type salt: number
    :type kdfParams: dictionary
    :return: Secret key derived from password.
    :rtype: string

    """
    if type(password) == 'undefined' or password == None or not salt:
        raise Exception("Must provide password and salt to derive a key")
    dkLen = kdfParams['dkLen']
    N = kdfParams['n']
    r = kdfParams['r']
    p = kdfParams['p']

    return scrypt(password,salt,dkLen,N,r,p,num_keys=1)


def marshal(derivedKey,keyObject,salt,iv,algo):
    """
    Assemble key data object in secret-storage format.

    :param derivedKey: Password-derived secret key.
    :param keyObject: Object containing the raw public / private keypair 
    :param salt: Randomly generated salt.
    :param iv: Initialization vector.
    :param algo: encryption algorithm to be used
    :type derivedKey: string
    :type keyObject: dictionary
    :type salt: number
    :type iv: number
    :type algo: string
    :return: key data object in secret-storage format
    :rtype: dictionary

    """
    # encrypt using last 16 bytes of derived key (this matches Bifrost)
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
    """
    Export private key to keystore secret-storage format.

    :param password: User-supplied password.
    :param keyObject: Object containing the raw public / private keypair 
    :param options: encryption specifications to be used
    :type password: string
    :type keyObject: dictionary
    :type options: dictionary
    :return: keyStorage for use with exportToFile
    :rtype: dictionary

    """
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
    """
    Recover plaintext private key from secret-storage key object.

    :param password: User-supplied password.
    :param keyStorage: Keystore object
    :param kdfParams: key-derivation parameters
    :type password: string
    :type keyStorage: dictionary
    :type kdfParams: dictionary
    :return: Plaintext private key
    :rtype: string

    """  
    # verify that message authentication codes match, then decrypt
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
    """
    Generate filename for a keystore file.

    :param publicKey: Topl address
    :type publicKey: string
    :return: Keystore filename
    :rtype: string

    """
    if type(publicKey) != type('string'):
        raise Exception('PublicKey must be given as a string for the filename')
    fileName = datetime.datetime.now().isoformat() + '-' + publicKey + '.json'
    return fileName.replace(':','-')


def byte2String(keyStorage):
    """
    Converts bytes types to string

    :param keyStorage: keyStorage object
    :type keyStorage: dictionary
    :return: dictionary containing string versions of byte strings
    :rtype: dictionary
    """
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
    """
    Converts string types to bytes

    :param keyStorage: keyStorage object
    :type keyStorage: dictionary
    :return: dictionary containing byte string versions of strings
    :rtype: dictionary
    """
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

# Key Manager Class

class KeyManager():
    """
    Create a new instance of the Key management interface.

    :param password: password for encrypting (decrypting) the keyfile
    :param kwargs: empty string or path to import keyfile
    :type password: string
    :type kwargs: string
    :return: `KeyManager` object
    :rtype: instance of `KeyManager`

    """
    def __init__(self, password, kwargs=''):
        #enforce that a password must be provided
        try:
            self.password = password
        except:
            raise Exception('A password must be provided.')
        # Initialize a key manager object with a key storage object
        def initKeyStorage(keyStorage,password):
            self.pk = keyStorage['publicKeyId']
            self.isLocked = False
            self.password = password
            self.__keyStorage = keyStorage

            if self.pk: #check if public key exists
                self.__sk = recover(password, self.__keyStorage, self.constants['scrypt'])
        
        def generateKey(password):
            # this will create a new curve25519 key pair and dump to an encrypted format
            initKeyStorage(dump(password, create(self.constants), self.constants),password)

        # Imports key data object from keystore JSON file.
        def importFromFile(filePath,password):#TODO
            f = open(filePath)
            KeyStorage = json.loads(f.read())
            
            initKeyStorage(string2Bytes(KeyStorage),password)

        # initialize variables
        try:
            self.constants = kwargs['constants']
        except:
            self.constants = defaultOptions
        initKeyStorage({'publicKeyId':'','crypto': {} }, '')

        # load in keyfile if a path was given, or default to generating a new key
        if kwargs != '':
            try:
                # Will check if only a string was given and assume it is the password
                importFromFile(kwargs['keyPath'],password)
            except:
                raise Exception('Error importing keyfile')
        else:
            generateKey(password)

    
    def verify(self,publicKey,message,signature):
        """
        Check whether a private key was used to generate the signature for a message. 
        This method is static so that it may be used without generating a keyfile

        :param publicKey: A public key (if string, must be base-58 encoded)
        :param message: Message to sign (utf-8 encoded)
        :param signature: Signature to verify (if string, must be base-58 encoded)
        :type publicKey: byte string
        :type message: byte string
        :type signature: byte string
        :return: verification
        :rtype: boolean

        """
        if curve.verifySignature(base58.b58decode(publicKey), message.encode('utf-8'), signature) == 0:#retunrs -1 if not verified 0 if verified
            return True
        return 'not verfied'

  
    def getKeyStorage(self):
        """
        Getter function to retrieve key storage in the Bifrost compatible format

        """
        if self.isLocked:
            raise Exception('Key manager is currently locked. Please unlock and try again.')
        
        if not self.pk:
            raise Exception('A key must be initialized before using this key manager')
        
        return byte2String(self.__keyStorage)#WRAPO


    def lockKey(self):
        """
        Set the key manager to locked so that the private key may not be decrypted

        """
        self.isLocked = True 

    
    def unlockKey(self, password):
        """
        Unlock the key manager to be used in transactions

        :param password: encryption password for accessing the keystorage object
        :type password: string

    """
        if not self.isLocked:
            raise Exception('The key is already unlocked')
        if password != self.password:
            raise Exception('Invalid password')
        self.isLocked = False


    def sign(self, message):
        """
        Generate the signature of a message using the provided private key

        :param message: Message to sign (utf-8 encoded)
        :type message: byte string
        :return: signature
        :rtype: bytes

        """
        if self.isLocked:
            raise Exception('The key is currently locked. Please unlock and try again.')
        return curve.calculateSignature(os.urandom(64), self.__sk, message.encode('utf-8'))

    
    def exportToFile(self, _keyPath):
        """
        Export formatted JSON to keystore file.

        :param _keyPath: Path to keystore folder (default: "keystore").
        :type _keyPath: string
        :return: JSON filename 
        :rtype: string

        """
        try:
            keyPath = _keyPath
        except:
            keyPath = 'keyfiles'

        outfile = generateKeystoreFilename(self.pk.decode('utf-8'))
        JSON = json.dumps(self.getKeyStorage())
        outpath = os.path.join(keyPath,outfile)

        f = open(outpath, 'w')
        f.write(JSON)
        f.close()
        return outpath



















        









