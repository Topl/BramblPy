import codecs
import collections
import sys
from typing import Any, Union, Type, Optional, TYPE_CHECKING
from abc import (
    ABC
)

from nacl.bindings import crypto_sign_SEEDBYTES, crypto_sign_seed_keypair, crypto_sign_PUBLICKEYBYTES
from nacl.encoding import RawEncoder
from nacl.utils import random

from brambl.base58 import encode_base58
from brambl.base58.encoding import Base58Encoder
from brambl.ed25519.utils.address import public_key_bytes_to_address, Address, NetworkId

# Must compare against version_info[0] and not version_info.major to please mypy.
from brambl.encoding import big_endian_to_int
from brambl.utils.Hash import digestAndEncode, hashFunc
from brambl.utils.types import is_bytes, is_string

if TYPE_CHECKING:
    from brambl.ed25519.backends.base import BaseEd25519Backend

if sys.version_info[0] == 2:
    ByteString = type(
        'BaseString',
        (Sequence, basestring),  # noqa: F821
        {},
    )  # type: Any
else:
    ByteString = collections.ByteString


class LazyBackend:
    def __init__(self,
                 backend: 'Union[BaseEd25519Backend, Type[BaseEd25519Backend], str, None]' = None,
                 ) -> None:
        from brambl.ed25519.backends.base import BaseEd25519Backend

        if backend is None:
            pass
        elif isinstance(backend, BaseEd25519Backend):
            pass
        elif isinstance(backend, type) and issubclass(backend, BaseEd25519Backend):
            backend = backend()
        elif is_string(backend):
            backend = self.get_backend(backend)
        else:
            raise ValueError(
                "Unsupported format for ECC backend.  Must be an instance or "
                "subclass of `ed25519.backends.BaseEd25519Backend` or a string of "
                "the dot-separated import path for the desired backend class"
            )

        self.backend = backend

    _backend = None  # type: BaseEd25519Backend

    @property
    def backend(self) -> 'BaseEd25519Backend':
        if self._backend is None:
            return self.get_backend()
        else:
            return self._backend

    @backend.setter
    def backend(self, value: 'BaseEd25519Backend') -> None:
        self._backend = value

    @classmethod
    def get_backend(cls, *args: Any, **kwargs: Any) -> 'BaseEd25519Backend':
        from brambl.ed25519.backends import get_backend
        return get_backend(*args, **kwargs)


class BaseEd25519Key(ByteString, collections.Hashable):
    _raw_key = None  # type: bytes

    def to_hex(self) -> str:
        # Need the 'type: ignore' comment below because of
        # https://github.com/python/typeshed/issues/300
        return '0x' + codecs.decode(codecs.encode(self._raw_key, 'hex'), 'ascii')  # type: ignore

    def to_bytes(self) -> bytes:
        return self._raw_key

    def __hash__(self) -> int:
        return big_endian_to_int(digestAndEncode(hashFunc().update(self.to_bytes())))

    def __str__(self) -> str:
        return self.to_hex()

    def __int__(self) -> int:
        return big_endian_to_int(self._raw_key)

    def __len__(self) -> int:
        return 32

    # Must be typed with `ignore` due to
    # https://github.com/python/mypy/issues/1237
    def __getitem__(self, index: int) -> int:  # type: ignore
        return self._raw_key[index]

    def __eq__(self, other: Any) -> bool:
        if hasattr(other, 'to_bytes'):
            return self.to_bytes() == other.to_bytes()
        elif is_bytes(other):
            return self.to_bytes() == other
        else:
            return False

    def __repr__(self) -> str:
        return "'{0}'".format(self.to_hex())

    def __index__(self) -> int:
        return self.__int__()

    def __hex__(self) -> str:
        if sys.version_info[0] == 2:
            return codecs.encode(self.to_hex(), 'latin-1')
        else:
            return self.to_hex()


class SigningKey(BaseEd25519Key, LazyBackend):
    """
        Private key for producing digital signatures using the Ed25519 algorithm.

        Signing ed25519 are produced from a 32-byte (256-bit) random seed value. This
        value can be passed into the :class:`~brambl.ed25519.datatypes.SigningKey` as a
        :func:`bytes` whose length is 32.

        .. warning:: This **must** be protected and remain secret. Anyone who knows
            the value of your :class:`~brambl.ed25519.datatypes.SigningKey` or it's seed can
            masquerade as you.

        :param seed: [:class:`bytes`] Random 32-byte value (i.e. private key)
        :param encoder: A class that is able to decode the seed

        :ivar: public_key: [:class:`~brambl.ed25519.datatypes.PublicKey`] The verify
            (i.e. public) key that corresponds with this signing key.
        """
    public_key = None  # type: PublicKey
    _raw_key = None  # type: bytes

    def __init__(self,
                 seed: bytes = None,
                 backend: 'Union[BaseEd25519Backend, Type[BaseEd25519Backend], str, None]' = None,
                 encoder=RawEncoder
                 ) -> None:
        seed = encoder.decode(seed)
        if not isinstance(seed, bytes):
            raise TypeError(
                "SigningKey must be created from a 32 byte seed"
            )

            # Verify that our seed is the proper size
        if len(seed) != crypto_sign_SEEDBYTES:
            raise ValueError(
                "The seed must be exactly %d bytes long"
                % crypto_sign_SEEDBYTES
            )

        public_key, secret_key = crypto_sign_seed_keypair(seed)

        self._seed = seed

        self._raw_key = secret_key
        self.public_key = PublicKey(public_key)

        super().__init__(backend=backend)

    @classmethod
    def generate(cls, seed=random(crypto_sign_SEEDBYTES), encoder=RawEncoder):
        seed = encoder.decode(seed)
        if not isinstance(seed, bytes):
            raise TypeError(
                "SigningKey must be created from a 32 byte seed"
            )
        return cls(
            seed=seed,
            encoder=encoder
        )


class PublicKey(BaseEd25519Key):

    def __init__(self,
                 key: bytes,
                 encoder=RawEncoder
                 ) -> None:
        key = encoder.decode(key)
        if not isinstance(key, bytes):
            raise TypeError("PublicKey must be created from 32 bytes")

        if len(key) != crypto_sign_PUBLICKEYBYTES:
            raise ValueError(
                "The key must be exactly %s bytes long"
                % crypto_sign_PUBLICKEYBYTES,
            )

        self._raw_key = key
        super().__init__()

    def to_address(self, network_prefix: NetworkId, proposition_type: str) -> \
            Address:
        return public_key_bytes_to_address(self.to_bytes(), network_prefix,
                                           proposition_type)


class BaseSignature(ByteString, ABC):
    """
        A ByteString subclass that holds a message that has been signed by a
        :class:`SigningKey`.
        """

    def __init__(self,
                 signature_bytes: bytes = None,
                 encoder=Base58Encoder
                 ) -> None:

        self._signature_bytes = signature_bytes
        self.encoder = encoder
        super().__init__()

    @property
    def signature_bytes(self) -> Optional[bytes]:
        return self._signature_bytes

    def to_bytes(self) -> bytes:
        return self.encoder.decode(self._signature_bytes)

    def __bytes__(self) -> bytes:
        return self.to_bytes()

    def to_base58(self) -> str:
        return encode_base58(self.to_bytes())

    def __hash__(self) -> int:
        return big_endian_to_int(digestAndEncode(self.to_bytes()))

    def __str__(self) -> str:
        return self.to_base58()

    def __len__(self) -> int:
        return len(bytes(self))

    def __eq__(self, other: Any) -> bool:
        if hasattr(other, 'to_bytes'):
            return self.to_bytes() == other.to_bytes()
        elif is_bytes(other):
            return self.to_bytes() == other
        else:
            return False

    # Must be typed with `ignore` due to
    # https://github.com/python/mypy/issues/1237
    def __getitem__(self, index: int) -> int:  # type: ignore
        return self.to_bytes()[index]

    def __repr__(self) -> str:
        return "'{0}'".format(self.to_hex())

    def __index__(self) -> int:
        return self.__int__()

    def __hex__(self) -> str:
        return self.to_hex()

    def __int__(self) -> int:
        return big_endian_to_int(self.to_bytes())

    def verify_msg(self,
                   message: bytes,
                   public_key: PublicKey) -> bool:
        message_hash = digestAndEncode(message)
        return self.verify_msg_hash(message_hash, public_key)

    def verify_msg_hash(self,
                        message_hash: bytes,
                        public_key: PublicKey) -> bool:
        return self.backend.ecc_verify(message_hash, self, public_key)


class SignedMessage(bytes):
    """
    A bytes subclass that holds a messaged that has been signed by a
    :class:`SigningKey`.
    """

    _signature = None
    _message = None

    @classmethod
    def from_parts(cls, signature, message, combined, encoder=Base58Encoder):
        decoded = encoder.decode(combined)
        obj = cls(decoded)
        obj._signature = signature
        obj._message = message
        return obj

    @property
    def signature(self):
        """
        The signature contained within the :class:`SignedMessage`.
        """
        return self._signature

    @property
    def message(self):
        """
        The message contained within the :class:`SignedMessage`.
        """
        return self._message
