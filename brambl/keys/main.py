from typing import Type

from brambl.keys.datatypes import LazyBackend, PublicKey, PrivateKey, BaseSignature

# These must be aliased due to a scoping issue in mypy
# https://github.com/python/mypy/issues/1775
from brambl.utils.encoding import Base58Encoder
from brambl.utils.exceptions import ValidationError
from brambl.utils.validation import validate_message_hash

_PublicKey = PublicKey
_PrivateKey = PrivateKey
_Signature = BaseSignature


class KeyAPI(LazyBackend):
    #
    # datatype shortcuts
    #
    PublicKey = PublicKey  # type: Type[_PublicKey]
    PrivateKey = PrivateKey  # type: Type[_PrivateKey]
    Signature = BaseSignature  # type: Type[_Signature]

    #
    # Proxy method calls to the backends
    #
    def ecc_sign(self,
                 message_hash: bytes,
                 private_key: _PrivateKey,
                 encoder=Base58Encoder
                 ) -> _Signature:
        validate_message_hash(message_hash)
        if not isinstance(private_key, PrivateKey):
            raise ValidationError(
                "The `private_key` must be an instance of `brambl.keys.datatypes.PrivateKey`"
            )
        signature = self.backend.ecc_sign(message_hash, private_key, encoder=encoder)
        if not isinstance(signature.signature, BaseSignature):
            raise ValidationError(
                "Backend returned an invalid signature.  Return value must be "
                "an instance of `brambl.keys.datatypes.Signature`"
            )
        return signature

    def ecc_verify(self,
                   message_hash: bytes,
                   signature: BaseSignature,
                   public_key: _PublicKey,
                   encoder=Base58Encoder) -> bytes:
        validate_message_hash(message_hash)
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "The `public_key` must be an instance of `brambl.keys.datatypes.PublicKey`"
            )
        if not isinstance(signature, BaseSignature):
            raise ValidationError(
                "The `signature` must be an instance of `brambl.keys.datatypes.BaseSignature`"
            )
        return self.backend.ecc_verify(signature, public_key, message_hash, encoder)

    def private_key_to_public_key(self, private_key: _PrivateKey) -> _PublicKey:
        if not isinstance(private_key, PrivateKey):
            raise ValidationError(
                "The `private_key` must be an instance of `brambl.keys.datatypes.PrivateKey`"
            )
        public_key = self.backend.private_key_to_public_key(private_key)
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "Backend returned an invalid public_key.  Return value must be "
                "an instance of `brambl.keys.datatypes.PublicKey`"
            )
        return public_key


# This creates an easy to import backend which will lazily fetch whatever
# backend has been configured at runtime (as opposed to import or instantiation time).
lazy_key_api = KeyAPI(backend=None)
