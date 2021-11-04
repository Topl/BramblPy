from typing import Type

from brambl.ed25519.datatypes import LazyBackend, PublicKey, SigningKey, BaseSignature, SignedMessage

# These must be aliased due to a scoping issue in mypy
# https://github.com/python/mypy/issues/1775
from brambl.utils.encoding import Base58Encoder
from brambl.utils.exceptions import ValidationError
from brambl.utils.validation import validate_message

_PublicKey = PublicKey
_SigningKey = SigningKey
_Signature = SignedMessage


class Ed25519API(LazyBackend):
    #
    # datatype shortcuts
    #
    PublicKey = PublicKey  # type: Type[_PublicKey]
    SigningKey = SigningKey  # type: Type[_SigningKey]
    Signature = SignedMessage  # type: Type[_Signature]

    #
    # Proxy method calls to the backends
    #
    def ecc_sign(self,
                 message: bytes,
                 private_key: _SigningKey,
                 encoder=Base58Encoder
                 ) -> _Signature:
        validate_message(message)
        if not isinstance(private_key, SigningKey):
            raise ValidationError(
                "The `private_key` must be an instance of `brambl.ed25519.datatypes.SigningKey`"
            )
        signature = self.backend.ecc_sign(message, private_key, encoder=encoder)
        if not isinstance(signature.signature, BaseSignature):
            raise ValidationError(
                "Backend returned an invalid signature.  Return value must be "
                "an instance of `brambl.ed25519.datatypes.Signature`"
            )
        return signature

    def ecc_verify(self,
                   message: bytes,
                   signature: BaseSignature,
                   public_key: _PublicKey,
                   encoder=Base58Encoder) -> bytes:
        validate_message(message)
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "The `public_key` must be an instance of `brambl.ed25519.datatypes.PublicKey`"
            )
        if not isinstance(signature, BaseSignature):
            raise ValidationError(
                "The `signature` must be an instance of `brambl.ed25519.datatypes.BaseSignature`"
            )
        return self.backend.ecc_verify(signature, public_key, message, encoder)

    def private_key_to_public_key(self, private_key: _SigningKey) -> _PublicKey:
        if not isinstance(private_key, SigningKey):
            raise ValidationError(
                "The `private_key` must be an instance of `brambl.ed25519.datatypes.SigningKey`"
            )
        public_key = self.backend.private_key_to_public_key(private_key)
        if not isinstance(public_key, PublicKey):
            raise ValidationError(
                "Backend returned an invalid public_key.  Return value must be "
                "an instance of `brambl.ed25519.datatypes.PublicKey`"
            )
        return public_key


# This creates an easy to import backend which will lazily fetch whatever
# backend has been configured at runtime (as opposed to import or instantiation time).
lazy_key_api = Ed25519API(backend=None)
