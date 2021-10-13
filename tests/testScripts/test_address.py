import os
import unittest

#print('cwd is %s' %(os.getcwd()))

from brambl.address import Address, PublicKeyCurve25519Address, PublicKeyEd25519Address, address
from tests.testScripts.example_addresses import MAINNET_ADDRESSES_OK, PRIVATE_ADDRESSES_OK, VALHALLA_ADDRESSES_OK


class BaseTestAddressOk(object):
    address_list = None
    AddressClass = None
    networkPrefix = None
    def test_address(self):
        for addr in self.address_list:
            addrobj = address(addr, self.networkPrefix)
            self.assertIsInstance(addrobj, self.AddressClass)
    
class TestValhallaAddressOK(BaseTestAddressOk, unittest.TestCase):
    address_list = VALHALLA_ADDRESSES_OK
    AddressClass = PublicKeyEd25519Address
    networkPrefix = 'valhalla'


class TestPrivateAddressOk(BaseTestAddressOk, unittest.TestCase):
    address_list = PRIVATE_ADDRESSES_OK
    AddressClass = PublicKeyEd25519Address
    networkPrefix = "private"

class MainnetAddressOK(BaseTestAddressOk, unittest.TestCase):
    address_list = MAINNET_ADDRESSES_OK
    AddressClass = PublicKeyEd25519Address
    networkPrefix = "toplnet"

class TestComparisons(unittest.TestCase):
    def test_cmp_Same_address(self):
        addr1 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")
        addr2 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")
        self.assertEqual(addr1, addr2)
    
    def test_cmp_different_address(self):
        addr1 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")
        addr2 = Address("3NKunrdkLG6nEZ5EKqvxP5u4VjML3GBXk2UQgA9ad5Rsdzh412Dk")
        self.assertNotEqual(addr1, addr2)
    
    def test_cmp_address_to_string(self):
        addr1 = "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        addr2 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")
        self.assertEqual(addr1, addr2)

    def test_cmp_address_to_bytes(self):
        addr2 = "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX".encode()
        addr1 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")

        self.assertEqual(addr1, addr2)

    def test_cmp_address_to_none(self):
        addr1 = Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")

        self.assertNotEqual(addr1, None)