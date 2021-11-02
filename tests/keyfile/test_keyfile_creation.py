from __future__ import unicode_literals

from base58 import b58decode

from brambl.keyfile.keyfile import create_keyfile_json, decode_keyfile_json

PRIVATE_KEY = b58decode('4vJ9JU1bJJE96FWSJKvHsmmFADCg4gpZQff4P3bkLKi')
PASSWORD = 'test'


def test_scrypt_keyfile_creation():
    keyfile_json = create_keyfile_json(
        PRIVATE_KEY,
        password=PASSWORD,
        kdf='scrypt',
        iterations=8192,
        network_prefix=0x40,
        proposition_type = "PublicKeyEd25519"
    )
    derived_private_key = decode_keyfile_json(keyfile_json, PASSWORD)
    assert derived_private_key == PRIVATE_KEY


def test_scrypt_keyfile_address():
    keyfile_json = create_keyfile_json(
        PRIVATE_KEY,
        password=PASSWORD,
        kdf='scrypt',
        iterations=2,
        network_prefix = 0x40,
        proposition_type = "PublicKeyEd25519"
    )
    assert keyfile_json['address'] == 'AUEgyX7QfKW2x2RVthNheLPAToQwxYjYiACgLjRY5XKPW5pMRG72'
