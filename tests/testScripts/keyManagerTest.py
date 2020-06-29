import os
import sys
import pathlib
path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import KeyManager


key = KeyManager.KeyManager('password')
h = key.getKeyStorage()
print(h)
sig = key.sign('this is a msg')
print(sig)
