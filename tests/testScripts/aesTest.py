import os
import sys
import pathlib
path = os.getcwd() + '/brambl/utils/'
sys.path.insert(1,path)
import Crypto



#taken from crypTest.js, make sure to update information before each new test
textJS = '1b9b93d0ae3f770a86f5a74456ffe6a0f65f2d486cc1'
keyJS = '703c99a9c2c0675f25a952b91af30f25ff303656a508d0f0d7e45afafa99cfc3'
ivJS = 'bdac53a1e8d4759318dd16bd14f5fd00'

textJS = bytes(bytearray.fromhex(textJS))
keyJS = bytes(bytearray.fromhex(keyJS))
ivJS = int(ivJS,16)

jsETest = Crypto.Decipher(textJS,keyJS,ivJS)
print(jsETest)












