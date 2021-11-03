from operator import __getitem__
from typing import NamedTuple

from brambl.ed25519.datatypes import BaseSignature, PublicKey


class Ed25519Proof(NamedTuple):
    public_key: PublicKey
    signature: BaseSignature

    def __getitem__(self, index):
        return __getitem__(self, index)