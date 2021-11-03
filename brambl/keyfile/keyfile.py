
import hmac
import json
import uuid

from Crypto import Random
from Crypto.Hash import BLAKE2b
from Crypto.Protocol.KDF import scrypt
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from base58 import b58encode, b58decode

from brambl.ed25519.utils.address import NetworkId
from brambl.ed25519 import keys
from brambl.utils.encoding import big_endian_to_int
from brambl.utils.functional import to_dict
from brambl.utils.types import is_string, is_dict

DKLEN = 32
SCRYPT_R = 1
SCRYPT_P = 8


def get_mac(derived_key, ciphertext):
    """
    Calculate message authentication code from secret (derived) key and
    encrypted text. The MAC is the blake2b-256 hash of the byte array
    formed by concatenating the second 16 bytes of the derived key with
    the ciphertext key's contents.

    :param derived_key: Secret key derived from password
    :param ciphertext: ciphertext Text encrypted with secret key.
    :type ciphertext: bytes
    :return: Base58-encoded MAC
    :rtype: bytes

    """
    blake = BLAKE2b.new(digest_bits=256)
    return blake.update(derived_key[16:32] + ciphertext).digest()


def load_keyfile(path_or_file_obj):
    if is_string(path_or_file_obj):
        with open(path_or_file_obj) as keyfile_file:
            return json.load(keyfile_file)
    else:
        return json.load(path_or_file_obj)


def create_keyfile_json(private_key, password, network_prefix: NetworkId, proposition_type: str, version=1,
                        kdf="scrypt", salt_size=16, iterations=None, dk_len=DKLEN, scrypt_r=SCRYPT_R,
                        scrypt_p=SCRYPT_P):
    '''
    BramblPy has been written to be compatible with all the possible encrypted keystores that can be produced by a Brambl Library
    '''
    if version == 0 or version == 1 or version == 2:
        return _create_keyfile_json(
            private_key,
            password,
            kdf,
            network_prefix,
            proposition_type,
            salt_size,
            kdf_params={
                'dkLen': dk_len,
                'n': iterations,  # cost (as given in bifrost)
                'r': scrypt_r,  # blocksize
                'p': scrypt_p  # parallelization
            }
        )
    else:
        raise NotImplementedError("Not yet implemented")


def decode_keyfile_json(raw_keyfile_json, password):
    keyfile_json = normalize_keys(raw_keyfile_json)
    version = keyfile_json['version']

    if version == 0 or version == 1 or version == 2:
        return _decode_keyfile_json(keyfile_json, password)
    else:
        raise NotImplementedError("Not yet implemented")


def extract_key_from_keyfile(path_or_file_obj, password):
    keyfile_json = load_keyfile(path_or_file_obj)
    private_key = decode_keyfile_json(keyfile_json, password)
    return private_key


@to_dict
def normalize_keys(keyfile_json):
    for key, value in keyfile_json.items():
        if is_string(key):
            norm_key = key.lower()
        else:
            norm_key = key

        if is_dict(value):
            norm_value = normalize_keys(value)
        else:
            norm_value = value

        yield norm_key, norm_value


def _create_keyfile_json(private_key, password, kdf, network_prefix: NetworkId, proposition_type: str, salt_size=16,
                         kdf_params=None):
    salt = Random.get_random_bytes(salt_size)

    if kdf_params is None:
        kdf_params = get_default_kdf_params_for_kdf(kdf)
    if kdf == 'scrypt':
        derived_key = _scrypt_hash(
            password,
            salt=salt,
            buflen=kdf_params['dkLen'],
            r=kdf_params['r'],
            p=kdf_params['p'],
            n=kdf_params['n'],
        )
        kdf_params['salt'] = b58encode(salt).decode("latin-1")
    else:
        raise NotImplementedError("KDF not implemented: {0}".format(kdf))

    preformatted_iv = Random.get_random_bytes(16)
    iv = big_endian_to_int(preformatted_iv)
    encrypt_key = derived_key
    ciphertext = encrypt_aes_ctr(private_key, encrypt_key, iv)
    mac = get_mac(derived_key, ciphertext)

    address = keys.SigningKey(private_key).public_key.to_address(network_prefix, proposition_type)

    return {
        'address': str(address),
        'crypto': {
            'cipher': 'aes-128-ctr',
            'cipherparams': {
                'iv': b58encode(preformatted_iv).decode("latin-1"),
            },
            'ciphertext': b58encode(ciphertext).decode("latin-1"),
            'kdf': kdf,
            'kdfparams': kdf_params,
            'mac': b58encode(mac).decode("latin-1"),
        },
        'id': str(uuid.uuid4()),
        'version': 2,
    }


#
# Verson 0,1 and 2 decoder
#
def _decode_keyfile_json(keyfile_json, password):
    crypto = keyfile_json['crypto']
    kdf = crypto['kdf']

    # Derive the encryption key from the password using the key derivation
    # function.
    if kdf == 'scrypt':
        derived_key = _derive_scrypt_key(crypto, password)
    else:
        raise TypeError("Unsupported key derivation function: {0}".format(kdf))

    # Validate that the derived key matchs the provided MAC
    ciphertext = b58decode(crypto['ciphertext'])
    mac = get_mac(derived_key, ciphertext)

    expected_mac = b58decode(crypto['mac'])

    if not hmac.compare_digest(mac, expected_mac):
        raise ValueError("MAC mismatch")

    # Decrypt the ciphertext using the derived encryption key to get the
    # private key.
    encrypt_key = derived_key
    cipherparams = crypto['cipherparams']
    iv = big_endian_to_int(b58decode(cipherparams['iv']))

    private_key = decrypt_aes_ctr(ciphertext, encrypt_key, iv)

    return private_key


def _derive_scrypt_key(crypto, password):
    kdf_params = crypto['kdfparams']
    salt = b58decode(kdf_params['salt'])
    p = kdf_params['p']
    r = kdf_params['r']
    n = kdf_params['n']
    buflen = kdf_params['dklen']

    derived_scrypt_key = _scrypt_hash(
        password,
        salt=salt,
        n=n,
        r=r,
        p=p,
        buflen=buflen,
    )
    return derived_scrypt_key


def _scrypt_hash(password, salt, n, r, p, buflen):
    derived_key = scrypt(
        password,
        salt=salt,
        key_len=buflen,
        N=n,
        r=r,
        p=p,
        num_keys=1,
    )
    return derived_key


def encrypt_aes_ctr(value, key, iv):
    ctr = Counter.new(128, initial_value=iv, allow_wraparound=True)
    encryptor = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = encryptor.encrypt(value)
    return ciphertext


def decrypt_aes_ctr(ciphertext, key, iv):
    ctr = Counter.new(128, initial_value=iv, allow_wraparound=True)
    encryptor = AES.new(key, AES.MODE_CTR, counter=ctr)
    return encryptor.decrypt(ciphertext)


#
# Utility
#
def get_default_kdf_params_for_kdf(kdf):
    if kdf == 'scrypt':
        # Key derivation function parameters
        return {
            'dkLen': 32,
            'n': 2 ** 18,  # cost (as given in bifrost)
            'r': 8,  # blocksize
            'p': 1  # parallelization
        }
    else:
        raise ValueError("Unsupported key derivation function: {0}".format(kdf))
