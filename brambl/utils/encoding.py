from typing import AnyStr, Any, Union

from base58 import b58encode, b58decode

from brambl.typing.encoding import Base58Str
from brambl.utils.base58 import encode_base58


def big_endian_to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")


class Base58Encoder:
    @staticmethod
    def encode(data: AnyStr) -> Base58Str:
        return encode_base58(data)

    @staticmethod
    def decode(data: Union[str, bytes]) -> bytes:
        return b58decode(data)
