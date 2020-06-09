import os
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import axolotl_curve25519 as curve
from Crypto.Random import get_random_bytes
import base64
import base58
from binascii import hexlify
import json

#BLAKE2b Test
"""
obj = BLAKE2b.new(digest_bits=512)
obj.update(b'Hello World')
print(base58.b58encode(obj.digest()))
"""


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


"""
alice = keyPair()
bob = keyPair()
signature = signData(alice.privateKey,'Hello World')

success = verify(alice.publicKey,'Hello World',signature)#successful test
print(success)
#wrong case tests
publicWrong = verify(bob.publicKey,'Hello World',signature)
print(publicWrong)
messageWrong = verify(alice.publicKey,'Wrong Message',signature)
print(messageWrong)
"""

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

"""
password = 'My password is password.'
salt = get_random_bytes(32)
key = scrypt(password,salt,32,N=2**14, r=8, p=1)
result = gencipher('aes-256-ctr',key,'Hello World')
message = genDecipher(key,result)
print(message)
"""


def hashFunc():
    return BLAKE2b.new(digest_bits=256)

def digestAndEncode(hash,encoding=''):#switch statement does not exist
    if encoding == 'hex':
        return hexlify(hash.digest())
    elif encoding == 'base64':
        return base64.b64encode(hash.digest())
    elif encoding == 'base58':
        return base58.b58encode(hash.digest())
    else:
        return hash.digest()


def any(message,encoding):
    msg = (json.dumps(message)).encode('utf-8')
    hash = hashFunc().update(msg)
    return digestAndEncode(hash,encoding).decode('utf-8')


def string(message,encoding):
    msg = (message).encode('utf-8')
    hash = hashFunc().update(msg)
    return (digestAndEncode(hash,encoding)).decode('utf-8')

def file(filePath,encoding):
    BLOCK_SIZE = 65536    #64kb
    hash = hashFunc()
    with open(filePath,'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return digestAndEncode(hash,encoding).decode('utf-8')


print(any({'dic':'tionary'},'base64'))
print(string('this is a string','base58'))
print(file('/home/arjunmehta/Brambl-Py/tests/fileTest.txt','hex'))




