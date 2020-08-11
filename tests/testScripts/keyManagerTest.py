from brambl.modules import KeyManager



key = KeyManager.KeyManager('a complex password')
h = key.getKeyStorage()
print(h)

sig = key.sign('this is a msg')
print(KeyManager.base58.b58encode(sig))

ver = key.verify(h['publicKeyId'],'this is a msg',sig)
print(ver)


