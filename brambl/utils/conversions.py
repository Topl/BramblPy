from typing import Callable, TypeVar, Union

from nacl.encoding import HexEncoder

from brambl.typing.encoding import Primitives, HexStr, Base58Str
from brambl.utils.decorators import validate_conversion_arguments
from brambl.utils.encoding import Base58Encoder
from brambl.utils.types import is_boolean

T = TypeVar("T")


def text_if_str(
        to_type: Callable[..., T], text_or_primitive: Union[bytes, int, str]
) -> T:
    """
    Convert to a type, assuming that strings can be only latin1 text (not a base58str).

    :param to_type function: takes the arguments (primitive, base58str=base58str, text=text),
        eg~ to_bytes, to_text, to_base58, to_int, etc
    :param text_or_primitive bytes, str, int: value to convert
    """
    if isinstance(text_or_primitive, str):
        return to_type(text=text_or_primitive)
    else:
        return to_type(text_or_primitive)


def is_integer(primitive):
    pass


@validate_conversion_arguments
def to_bytes(
        primitive: Primitives = None, hexstr: HexStr = None, text: str = None, base58str: Base58Str = None
) -> bytes:
    if is_boolean(primitive):
        return b"\x01" if primitive else b"\x00"
    elif isinstance(primitive, bytearray):
        return bytes(primitive)
    elif isinstance(primitive, bytes):
        return primitive
    elif is_integer(primitive):
        return to_bytes(hexstr=HexEncoder.decode(primitive))
    elif hexstr is not None:
        if len(hexstr) % 2:
            # type check ignored here because casting an Optional arg to str is not possible
            hexstr = "0x0" + remove_0x_prefix(hexstr)  # type: ignore
        return HexEncoder.decode(hexstr)
    elif base58str is not None:
        return Base58Encoder.decode(Base58Str)
    elif text is not None:
        return text.encode("latin-1")
    raise TypeError(
        "expected a bool, int, byte or bytearray in first arg, or keyword of hexstr, base58str or text"
    )
