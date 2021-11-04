import collections
import numbers
from typing import Any, Callable, Literal, NewType, Optional, TypedDict, Union, TypeVar

from brambl.datastructures import NamedElementOnion

TReturn = TypeVar("TReturn")
RPCEndpoint = NewType("RPCEndpoint", str)

bytes_types = (bytes, bytearray)
integer_types = (int,)
text_types = (str,)
string_types = (bytes, str, bytearray)


class RPCError(TypedDict):
    code: int
    message: str
    data: Optional[str]


class RPCResponse(TypedDict, total=False):
    error: Union[RPCError]
    id: int
    jsonrpc: Literal["2.0"]
    result: Any


Middleware = Callable[[Callable[[RPCEndpoint, Any], RPCResponse], "Brambl"], Any]
MiddlewareOnion = NamedElementOnion[str, Middleware]

URI = NewType('URI', str)


def is_integer(value: Any) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)


def is_text(value: Any) -> bool:
    return isinstance(value, text_types)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_boolean(value: Any) -> bool:
    return isinstance(value, bool)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, collections.abc.Mapping)


def is_list_like(obj: Any) -> bool:
    return not is_string(obj) and isinstance(obj, collections.abc.Sequence)


def is_list(obj: Any) -> bool:
    return isinstance(obj, list)


def is_tuple(obj: Any) -> bool:
    return isinstance(obj, tuple)


def is_null(obj: Any) -> bool:
    return obj is None


def is_number(obj: Any) -> bool:
    return isinstance(obj, numbers.Number)
