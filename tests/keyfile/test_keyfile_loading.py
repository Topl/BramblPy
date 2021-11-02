import codecs

from base58 import b58decode

from brambl.keyfile.keyfile import decode_keyfile_json


def test_decoding_keyfile(keyfile_data):
    password = codecs.encode(keyfile_data['password'], 'latin-1')
    keyfile_json = keyfile_data['json']
    private_key = keyfile_data['priv']

    derived_private_key = decode_keyfile_json(keyfile_json, password)
    assert b58decode(private_key) == derived_private_key