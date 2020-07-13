import os
import sys
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import axolotl_curve25519 as curve
import base58
import pyaes
from binascii import hexlify

#curve25519 Test
def sigverify(pubKey,message, signature):
    verified = curve.verifySignature(pubKey,base58.b58encode(message),signature)
    if verified == 0:#return 0 if verified
        return True
    else:
        return False

#AES Test
def aesCipher(algorithm,plaintext, key, iv):
    if algorithm != 'aes-256-ctr':
        raise Exception('Algorithm not supported')
    aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

    
def aesDecipher(ciphertext,key,iv):
    aes = pyaes.AESModeOfOperationCTR(key,pyaes.Counter(iv))
    return aes.decrypt(ciphertext).decode('utf-8')
