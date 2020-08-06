"""
Hash.py
====================================

"""
# Dependencies
from Crypto.Hash import BLAKE2b
import base64
import base58
from binascii import hexlify

def hashFunc():
    """
    standard FastCryptographicHash is Bifrost

    :return: Initialized hash function
    :rtype: Blake2b-256 hash

    """
    return BLAKE2b.new(digest_bits=256)

def digestAndEncode(hash,encoding):#switch statement does not exist
    """
    Create hash digest and encode

    :param hash: Initialized Blake2b-256 hash function
    :param encoding: output encoding
    :type hash: object
    :type encoding: string
    :return: Blake2b-256 hash digest
    :rtype: Blake2b-256 hash

    """
    if encoding == 'hex':
        return hexlify(hash.digest())
    elif encoding == 'base64':
        return base64.b64encode(hash.digest())
    elif encoding == 'base58':
        return base58.b58encode(hash.digest())
    else:
        return hash.digest()


def string(message,encoding):
    """
    Calculates the Blake2b-256 of a string input

    :param message: input string message to create the hash digest of
    :param encoding: output encoding
    :type message: string
    :type encoding: string
    :return: Blake2b-256 hash digest
    :rtype: Blake2b-256 hash

    """
    msg = (message).encode('utf-8')
    hash = hashFunc().update(msg)
    return (digestAndEncode(hash,encoding)).decode('utf-8')


def file(filePath,encoding):
    """
    Reads the file from disk and calculates the Blake2b-256

    :param filepath: path to the input file
    :param encoding: output encoding
    :type filepath: string
    :type encoding: string
    :return: Blake2b-256 hash digest
    :rtype: Blake2b-256 hash

    """
    BLOCK_SIZE = 65536    #64kb
    hash = hashFunc()
    with open(filePath,'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return digestAndEncode(hash,encoding).decode('utf-8')








