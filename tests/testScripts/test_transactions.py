from decimal import Decimal
import unittest
from brambl.address import Address
from brambl.consts import PropositionType
from brambl.metadata import Metadata
from brambl.transaction import Input

from brambl.utils.validation import validate_txId

class BasicTransactionTests(unittest.TestCase):
    def test_txid_validator_error(self):
        self.assertRaises(ValueError, validate_txId, "abc")
        self.assertRaises(TypeError, validate_txId, None)
        self.assertRaises(TypeError, validate_txId, [])
    
    def test_input(self):
        inp = Input(
            fee = 100,
            propositionType = PropositionType.PUBLICKEYED25519,
            data = Metadata(),
             txType = "PolyTransaction",
            sender =  [Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX")],
            changeAddress =  Address("3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"),
            recipients = [Address("3NKunrdkLG6nEZ5EKqvxP5u4VjML3GBXk2UQgA9ad5Rsdzh412Dk")],
            consolidationAddress = Address("3NKunrdkLG6nEZ5EKqvxP5u4VjML3GBXk2UQgA9ad5Rsdzh412Dk"),
            assetCode =  "5YJoZH7jk5o1LipWMkH3Kyy9cu5CRCM2U9sbA5nMSi32raW42cWVMaPwqy"
        )
        self.assertEqual(len(inp.sender), 1)
        self.assertEqual(len(inp.recipients), 1)
        self.assertEqual(inp.fee,  100)
        self.assertIsInstance(inp.propositionType, PropositionType)
        self.assertEqual(inp.txType, "PolyTransaction")
    
    def test_inherited(self):
        class CustomTxInput(Input):
            fee = Decimal("0.168801")
        
        tx = CustomTxInput

        self.assertEqual(tx.fee, Decimal("0.168801"))