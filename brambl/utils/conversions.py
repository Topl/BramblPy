from typing import Union, Callable

from brambl.base58 import encode_base58
from brambl.encoding import int_to_big_endian
from brambl.typing.encoding import HexStr, Base58Str
from brambl.utils.decorators import validate_conversion_arguments, T
from brambl.utils.hex import add_0x_prefix, encode_hex, decode_hex, remove_0x_prefix
from brambl.utils.types import is_boolean, is_string, is_integer

Primitives = Union[bytes, int, bool]


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
        return Base58Str(encode_base58(decode_hex(hexstr)))

    if text is not None:
        return Base58Str(encode_base58(text.encode("utf-8")))

    if is_boolean(primitive):
        return Base58Str("1") if primitive else Base58Str("0")

    if isinstance(primitive, (bytes, bytearray)):
        return Base58Str(encode_base58(primitive))
    elif is_string(primitive):
        raise TypeError(
            "Unsupported type: The primitive argument must be one of: bytes,"
            "bytearray, int or bool and not str"
        )

    if is_integer(primitive):
        return Base58Str(encode_base58(hex(primitive)))

    raise TypeError(
        "Unsupported type: '{0}'.  Must be one of: bool, str, bytes, bytearray"
        "or int.".format(repr(type(primitive)))
    )


@validate_conversion_arguments
def to_text(
        primitive: Primitives = None, base58str: Base58Str = None, text: str = None, hexstr: HexStr = None
) -> str:
    if base58str is not None:
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


def text_if_str(
        to_type: Callable[..., T], text_or_primitive: Union[bytes, int, str]
) -> T:
    """
    Convert to a type, assuming that strings can be only latin1 text (not a base58str).

    :param to_type: takes the arguments (primitive, base58str=base58str, text=text),
        eg~ to_bytes, to_text, to_base58, to_int, etc
    :param text_or_primitive: bytes, str, int - value to convert
    """
    if isinstance(text_or_primitive, str):
        return to_type(text=text_or_primitive)
    else:
        return to_type(text_or_primitive)


@validate_conversion_arguments
def to_bytes(
        primitive: Primitives = None, hexstr: HexStr = None, text: str = None
) -> bytes:
    if is_boolean(primitive):
        return b"\x01" if primitive else b"\x00"
    elif isinstance(primitive, bytearray):
        return bytes(primitive)
    elif isinstance(primitive, bytes):
        return primitive
    elif isinstance(primitive, int):
        # Note that this int check must come after the bool check, because
        #   isinstance(True, int) is True
        if primitive < 0:
            raise ValueError(f"Cannot convert negative integer {primitive} to bytes")
        else:
            return to_bytes(hexstr=HexStr(hex(primitive)))
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
