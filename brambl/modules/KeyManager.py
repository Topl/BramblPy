from Crypto.Hash import BLAKE2b
from Crypto.Hash import keccak
import axolotl_curve25519 as curve
import base58

defaultOptions = {
    'cipher': 'aes-256-ctr',
    'ivBytes': 16,
    'keyBytes': 32,
    'scrypt': {
        'dkLen': 32,
        'n': 2**18,
        'r': 8,
        'p': 1
    }
}


def isFunction(f):
    return callable(f)




