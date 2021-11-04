import binascii
from typing import AnyStr

from brambl.typing.encoding import HexStr
from brambl.utils.types import is_text, is_string


def decode_hex(value: str) -> bytes:
    if not is_text(value):
        raise TypeError("Value must be an instance of str")
    non_prefixed = remove_0x_prefix(HexStr(value))
    # unhexlify will only accept bytes type someday
    ascii_hex = non_prefixed.encode("ascii")
    return binascii.unhexlify(ascii_hex)


def add_0x_prefix(value: HexStr) -> HexStr:
    if is_0x_prefixed(value):
        return value
    return HexStr("0x" + value)


def encode_hex(value: AnyStr) -> HexStr:
    if not is_string(value):
        raise TypeError("Value must be an instance of str or unicode")
    elif isinstance(value, (bytes, bytearray)):
        ascii_bytes = value
    else:
        ascii_bytes = value.encode("ascii")

    binary_hex = binascii.hexlify(ascii_bytes)
    return add_0x_prefix(HexStr(binary_hex.decode("ascii")))


def is_0x_prefixed(value: str) -> bool:
    if not is_text(value):
        raise TypeError(
            "is_0x_prefixed requires text typed arguments. Got: {0}".format(repr(value))
        )
    return value.startswith("0x") or value.startswith("0X")


def remove_0x_prefix(value: HexStr) -> HexStr:
    if is_0x_prefixed(value):
        return HexStr(value[2:])
    return value
