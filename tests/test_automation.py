import pytest
import os
import sys
import json

path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import KeyManager

path = os.getcwd() + '/brambl/utils/' #update path once directory rename is sorted
sys.path.insert(1,path)
import Hash
import CrypTools

def test_str2pybuf():
    assert KeyManager.str2pybuf('test') == b'\x99\xc7\xb3'

def test_encrypt():
    assert KeyManager.encrypt('test',b'1111111111111111',bytes(b'iv'),'aes-256-ctr') == b'\x03~r\xa5'

def test_decrypt():
    assert KeyManager.decrypt(b'\x03~r\xa5',b'1111111111111111',bytes(b'iv'),'aes-256-ctr') == b'test'

def test_getMAC():
    assert KeyManager.getMAC(b'key',b'text') == b'\x95\x99\xd5\xe4\xe41!\x19l\xad\xfe\xae\xa3&\xe4oX\xd9\xdbt)\x9d\xec\xfdd\xbd;p\x03P\xcc\xd9'

def test_digestAndEncode():
    blakeHash = Hash.hashFunc()
    assert Hash.digestAndEncode(blakeHash,'hex') == b'0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8'
    assert Hash.digestAndEncode(blakeHash,'base64') == b'DldRwCblQ7Loqy6wYJnaodHl30d3j3eH+qtFzfEv46g='
    assert Hash.digestAndEncode(blakeHash,'base58') == b'xyw95Bsby3s4mt6f4FmFDnFVpQBAeJxBFNGzu2cX4dM'

def test_string():
    assert Hash.string('message','hex') == '2e7836cc18ab1db2a2e239ebf4043772b3359520198b5fd55443b01a1023a5b0'
    assert Hash.string('message','base64') == 'Lng2zBirHbKi4jnr9AQ3crM1lSAZi1/VVEOwGhAjpbA='
    assert Hash.string('message','base58') == '48Q5BFky1FezpJW7weo6yfhzPfnjTahJ4wT16NdvQC5M'
