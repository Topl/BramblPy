import os

import pytest
from brambl.ed25519 import keys

from brambl.ed25519.KeyManager import KeyManager

PRIVATE_KEY_AS_BYTES = b'unicorns' * 4
PRIVATE_KEY_AS_HEXSTR = '0x756e69636f726e73756e69636f726e73756e69636f726e73756e69636f726e73'
PRIVATE_KEY_AS_INT = 0x756e69636f726e73756e69636f726e73756e69636f726e73756e69636f726e73
PRIVATE_KEY_AS_OBJ = keys.PrivateKey(PRIVATE_KEY_AS_BYTES)

PRIVATE_KEY_AS_BYTES_ALT = b'rainbows' * 4
PRIVATE_KEY_AS_HEXSTR_ALT = '0x7261696e626f77737261696e626f77737261696e626f77737261696e626f7773'
PRIVATE_KEY_AS_INT_ALT = 0x7261696e626f77737261696e626f77737261696e626f77737261696e626f7773
PRIVATE_KEY_AS_OBJ_ALT = keys.PrivateKey(PRIVATE_KEY_AS_BYTES_ALT)


@pytest.fixture(
    params=[PRIVATE_KEY_AS_INT, PRIVATE_KEY_AS_HEXSTR, PRIVATE_KEY_AS_BYTES, PRIVATE_KEY_AS_OBJ])  # noqa: 501
def PRIVATE_KEY(request):
    return request.param


@pytest.fixture(params=['instance', 'class'])
def key_man(request):
    if request.param == 'instance':
        return KeyManager()
    elif request.param == 'class':
        return KeyManager
    else:
        raise Exception("key manager invocation {request.param} is not supported")


@pytest.fixture
def keyed_manager():
    return KeyManager.from_key(PRIVATE_KEY_AS_BYTES)


def test_brambl_key_manager_default_kdf(acct, monkeypatch):
    assert os.getenv('BRAMBL_PRIMARY_KDF') is None
    assert acct._default_kdf == 'scrypt'

    monkeypatch.setenv('BRAMBL_PRIMARY_KDF', 'pbkdf2')
    assert os.getenv('BRAMBL_PRIMARY_KDF') == 'pbkdf2'

    import importlib
    from brambl.ed25519.KeyManager import KeyManager
    importlib.reload(KeyManager)
    assert KeyManager._default_kdf == 'pbkdf2'

def test_brambl_key_manager_create_variation(key_man):
    account1 = key_man.create()
    account2 = key_man.create()
    assert account1 != account2

def test_brambl_key_manager_equality(key_man, PRIVATE_KEY):
    acct1 = key_man.from_key(PRIVATE_KEY)
    acct2 = key_man.from_key(PRIVATE_KEY)
    assert acct1 == acct2

def test_brambl_key_manager_from_key_reproducible(key_man, PRIVATE_KEY):
    account1 = key_man.from_key(PRIVATE_KEY)
    account2 = key_man.from_key(PRIVATE_KEY)
    assert bytes(account1) == PRIVATE_KEY_AS_BYTES
    assert bytes(account1) == bytes(account2)
    assert isinstance(str(account1), str)

def test_brambl_key_manager_from_key_diverge(key_man, PRIVATE_KEY, PRIVATE_KEY_ALT):
    key_man1 = key_man.from_key(PRIVATE_KEY)
    key_man2 = key_man.from_key(PRIVATE_KEY_ALT)
    assert bytes(key_man1) == PRIVATE_KEY_AS_BYTES_ALT
    assert bytes(key_man1) != bytes(key_man2)

def test_brambl_key_manager_from_key_properties(key_man, PRIVATE_KEY):
    credential = key_man.from_key(PRIVATE_KEY)
    assert callable(credential.signHash)
    assert is_checksum_address(account.address)
    assert account.address == ACCT_ADDRESS
    assert account.key == PRIVATE_KEY_AS_OBJ


