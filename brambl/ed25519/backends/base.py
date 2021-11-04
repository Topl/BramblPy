from __future__ import annotations

from typing import Optional

from brambl.base58.encoding import Base58Encoder
from brambl.ed25519.datatypes import SigningKey, BaseSignature, PublicKey


class BaseEd25519Backend(object):
    def ecc_sign(self,
                   message: bytes,
                   private_key: SigningKey,
                   encoder=Base58Encoder,
                 ) -> BaseSignature:
        raise NotImplementedError()

    def ecc_verify(self,
                     message: Optional[bytes],
                     signature: BaseSignature,
                     public_key: PublicKey,
                     encoder=Base58Encoder
                   ) -> bytes:
        raise NotImplementedError()

    def private_key_to_public_key(self,
                                  private_key: SigningKey) -> PublicKey:
        raise NotImplementedError()
