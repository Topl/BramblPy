from typing import AnyStr, Union

from base58 import b58decode

from brambl.base58 import encode_base58
from brambl.typing.encoding import Base58Str


class Base58Encoder:
    @staticmethod
    def encode(data: AnyStr) -> Base58Str:
        return encode_base58(data)

    @staticmethod
    def decode(data: Union[str, bytes]) -> bytes:
        return b58decode(data)
