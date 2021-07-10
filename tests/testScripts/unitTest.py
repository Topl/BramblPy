import unittest
import json
import base58

from brambl.modules import KeyManager
from brambl.utils import Hash
from brambl.utils import CrypTools


class TestBasicMethods(unittest.TestCase):

    def test_str2pybuf(self):
        self.assertEqual(KeyManager.str2pybuf('test'),b'\x99\xc7\xb3')

    def test_encrypt(self):
        self.assertEqual(KeyManager.encrypt('test',b'1111111111111111',bytes(b'iv'),'aes-256-ctr'),b'\x03~r\xa5')

    def test_decrypt(self):
        self.assertEqual(KeyManager.decrypt(b'\x03~r\xa5',b'1111111111111111',bytes(b'iv'),'aes-256-ctr'),b'test')

    def test_getMAC(self):
        self.assertEqual(KeyManager.getMAC(b'\xcc\xe43\xb6\xe3Q\x07\xf5\xbb\xf3\x0e1k\x01\xf5"\x11IO2iX4\xda:\xf3!\x1e0\xd3-\r',
                                           base58.b58decode("46bFSSr1npYKmZvRwoYYoQ1zN4jyrKrp5SxHe1gZBKsbNnhyUBbjEAvZwm6ntaDdkk6itTPpDusHq13DUy71Lwe5")),
                         b'V\x81\xe1pJk\x11\xca\xb8\xc8\x9f\xe0\xd4\xd07\x04#\xdd\x9eL\xbd\xe5$\xc7\xc2%\xa3)M\x83/\xe0')

    def test_digestAndEncode(self):
        blakeHash = Hash.hashFunc()
        self.assertEqual(Hash.digestAndEncode(blakeHash,'hex'),b'0e5751c026e543b2e8ab2eb06099daa1d1e5df47778f7787faab45cdf12fe3a8')
        self.assertEqual(Hash.digestAndEncode(blakeHash,'base64'),b'DldRwCblQ7Loqy6wYJnaodHl30d3j3eH+qtFzfEv46g=')
        self.assertEqual(Hash.digestAndEncode(blakeHash,'base58'),b'xyw95Bsby3s4mt6f4FmFDnFVpQBAeJxBFNGzu2cX4dM')

    def test_string(self):
        self.assertEqual(Hash.string('message','hex'),'2e7836cc18ab1db2a2e239ebf4043772b3359520198b5fd55443b01a1023a5b0')
        self.assertEqual(Hash.string('message','base64'),'Lng2zBirHbKi4jnr9AQ3crM1lSAZi1/VVEOwGhAjpbA=')
        self.assertEqual(Hash.string('message','base58'),'48Q5BFky1FezpJW7weo6yfhzPfnjTahJ4wT16NdvQC5M')

    def test_aesCipher(self):
        pass
    
    def test_aesDecipher(self):
        pass

    #concludes the unit tests
if __name__ == '__main__':
    unittest.main()


