import hashlib
#from Crypto.Hash import blake2b


m = hashlib.blake2b()
m.update(b'Hello World')
print(m.digest())
print(m.hexdigest())

'''
#for crypto.hash, does not work#
obj = blake2b.new(digest_bits=512)
obj.update(b'Hello World')
print(obj.hexidigest())
'''