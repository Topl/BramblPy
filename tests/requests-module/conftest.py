import os.path
import warnings
from distutils import dir_util

import pytest
from _pytest.fixtures import fixture

from brambl.Brambl import Brambl
from brambl.client.rpc import HTTPClient
from brambl.credentials.credential_manager import Ed25519CredentialManager
from brambl.keyfile.keyfile import load_keyfile


@pytest.fixture(autouse=True)
def print_warnings():
    warnings.simplefilter('always')


def brambl():
    client = HTTPClient()
    return Brambl(client)


@pytest.fixture(name="brambl")
def brambl_fixture():
    return brambl()


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name as the test
    and if available moving all contents to a temporary directory so that all the tests
    can use them freely
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    # Important, this code will not work in Python 2 as the copy_tree method
    # takes a bytes object as the second object instead of the string object
    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


@fixture
def default_address(datadir):
    expected_keyfile = datadir.join(
        'AUAr1QSvxLAoHHLrGKMMvyYpaReH6EmwQLAqT1zHMkxSQkNaRiz8.json')
    with open(expected_keyfile) as keyfile_file:
        loaded_keyfile_json = load_keyfile(keyfile_file)
    password = "test"
    derived_private_key = Ed25519CredentialManager.decrypt(loaded_keyfile_json,
                                                           password)
    return Ed25519CredentialManager.from_key(derived_private_key, 0x40)


@pytest.fixture
def extra_addresses():
    num_addresses_to_create = 10
    list_topl_credentials = []

    for i in range(num_addresses_to_create):
        list_topl_credentials.append(Ed25519CredentialManager.create(0x40))

    return list_topl_credentials
