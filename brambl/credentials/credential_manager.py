"""
credential_manager.py
====================================
Create, import, and export Topl Bifrost keys.
Also allows for signing of transactions

"""
import json
# Dependencies
import os

from Crypto.Hash import BLAKE2b
from hexbytes import HexBytes

from brambl.topl_base58.encoding import Base58Encoder
from brambl.credentials.datastructures import Ed25519Proof
from brambl.credentials.local import LocalCredential
from brambl.ed25519 import keys, Ed25519API
# Default options for key generation as of 2020.08.01
from brambl.ed25519.utils.address import NetworkId
from brambl.ed25519.utils.constants import ed25519
from brambl.keyfile.keyfile import decode_keyfile_json, create_keyfile_json
from brambl.typing.encoding import Base58Str
from brambl.utils.conversions import to_bytes
from brambl.utils.curried import text_if_str
from brambl.utils.decorators import combomethod
from brambl.utils.exceptions import ValidationError
from brambl.utils.types import is_dict


# Generic key methods

class Ed25519CredentialManager(object):
    """
        The primary entry point for working with Topl knowledge proposition credentials (credentials that support
        signing using a private key

        It does **not** require a connection to a Bifrost node.
        """
    _keys = keys

    _default_kdf = os.getenv('TOPL_CREDENTIAL_KDF', 'scrypt')

    @combomethod
    def create(self, network_prefix: NetworkId, extra_entropy=''):
        """
        Creates a new credential, and returns it as a :class:`~brambl.ed25519.`.

        :param extra_entropy: Add extra randomness to whatever randomness your OS can provide
        :type extra_entropy: str or bytes or int
        :param network_prefix: The network on which this new credential will be used
        :type network_prefix: :class: NetworkId
        :returns: an object with private key and convenience methods

        """

        def bifrostBlake2b(buffer):
            blake = BLAKE2b.new(digest_bits=256)
            return blake.update(buffer).digest()

        extra_key_bytes = text_if_str(to_bytes, extra_entropy)
        seed_bytes = bifrostBlake2b(os.urandom(32 - len(extra_key_bytes)) + extra_key_bytes)
        ed25519_private_key = keys.SigningKey(seed_bytes)
        return self.from_key(ed25519_private_key, network_prefix)

    @combomethod
    def from_key(self, private_key, network_prefix: NetworkId):
        r"""
        Returns a convenient credential object for working with the given private key.

        :param private_key: The raw private key
        :type private_key: hex str, bytes, int or :class:`brambl.ed25519.datatypes.SigningKey`
        :param network_prefix: The network prefix of the credential that is created using this key.
        :type network_prefix: :class: `NetworkId`
        :return: object with methods for signing and encrypting
        :rtype: LocalCredential

        .. doctest:: python

            >>> credential = Ed25519CredentialManager(.from_key(
            ... 0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364)
            >>> credential.address
            '9dTrPSfxy9FyBJejxWMhcsKMw8ZV5MSioMLjgCZQLKEoc8iELQ9'

            # These methods are also available: sign_message(), sign_transaction(), encrypt()
            # They correspond to the same-named methods in CredentialManager*
            # but without the private key argument
        """
        key = self._parseSigningKey(private_key)
        return LocalCredential(key, self, network_prefix, ed25519)

    @staticmethod
    def decrypt(keyfile_json, password):
        """
            Decrypts a private key.

            The key may have been encrypted using a Bifrost client or :meth:`~CredentialManager.encrypt`.

            :param keyfile_json: The encrypted key
            :type keyfile_json: dict or str
            :param str password: The password that was used to encrypt the key
            :returns: the raw private key
            :rtype: ~Base58Str

            .. doctest:: python

                >>> encrypted = {
    'Crypto': {
        'cipher': 'aes-256-ctr',
        'cipherparams': {
            'iv': 'D1bnzq5VUH3R6TPvkrqCnq',
        },
        'ciphertext': 'ErMJrbu35u8Y6NbuagEaZKWkUPk9MoFD4dfxeQzvPXL4',
        'kdf': 'scrypt',
        'kdfparams': {
            'dklen': 32,
            'n': 8192,
            'p': 1,
            'r': 8,
            'salt': '2G3JuACUCnjLFcCmDmD9pSUWY9ryRpwVj89bioAFbUjt',
        },
        'mac': '3ibMYUndvubiUnb2nnisiRxZCWW5xcgqFCE97WUu5KFv',
    },
    'address': 'AUEgyX7QfKW2x2RVthNheLPAToQwxYjYiACgLjRY5XKPW5pMRG72',
    'id': '3c8efdd6-d538-47ec-b241-36783d3418b9',
    'version': 2,
}
                >>> Ed25519CredentialManager.decrypt(encrypted, 'test')
                4vJ9JU1bJJE96FWSJKvHsmmFADCg4gpZQff4P3bkLKi

            """
        if isinstance(keyfile_json, str):
            keyfile = json.loads(keyfile_json)
        elif is_dict(keyfile_json):
            keyfile = keyfile_json
        else:
            raise TypeError("The keyfile should be supplied as a JSON string, or a dictionary.")
        password_bytes = text_if_str(to_bytes, password)
        return Base58Str(decode_keyfile_json(keyfile, password_bytes))

    @classmethod
    def encrypt(cls, private_key, password, network_prefix: NetworkId, kdf=None, iterations=None):
        """
                Creates a dictionary with an encrypted version of your private key.
                To import this keyfile into a Bifrost client:
                encode this dictionary with :func:`json.dumps` and save it to disk where your
                client keeps key files.

                :param private_key: The raw private key
                :type private_key: hex str, bytes, int or :class:`brambl.ed25519.datatypes.SigningKey`
                :param str password: The password which you will need to unlock the address in your client
                :param network_prefix: The network on which your credential will be used
                :param str kdf: The key derivation function to use when encrypting your private key
                :param int iterations: The work factor for the key derivation function
                :returns: The data to use in your encrypted file
                :rtype: dict

                If kdf is not set, the default key derivation function falls back to the
                environment variable :envvar:`TOPL_CREDENTIAL_KDF`. If that is not set, then
                'scrypt' will be used as the default.

                .. doctest:: python

            >>> from pprint import pprint
            >>> encrypted = Ed25519CredentialManager.encrypt(
            ...     0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364,
            ...     'password'
            ... )
            >>> pprint(encrypted)

            {
    'Crypto': {
        'cipher': 'aes-256-ctr',
        'cipherparams': {
            'iv': 'D1bnzq5VUH3R6TPvkrqCnq',
        },
        'ciphertext': 'ErMJrbu35u8Y6NbuagEaZKWkUPk9MoFD4dfxeQzvPXL4',
        'kdf': 'scrypt',
        'kdfparams': {
            'dklen': 32,
            'n': 8192,
            'p': 1,
            'r': 8,
            'salt': '2G3JuACUCnjLFcCmDmD9pSUWY9ryRpwVj89bioAFbUjt',
        },
        'mac': '3ibMYUndvubiUnb2nnisiRxZCWW5xcgqFCE97WUu5KFv',
    },
    'address': 'AUEgyX7QfKW2x2RVthNheLPAToQwxYjYiACgLjRY5XKPW5pMRG72',
    'id': '3c8efdd6-d538-47ec-b241-36783d3418b9',
    'version': 2,
}
    >>> with open('my-keyfile', 'w') as f: # doctest: +SKIP
            ...    f.write(json.dumps(encrypted))

        """
        if isinstance(private_key, keys.SigningKey):
            key_bytes = private_key.to_bytes()
        else:
            key_bytes = HexBytes(private_key)

        if kdf is None:
            kdf = cls._default_kdf

        password_bytes = text_if_str(to_bytes, password)
        assert len(key_bytes) == 32

        return create_keyfile_json(key_bytes, password_bytes, network_prefix, ed25519, kdf=kdf, iterations=iterations)

    @combomethod
    def _parseSigningKey(self, key):
        """
        Generate a :class:`brambl.ed25519.datatypes.SigningKey` from the provided key.

        If the key is already of type :class:`brambl.ed25519.datatypes.SigningKey`, return the key.

        :param key: the private key from which a :class:`brambl.ed25519.datatypes.SigningKey`
                    will be generated
        :type key: hex str, bytes, int or :class:`brambl.ed25519.datatypes.SigningKey`
        :returns: the provided key represented as a :class:`brambl.ed25519.datatypes.SigningKey`
        """
        if isinstance(key, self._keys.SigningKey):
            return key
        elif isinstance(key, str):
            try:
                return self._keys.SigningKey(to_bytes(hexstr=key))
            except ValidationError as original_exception:
                raise ValueError(
                    "The private key must be exactly 32 bytes long, instead of "
                    "%d bytes." % len(key)
                ) from original_exception

        try:
            return self._keys.SigningKey(to_bytes(key))
        except ValidationError as original_exception:
            raise ValueError(
                "The private key must be exactly 32 bytes long, instead of "
                "%d bytes." % len(key)
            ) from original_exception

    @combomethod
    def _generate_proof(self, signable_message: bytes, private_key, encoder=Base58Encoder):
        """
        Signs the provided message

        This API supports only the bytes messaging format.

        :param signable_message: the encoded message for signing
        :param private_key: the key to sign the message with
        :type private_key: hex str, bytes, int or :class:`brambl.ed25519.datatypes.SigningKey`
        :returns: Various details about the proof - most importantly the public key and signature fields
        :rtype: ~brambl.ed25519.datatypes.SignedMessage
        """
        key = self._parseSigningKey(private_key)
        signature_bytes = keys.ecc_sign(signable_message, key, encoder=encoder)
        return Ed25519Proof(public_key=key.public_key, signature=signature_bytes.signature)

    @combomethod
    def sign_transaction(self, transaction_dict, private_key):
        """
        Signs a transaction using a local private key.

        It produces signature details and the Base58 encoded proof suitable for broadcast using
        :meth: `brambl.broadcastTransaction()`
        """
        pass

    def set_key_backend(self, backend):
        """
        Change the backend used by the underlying ed25519 library.

        *(The default is fine for most users)*

        :param backend: any backend that works in
            `brambl.Ed25519Api(backend)`_

        """
        self._keys = Ed25519API(backend)
