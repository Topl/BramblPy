import warnings

import pytest

from brambl.client.rpc import HTTPClient
from brambl.credentials.credential_manager import Ed25519CredentialManager


@pytest.fixture(autouse=True)
def print_warnings():
    warnings.simplefilter('always')


@pytest.fixture()
def brambl():
    client = HTTPClient()
    return brambl(client)


@pytest.fixture
def extra_addresses(brambl, address_password):
    num_addresses_to_create = 10
    list_topl_credentials = []

    for i in range(num_addresses_to_create):
        list_topl_credentials.append(Ed25519CredentialManager.create(0x40))

    return list_topl_credentials
