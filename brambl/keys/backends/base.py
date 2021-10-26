from __future__ import annotations

from typing import Optional

from brambl.keys.datatypes import PrivateKey, BaseSignature, PublicKey
from brambl.utils.encoding import Base58Encoder


class BaseECCBackend(object):
    def ecc_sign(self,
                   msg_hash: bytes,
                   private_key: PrivateKey,
                   encoder=Base58Encoder,
                 ) -> BaseSignature:
        raise NotImplementedError()

    def ecc_verify(self,
                     msg_hash: Optional[bytes],
                     signature: BaseSignature,
                     public_key: PublicKey,
                     encoder=Base58Encoder
                   ) -> bytes:
        raise NotImplementedError()

    def private_key_to_public_key(self,
                                  private_key: PrivateKey) -> PublicKey:
        raise NotImplementedError()
