from brambl.credentials.base import BaseCredential
from brambl.ed25519.utils.address import NetworkId
from brambl.utils.encoding import Base58Encoder


class LocalCredential(BaseCredential):
    r"""
    A collection of convenience methods to sign and encrypt, with an embedded private key.

    .. code-block:: python

        >>> my_local_credential.address # doctest: +SKIP
        "9dTrPSfxy9FyBJejxWMhcsKMw8ZV5MSioMLjgCZQLKEoc8iELQ9"
        >>> my_local_credential.key # doctest: +SKIP
        b"\x01\x23..."

    You can also get the public key by casting the account to :class:`bytes`:

    .. code-block:: python

        >>> bytes(my_local_credential) # doctest: +SKIP
        b"\\x01\\x23..."
    """

    def __init__(self, key, credential_manager, network_prefix: NetworkId, proposition_type: str):
        """
        Initialize a new account with the the given private key.

        :param brambl.ed25519.datatypes.SigningKey key: to prefill in private key execution
        :param ~brambl.ed25519.Ed25519API credential_manager: the key-unaware management API
        """
        self._public_api = credential_manager

        self._address = credential_manager.keys.private_key_to_public_key(key).to_address(network_prefix,
                                                                                          proposition_type)

        self._private_key = key
        self._public_key = key.public_key.to_bytes()

        self._key_obj = key

    @property
    def address(self):
        return self._address

    @property
    def key(self):
        """
        Get the public key.
        """
        return self._public_key

    def encrypt(self, password, kdf=None, iterations=None):
        """
        Generate a string with the encrypted key.
        """
        return self._public_api.encrypt(self.key, password, kdf=kdf, iterations=iterations)

    def _generate_proof_for_message(self, signable_message: bytes, encoder=Base58Encoder):
        """
        Generate a proof using the private key.
        """
        return self._public_api._generate_proof(signable_message, private_key=self._private_key, encoder=encoder)

    def sign_message(self, signable_message: bytes, encoder=Base58Encoder):
        return self._generate_proof_for_message(signable_message, encoder=encoder)

    def _generate_proof_for_transaction(self, transaction_dict):
        pass

    def sign_transaction(self, transaction_dict):
        return self._generate_proof_for_transaction(transaction_dict)

    def __bytes__(self):
        return self.key
