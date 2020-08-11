from brambl.modules import KeyManager
from binascii import hexlify
import base58

path = '/home/arjunmehta/'
gjal = KeyManager.KeyManager('password')

h = gjal.getKeyStorage()
print(h)

exporte = gjal.exportToFile(path)
print(exporte)