from Crypto.Hash import BLAKE2b
import base64
import base58
from binascii import hexlify

def hashFunc():
    return BLAKE2b.new(digest_bits=256)

def digestAndEncode(hash,encoding=''):#switch statement does not exist
    if encoding == 'hex':
        return hexlify(hash.digest())
    elif encoding == 'base64':
        return base64.b64encode(hash.digest())
    elif encoding == 'base58':
        return base58.b58encode(hash.digest())
    else:
        return hash.digest()

def string(message,encoding):
    msg = (message).encode('utf-8')
    hash = hashFunc().update(msg)
    return (digestAndEncode(hash,encoding)).decode('utf-8')

def file(filePath,encoding):
    BLOCK_SIZE = 65536    #64kb
    hash = hashFunc()
    with open(filePath,'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return digestAndEncode(hash,encoding).decode('utf-8')








