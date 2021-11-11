from brambl.types import PolyRawTxParams, Poly


def test_uses_default_address_when_set(brambl, default_address,
                                       extra_addresses):
    brambl.requests.default_address = default_address.address
    assert brambl.requests.default_address == default_address.address

    transaction: PolyRawTxParams = {
        "propositionType": "PublicKeyEd25519",
        "data": "Unit Test 1",
        "recipients": [[str(extra_addresses[1].address), Poly("0")]],
        "fee": Poly("100"),
        "boxSelectionAlgorithm": "All"
    }

    txn = brambl.requests.send_raw_poly_transaction(transaction)
    assert txn['rawTx']['from'][0][0] == default_address.address


def test_uses_given_from_address_when_provided(brambl, default_address,
                                               extra_addresses):
    brambl.requests.default_address = extra_addresses[2].address
    assert brambl.requests.default_address == extra_addresses[2].address

    transaction: PolyRawTxParams = {
        "propositionType": "PublicKeyEd25519",
        "data": "Unit Test 1",
        "recipients": [[str(extra_addresses[1].address), "0"]],
        "fee": "100",
        "boxSelectionAlgorithm": "All",
        "sender": [str(default_address.address)]
    }

    txn = brambl.requests.send_raw_poly_transaction(transaction)
    assert txn['rawTx']['from'][0][0] == str(default_address.address)


