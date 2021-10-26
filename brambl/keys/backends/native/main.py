from abc import ABC
from typing import Optional  # noqa: F401

from nacl.bindings import crypto_sign, crypto_sign_BYTES, crypto_sign_open, crypto_scalarmult_base

from brambl.keys.backends import BaseECCBackend
from brambl.keys.datatypes import BaseSignature, PublicKey, BaseKey, PrivateKey, SignedMessage
from brambl.utils.encoding import Base58Encoder


class NativeECCBackend(BaseECCBackend, ABC, BaseKey):
    def ecc_sign(self,
                 msg_hash: bytes,
                 private_key: PrivateKey,
                 encoder=Base58Encoder,
                 ) -> SignedMessage:
        raw_signed = crypto_sign(msg_hash, private_key.to_bytes())
        signature = encoder.encode(raw_signed[:crypto_sign_BYTES])

        signature = BaseSignature(signature_bytes=signature, encoder=encoder)

        message = encoder.encode(raw_signed[crypto_sign_BYTES:])
        signed = encoder.encode(raw_signed)
        return SignedMessage.from_parts(signature, message, signed)

    def ecc_verify(self, signature: BaseSignature,
                   public_key: PublicKey, msg_hash: Optional[bytes] = None, encoder=Base58Encoder) -> bytes:
        """
        Verifies the signature of a signed message, returning the message
        if it has not been tampered with else raising
        :class:`~brambl.keys.BadSignature`.

        :param msg_hash: [:class:`bytes`] Either the original message or a
            signature and message concatenated together.
        :param signature: [:class:`bytes`] If an unsigned message is given for
            msg_hash then the detached signature must be provided.
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

            smessage = signature.to_bytes() + encoder.decode(msg_hash)
        else:
            # Decode the signed message
            smessage = encoder.decode(msg_hash)

        return crypto_sign_open(smessage, public_key.to_bytes())

    def private_key_to_public_key(self, private_key: PrivateKey) -> PublicKey:
        public_key_bytes = crypto_scalarmult_base(private_key.to_bytes())
        public_key = PublicKey(public_key_bytes, backend=self)
        return public_key
