from typing import AnyStr, Union

from base58 import b58decode

from brambl.base58 import encode_base58
from brambl.typing.encoding import Base58Str


def big_endian_to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")


class Base58Encoder:
    @staticmethod
    def encode(data: AnyStr) -> Base58Str:
        return encode_base58(data)

    @staticmethod
    def decode(data: Union[str, bytes]) -> bytes:
        return b58decode(data)