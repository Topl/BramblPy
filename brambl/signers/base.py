from abc import (
    ABC,
    abstractmethod,
)


class BaseCredential(ABC):
    """
    Specify convenience methods to sign transactions and message hashes.
    """

    @property
    @abstractmethod
    def address(self):
        """
        The checksummed public address for this account.

        .. code-block:: python

            >>> my_credential.address # doctest: +SKIP
            "9dTrPSfxy9FyBJejxWMhcsKMw8ZV5MSioMLjgCZQLKEoc8iELQ9"

        """
        pass

    @abstractmethod
    def signHash(self, message_hash):
        """
        Sign the hash of a message.

        :param bytes message_hash: the messageToSign that is returned from Bifrost via the rawTransfer JSON-RPC routes
        """
        pass

    def __eq__(self, other):
        """
        Equality test between two credentials.

        Two credentials are considered the same if they are exactly the same type,
        and can sign for the same address.
        """
        return type(self) == type(other) and self.address == other.address

    def __hash__(self):
        return hash((type(self), self.address))
