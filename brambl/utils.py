from Crypto.Hash import BLAKE2b
import donna25519

obj = BLAKE2b.new(digest_bits=512)
obj.update(b'Hello World')


def keyPair():
    return donna25519.PrivateKey()#default os.urandom

def signData(sender, receiver):
    return receiver.do_exchange(sender.get_public())#intended shared key
            

def verify(intededKey,sender,decrypter):
    if  intededKey == decrypter.do_exchange(sender.get_public()):
        return True
    else:
        return False


alice = keyPair()#intialize 
bob = keyPair()
carl = keyPair()
shared = signData(alice,bob)#create a shared key 
print(verify(shared,alice,bob))#intended message for bob
print(verify(shared,alice,carl))#message not intended for carl



    




