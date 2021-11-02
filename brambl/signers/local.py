from brambl.signers.base import BaseCredential


class LocalCredential(BaseCredential):
    """
    A collection of convenience methods to sign and encrypt, with an embedded private key.

    :var bytes key: the 32-byte private key data

    .. code-block:: python

        >>> my_local_credential.address # doctest: +SKIP
        "9dTrPSfxy9FyBJejxWMhcsKMw8ZV5MSioMLjgCZQLKEoc8iELQ9"
        >>> my_local_credential.key # doctest: +SKIP
        b"\x01\x23..."

    You can also get the private key by casting the account to :class:`bytes`:

    .. code-block:: python

        >>> bytes(my_local_account) # doctest: +SKIP
        b"\\x01\\x23..."
    """
    def __init__(self, key, keyapi):
        """
        Initialize a new credential with the the given private key.

        :param ~brambl.keys.datatypes.PrivateKey key: to prefill in private key execution
        :param ~brambl.credentials.wallet wallet: the key-unaware management API
        """
        self._publicapi = keyapi

        self._address = key.public_key.to_address()

        key_raw = key.to_bytes()
        self._private_key = key_raw

        self._key_obj = key

    @property
    def address(self):
        return self._address

    @property
    def key(self):
        """
        Get the private key.
        """
        return self._private_key

    def encrypt(self, password, kdf=None, iterations=None):
        """
        Generate a string with the encrypted key.
        """
        return self._publicapi.encrypt(self.key, password, kdf=kdf, iterations=iterations)

    def signHash(self, message_hash):
        return self._publicapi.signHash(
            message_hash,
            private_key=self.key,
        )

    def __bytes__(self):
        return self.key
