import os
import sys
import pathlib
path = os.getcwd() + '/brambl/utils/'
sys.path.insert(1,path)
import Crypto



#taken from crypTest.js, make sure to update information before each new test
textJS = '90b9072aca718db59feb84bd14e8f6b76d4988bb2b75'
keyJS = '703c99a9c2c0675f25a952b91af30f25ff303656a508d0f0d7e45afafa99cfc3'
ivJS = 'f59cf92439588a55d2b56f4681fba697'

textJS = bytes(bytearray.fromhex(textJS))
keyJS = bytes(bytearray.fromhex(keyJS))
ivJS = int(ivJS,16)

jsETest = Crypo.Decipher(textJS,keyJS,ivJS)
print(jsETest)








