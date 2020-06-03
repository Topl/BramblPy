import os
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
import donna25519
import axolotl_curve25519 as curve
import base58

#BLAKE2b Test
obj = BLAKE2b.new(digest_bits=512)
obj.update(b'Hello World')
#print(base58.b58encode(obj.digest()))



#curve25519 Test
class keyPair():
    def __init__(self):
        self.privateKey = curve.generatePrivateKey(os.urandom(32))
        self.publicKey = curve.generatePublicKey(self.privateKey)

def signData(privKey,message):
    return curve.calculateSignature(os.urandom(64),privKey,base58.b58encode(message))
            

def verify(pubKey,message, signature):
    verified = curve.verifySignature(pubKey,base58.b58encode(message),signature)
    if verified == 0:
        return True
    else:
        return False



alice = keyPair()
bob = keyPair()
signature = signData(alice.privateKey,'Hello World')

success = verify(alice.publicKey,'Hello World',signature)
print(success)

publicWrong = verify(bob.publicKey,'Hello World',signature)
print(publicWrong)
messageWrong = verify(alice.publicKey,'Wrong Message',signature)
print(messageWrong)


#AES Test
key = b'Sixteen byte key'
cipher = AES.new(key,AES.MODE_EAX)#create AES object
nonce = cipher.nonce#define nonce for decode
ciphertext, tag = cipher.encrypt_and_digest(base58.b58encode('Hello World'))#define the ciphertext and tag used to decode


cipher2 = AES.new(key,AES.MODE_EAX,nonce=nonce)#new AES object with nonce og nonce param
plaintext = cipher2.decrypt(ciphertext)#message
try:
    cipher2.verify(tag)#verfy with tag
    #print(base58.b58decode(plaintext))
except:
    print('key incorrect or message corrupted')
