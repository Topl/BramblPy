from Crypto.Hash import BLAKE2b
import curve25519
obj = BLAKE2b.new(digest_bits=512)
obj.update(b'Hello World')
print(obj.digest())

