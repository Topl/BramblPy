import collections
import numbers
from typing import Any, Callable, Literal, NewType, Optional, TypedDict, Union, TypeVar

from brambl.datastructures import NamedElementOnion

TReturn = TypeVar("TReturn")
RPCEndpoint = NewType("RPCEndpoint", str)


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
