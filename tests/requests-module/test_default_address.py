import pytest


def test_uses_default_address_when_set(brambl, extra_addresses,
                                       wait_for_transaction):
    brambl.requests.default_address = extra_addresses[2]
    assert brambl.requests.default_address == extra_addresses[2]


def test_uses_defaultAccount_when_set_with_warning(web3, extra_addresses,
                                                   wait_for_transaction):
    with pytest.warns(DeprecationWarning):
        web3.eth.defaultAccount = extra_addresses[2]

    with pytest.warns(DeprecationWarning):
        assert web3.eth.defaultAccount == extra_addresses[2]

    txn_hash = web3.eth.send_transaction({
        "to": extra_addresses[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.eth.get_transaction(txn_hash)
    assert txn['from'] == extra_addresses[2]


def test_uses_given_from_address_when_provided(web3, extra_addresses,
                                               wait_for_transaction):
    web3.eth.default_address = extra_addresses[2]
    txn_hash = web3.eth.send_transaction({
        "from": extra_addresses[5],
        "to": extra_addresses[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.eth.get_transaction(txn_hash)
    assert txn['from'] == extra_addresses[5]


def test_uses_given_from_address_when_provided_with_warning(web3, extra_addresses,
                                                            wait_for_transaction):
    with pytest.warns(DeprecationWarning):
        web3.eth.defaultAccount = extra_addresses[2]

    with pytest.warns(DeprecationWarning):
        assert web3.eth.defaultAccount == extra_addresses[2]

    txn_hash = web3.eth.send_transaction({
        "from": extra_addresses[5],
        "to": extra_addresses[1],
        "value": 1234,
    })

    wait_for_transaction(web3, txn_hash)

    txn = web3.eth.get_transaction(txn_hash)
    assert txn['from'] == extra_addresses[5]
