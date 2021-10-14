import unittest

from base58 import b58decode

from brambl.simple_models import AssetCode


class TestComparisons(unittest.TestCase):
    def test_cmpp_same_assetCode(self):
        name = ("name".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name,
            "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        )
        asset2 = AssetCode(
            name,
            "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        )
        self.assertEqual(asset1, asset2)

    def test_cmp_different_name_assetcode(self):
        name1 = ("name1".encode("latin-1")).decode("latin-1")
        name2 = ("name2".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name1,
            "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        )
        asset2 = AssetCode(
            name2,
            "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        )
        self.assertNotEqual(asset1, asset2)

    def test_cmp_different_issuer_address(self):
        name = ("name".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name,
            "3NLHCWwuZrn8wMFUX1QR76M8iWXYht4n52eNGMTM3cyxJzQayNrX"
        )
        asset2 = AssetCode(
            name,
            "AU9avKWiVVPKyU9LoMqDpduS4knoLDMdPEK54qKDNBpdnAMwQZcS"
        )
        self.assertNotEqual(asset1, asset2)

    def test_cmp_assetcode_to_string(self):
        name = ("name".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name,
            "AU9avKWiVVPKyU9LoMqDpduS4knoLDMdPEK54qKDNBpdnAMwQZcS"
        )
        asset2 = "6Lm9dRk8kZqP1ZgKJutmNAmkwZsqKu14JLrtWWcZapuFpZ92vXpRBegg2b"
        self.assertEqual(asset1, asset2)

    def test_cmp_assetcode_to_bytes(self):
        name = ("name".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name,
            "AU9avKWiVVPKyU9LoMqDpduS4knoLDMdPEK54qKDNBpdnAMwQZcS"
        )
        asset2 = b58decode("6Lm9dRk8kZqP1ZgKJutmNAmkwZsqKu14JLrtWWcZapuFpZ92vXpRBegg2b")
        self.assertEqual(asset1, asset2)

    def test_cmp_assetcode_to_none(self):
        name = ("name".encode("latin-1")).decode("latin-1")
        asset1 = AssetCode(
            name,
            "AU9avKWiVVPKyU9LoMqDpduS4knoLDMdPEK54qKDNBpdnAMwQZcS"
        )
        self.assertNotEqual(asset1, None)