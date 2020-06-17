import os
import sys
import pathlib
path = os.getcwd() + '/brambl/utils/'
sys.path.insert(1,path)
import Crypto



#taken from crypTest.js, make sure to update information before each new test
textJS = '25be3f956c58298b4a10d063142a7de70689e54b6d2d'
keyJS = '854afd3e7dcc1433dfc300717009c5e6e2d09ba523c7a39d694554f26b938aa8'
ivJS = 'a64ae7e7b1348a2c9a239a7deca21ea8'

textJS = bytes(bytearray.fromhex(textJS))
keyJS = bytes(bytearray.fromhex(keyJS))
ivJS = int(ivJS,16)

jsETest = aesDecipher(textJS,keyJS,ivJS)
print(jsETest)








