from abc import (
    ABC,
    abstractmethod,
)

class BaseCredential(ABC):
    """
    Specify convenience methods to generate proofs for tranasactions, as well as propositions (the most common currently
    being the public_key_hash.
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
    def generate_proof_for_message(self, signable_message: bytes):
        """
        Sign the Bifrost message.

        This uses the same structure
        as in particular credential implementations, but without specifying whether a private key, script, or
        other mechanism is used to generate the proof

        :param signable_message: The serialized message, ready for signing
        """
        pass

    @abstractmethod
    def generate_proof_for_transaction(self, transaction_dict):
        """
        Sign a transaction dict.

        This uses the same structure as in
        particular credential implementations, but without specifying whether a private key, script, or other
        mechanism is used to generate the proof

        :param dict transaction_dict: transaction with all fields specified
        """
        pass

    def __eq__(self, other):
        """
        Equality test between two credentials.

        Two accounts are considered the same if they are exactly the same type,
        and can sign for the same address.
        """
        return type(self) == type(other) and self.address == other.address

    def __hash__(self):
        return hash((type(self), self.address))
