from typing import AnyStr

from base58 import b58encode

from brambl.typing.encoding import Base58Str
from brambl.utils.types import is_string


def encode_base58(value: AnyStr) -> Base58Str:
    if not is_string(value):
        raise TypeError("Value must be an instance of str or unicode")
    elif isinstance(value, (bytes, bytearray)):
        latin1_bytes = value
    else:
        latin1_bytes = value.encode("latin-1")

    binary_base58 = b58encode(latin1_bytes)
    return Base58Str(binary_base58.decode("latin-1"))