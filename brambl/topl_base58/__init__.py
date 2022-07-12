from typing import AnyStr, Union

from base58 import b58encode, b58decode

from brambl.topl_typing.encoding import Base58Str
from brambl.utils.types import is_string


def isBase58(sb: Union[str, bytes]) -> bool:
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'latin-1')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return b58encode(b58decode(sb_bytes)) == sb_bytes
    except Exception:
        return False

def encode_base58(value: AnyStr) -> Base58Str:
    if not is_string(value):
        raise TypeError("Value must be an instance of str or unicode")
    elif isinstance(value, (bytes, bytearray)):
        latin1_bytes = value
    else:
        latin1_bytes = value.encode("latin-1")

    binary_base58 = b58encode(latin1_bytes)
    return Base58Str(binary_base58.decode("latin-1"))