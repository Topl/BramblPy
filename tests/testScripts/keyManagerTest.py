import os
import sys
import pathlib
path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import KeyManager



key = KeyManager.KeyManager('a complex password')
h = key.getKeyStorage()
print(h)

sig = key.sign('this is a msg')
print(KeyManager.base58.b58encode(sig))

ver = key.verify(h['publicKeyId'],'this is a msg',sig)
print(ver)


