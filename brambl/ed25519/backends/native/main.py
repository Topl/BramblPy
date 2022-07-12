from abc import ABC
from typing import Optional  # noqa: F401

from nacl.bindings import crypto_sign, crypto_sign_BYTES, crypto_sign_open, crypto_scalarmult_base

from brambl.topl_base58.encoding import Base58Encoder
from brambl.ed25519.backends import BaseEd25519Backend
from brambl.ed25519.datatypes import BaseSignature, PublicKey, BaseEd25519Key, SigningKey, SignedMessage


class NativeECCBackend(BaseEd25519Backend, ABC, BaseEd25519Key):
    def ecc_sign(self,
                 message: bytes,
                 private_key: SigningKey,
                 encoder=Base58Encoder,
                 ) -> SignedMessage:
        raw_signed = crypto_sign(message, private_key.to_bytes())
        signature = encoder.encode(raw_signed[:crypto_sign_BYTES])

        signature = BaseSignature(signature_bytes=signature, encoder=encoder)

        message = encoder.encode(raw_signed[crypto_sign_BYTES:])
        signed = encoder.encode(raw_signed)
        return SignedMessage.from_parts(signature, message, signed, encoder)

    def ecc_verify(self, signature: BaseSignature,
                   public_key: PublicKey, message: bytes, encoder=Base58Encoder) -> bytes:
        """
        Verifies the signature of a signed message, returning the message
        if it has not been tampered with else raising
        :class:`~brambl.ed25519.BadSignature`.

        :param message: [:class:`bytes`] Either the original message or a
            signature and message concatenated together.
        :param signature: [:class:`bytes`] If an unsigned message is given for
            message then the detached signature must be provided.
        :rtype: :class:`bytes`
        """
        if signature is not None:
            # If we were given the message and signature separately, validate
            #   signature size and combine them.
            if len(signature.to_bytes()) != crypto_sign_BYTES:
                raise ValueError(
                    "The signature must be exactly %d bytes long"
                    % crypto_sign_BYTES,
                )

            smessage = signature.to_bytes() + encoder.decode(message)
        else:
            # Decode the signed message
            smessage = encoder.decode(message)

        return crypto_sign_open(smessage, public_key.to_bytes())

    def private_key_to_public_key(self, private_key: SigningKey) -> PublicKey:
        public_key_bytes = crypto_scalarmult_base(private_key.to_bytes())
        public_key = PublicKey(public_key_bytes)
        return public_key
