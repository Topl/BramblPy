from typing import NewType, Union

from base58 import b58decode, b58encode
from brambl.types import is_boolean, is_integer, is_string
from brambl.utils.decorators import validate_conversion_arguments
from brambl.utils.encoding import int_to_big_endian
from brambl.utils.hex import add_0x_prefix, decode_hex, encode_hex

Primitives = Union[bytes, int, bool]
Base58Str = NewType('Base58Str', str)
HexStr = NewType('HexStr', str)

@validate_conversion_arguments
def to_hex(
    primitive: Primitives = None, hexstr: HexStr = None, text: str = None
) -> HexStr:
    """
    Auto converts any supported value into its hex representation.
    """
    if hexstr is not None:
        return add_0x_prefix(HexStr(hexstr.lower()))

    if text is not None:
        return encode_hex(text.encode("utf-8"))

    if is_boolean(primitive):
        return HexStr("0x1") if primitive else HexStr("0x0")

    if isinstance(primitive, (bytes, bytearray)):
        return encode_hex(primitive)
    elif is_string(primitive):
        raise TypeError(
            "Unsupported type: The primitive argument must be one of: bytes,"
            "bytearray, int or bool and not str"
        )

    if is_integer(primitive):
        return HexStr(hex(primitive))

    raise TypeError(
        "Unsupported type: '{0}'.  Must be one of: bool, str, bytes, bytearray"
        "or int.".format(repr(type(primitive)))
    )

@validate_conversion_arguments
def to_base58(
    primitive: Primitives = None, base58str: Base58Str = None, text: str = None, hexstr: HexStr = None
) -> Base58Str:
    """
    Auto converts any supported value into its hex representation.
    """
    if base58str is not None:
        return Base58Str(base58str.lower())

    if hexstr is not None:
        return Base58Str(b58encode(decode_hex(hexstr)))

    if text is not None:
        return Base58Str(b58encode(text.encode("utf-8")))

    if is_boolean(primitive):
        return Base58Str("1") if primitive else Base58Str("0")

    if isinstance(primitive, (bytes, bytearray)):
        return Base58Str(b58encode(primitive))
    elif is_string(primitive):
        raise TypeError(
            "Unsupported type: The primitive argument must be one of: bytes,"
            "bytearray, int or bool and not str"
        )

    if is_integer(primitive):
        return Base58Str(b58encode(hex(primitive)))

    raise TypeError(
        "Unsupported type: '{0}'.  Must be one of: bool, str, bytes, bytearray"
        "or int.".format(repr(type(primitive)))
    )


@validate_conversion_arguments
def to_text(
    primitive: Primitives = None, base58str: Base58Str = None, text: str = None, hexstr = HexStr
) -> str:
    if Base58Str is not None:
        return to_bytes(base58str=base58str).decode("utf-8")
    elif hexstr is not None:
        return to_bytes(hexstr=hexstr).decode("utf-8")
    elif text is not None:
        return text
    elif isinstance(primitive, str):
        return to_text(hexstr=primitive)
    elif isinstance(primitive, (bytes, bytearray)):
        return primitive.decode("utf-8")
    elif is_integer(primitive):
        byte_encoding = int_to_big_endian(primitive)
        return to_text(byte_encoding)
    raise TypeError("Expected an int, bytes, bytearray or hexstr.")

@validate_conversion_arguments
def to_bytes(
    primitive: Primitives = None, base58str: Base58Str = None, text: str = None,
    hexstr: HexStr = None
) -> bytes:
    if is_boolean(primitive):
        return b"\x01" if primitive else b"\x00"
    elif isinstance(primitive, bytearray):
        return bytes(primitive)
    elif isinstance(primitive, bytes):
        return primitive
    elif is_integer(primitive):
        return to_bytes(base58str=b58encode(primitive))
    elif base58str is not None:
        return b58decode(base58str)
    elif hexstr is not None:
        if len(hexstr) % 2:
            # type check ignored here because casting an Optional arg to str is not possible
            hexstr = "0x0" + remove_0x_prefix(hexstr)  # type: ignore
        return decode_hex(hexstr)
    elif text is not None:
        return text.encode("utf-8")
    raise TypeError(
        "expected a bool, int, byte or bytearray in first arg, or keyword of base58str or text"
    )