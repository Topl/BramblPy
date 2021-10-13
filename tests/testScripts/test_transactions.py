import unittest

from brambl.modules.Requests import validate_txId

class BasicTransactionTests(unittest.TestCase):
    def test_txid_validator_error(self):
        self.assertRaises(ValueError, validate_txId, "abc")
        self.assertRaises(TypeError, validate_txId, None)
        self.assertRaises(TypeError, validate_txId, [])
        
