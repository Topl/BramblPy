import os
import sys
import pathlib
path = os.getcwd() + '/brambl/modules/'
sys.path.insert(1,path)
import KeyManager
from binascii import hexlify
import base58

path = '/home/arjunmehta/'
gjal = KeyManager.KeyManager('password')

h = gjal.getKeyStorage()
print(h)

exporte = gjal.exportToFile(path)
print(exporte)