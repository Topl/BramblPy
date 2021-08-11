import unittest
import json
import base58

from brambl.modules import KeyManager
from brambl.utils import Hash
from brambl.utils import CrypTools
from brambl.Brambl import Brambl
import mock


def simple_urandom(length):
    return ('f' * length).encode('utf-8')


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


class TestAddSigMethods(unittest.IsolatedAsyncioTestCase):
    @mock.patch('brambl.modules.KeyManager.urandom', side_effect=simple_urandom)
    async def test_addSigToTx(self, urandom_function):
        key_manager_1 = KeyManager.KeyManager(password='test', kwargs={'keyPath': '../keyFile_1.json'})
        prototypeTx = '''{
           "jsonrpc":"2.0",
           "id":"e7789f19-c540-4f04-b9ba-5e424d7172f6",
           "result":{
              "rawTx":{
                 "txType":"AssetTransfer",
                 "timestamp":1626104397373,
                 "signatures":{
                    
                 },
                 "newBoxes":[
                    {
                       "nonce":"2149736382704735321",
                       "id":"EgyDSm5Yz8GfkvvPnaJfXnDvBiTK4nSmzFANq4STWt8H",
                       "evidence":"YYTe1t1hHa429em6yDzCFsRakUJjhSynFPpKjFJ2uQMu",
                       "type":"PolyBox",
                       "value":{
                          "type":"Simple",
                          "quantity":"4800"
                       }
                    },
                    {
                       "nonce":"1312804140406069949",
                       "id":"AzDS9YnqiWYDMhbpDjGPA6ZHi3uibotrYPxW9k1ELiHL",
                       "evidence":"YYTe1t1hHa429em6yDzCFsRakUJjhSynFPpKjFJ2uQMu",
                       "type":"AssetBox",
                       "value":{
                          "quantity":"1",
                          "assetCode":"5YJR24BDmDJuZPeDRCn7TPy96qtxDUDLHs22RVWUXDm2jcAJGzK9DysDM1",
                          "metadata":"e7789f19-c540-4f04-b9ba-5e424d7172f6",
                          "type":"Asset",
                          "securityRoot":"7dqWYvKyH5MKJDSvVDDTB5L5Vv2LQyzVfHS98GSjvdck"
                       }
                    }
                 ],
                 "data":"{}",
                 "to":[
                    [
                       "3NLeYvHanEmMZLW7bvBsKAV5bvZaGqmiS4gz9FPitEMTdvF51dod",
                       {
                          "type":"Simple",
                          "quantity":"4800"
                       }
                    ],
                    [
                       "3NLeYvHanEmMZLW7bvBsKAV5bvZaGqmiS4gz9FPitEMTdvF51dod",
                       {
                          "quantity":"1",
                          "assetCode":"5YJR24BDmDJuZPeDRCn7TPy96qtxDUDLHs22RVWUXDm2jcAJGzK9DysDM1",
                          "metadata":"e7789f19-c540-4f04-b9ba-5e424d7172f6",
                          "type":"Asset",
                          "securityRoot":"7dqWYvKyH5MKJDSvVDDTB5L5Vv2LQyzVfHS98GSjvdck"
                       }
                    ]
                 ],
                 "propositionType":"PublicKeyCurve25519",
                 "from":[
                    [
                       "3NLeYvHanEmMZLW7bvBsKAV5bvZaGqmiS4gz9FPitEMTdvF51dod",
                       "-3694647291444886373"
                    ]
                 ],
                 "minting":true,
                 "txId":"pcrvnEse27woodXV7FZ83qm9o1mgN6EtVdXAVrAKnyjs",
                 "boxesToRemove":[
                    "AbmpiZnGmtWb6KyFNhAqMNf4TAtdo98AMbhARems7zSV"
                 ],
                 "fee":"100"
              },
              "messageToSign":"4DoyoG2rAaqjk3z8PLwKm7vJmNkyWGhB3GW3dybUV8QhAhSeXqM9fXFcGBfP3nvE3BZsSb2FVFJ8PuGWQXaQJ8K99t6ZfKKe6Wd9Ux4LzhgxXF7GRUHPz6qkUURxRR4dudUniixmVSApRv66pynV4rmVCyNRqnbyZ86VHnZCoFuxsMavHf2qicvh85hRkazcPcpvjswVXkfuVfACbNGPvcMRCAcF8TirFkSFTdBfCCwMrgZQcjpQE8EHvfS7y6KofGSwsZzemiRHeY8aKr9t8bjZTWWcH6Vy5oPRENeu1hQ8KbxKHPyW48oHhAHWRzbjVLSneFi4x82ZBisDNzE6K8Dj5v2CPJrZ639nic45rNYxfqBEe9RBfda9TBLE8JZwRxSijnR5esrAdEjcWTzNN2Dq9oePLTijhHoEFcnnesRirW9pdpUiM7yx3hvBiEbXxe8Q9u44grekiBXZBRPAv9Vqq3DF3aG4wb81eCsvZ6cnjpYQBBZBwbC8FsfZUySvrAMGdmsYp1FE5ovVZQhWkTeAeQ56UhtRgsfLBo5oHPuNZtbs3EmQt"
           }
        }'''

        tx = await Brambl.addSigToTx(self=self, prototypeTx=prototypeTx, userKeys=key_manager_1)
        signatures = json.loads(tx)['signatures']
        self.assertEqual(signatures, {'VerBy9rzEeYCnFihJtefevmwHmx9iUnRrSbeVBWCmiFf':'8y4GPKUx7rYZnLEL6K58wq4k9qokP6axfqQWLXtAk8WBf4VJqwWjcXuMeTKygRfjNSg5FWaGAwhFGsoQ7A9hVYJu'})

        key_manager_2 = KeyManager.KeyManager(password="test", kwargs={'keyPath': '../keyFile_2.json'})
        key_manager_list = [key_manager_1, key_manager_2]

        tx_list = await Brambl.addSigToTx(self=self, prototypeTx=prototypeTx, userKeys=key_manager_list)
        signatures_list = json.loads(tx_list)['signatures']
        self.assertEqual(signatures_list, {'VerBy9rzEeYCnFihJtefevmwHmx9iUnRrSbeVBWCmiFf': '8y4GPKUx7rYZnLEL6K58wq4k9qokP6axfqQWLXtAk8WBf4VJqwWjcXuMeTKygRfjNSg5FWaGAwhFGsoQ7A9hVYJu', 'PEkXe94z6TafpNLBB7vt2zvwxcbvUUGZvVpnGyDEVPPa': '7ER7z4Kiup5aL2k8ne6wmTLuh1sRMTfrSWW8kK2kDMaTZ1nsx6WAJhpAYyhVqAsF3zvTRSTHSqao2JU1UjLoZyDp'})


    #concludes the unit tests
if __name__ == '__main__':
    unittest.main()


