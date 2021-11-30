import pytest


def test_bifrost_protocol_version(brambl):
    assert brambl.requests.node_info == {
        'network': 'PrivateTestnet', 'nodeAddress': 'N/A', 'version': '1.9.1'}