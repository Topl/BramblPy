#  Module should no longer have access to the full brambl api.
#  Only the calling functions need access to the request methods.
#  Any "re-entrant" shenanigans can go in the middlewares, which do
#  have brambl access.
from typing import Any, Coroutine, TYPE_CHECKING, Callable

from toolz import curry, pipe

from brambl.types import TReturn, RPCResponse
from brambl.method import Method

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401


@curry
def retrieve_blocking_method_call_fn(
        brambl: "Brambl", module: "Module", method: Method[Callable[..., TReturn]]
) -> Callable[..., TReturn]:
    def caller(*args: Any, **kwargs: Any) -> TReturn:
        (method_str, params) = method.process_params(module, *args, **kwargs)  # noqa: E501
        result = brambl.manager.request_blocking(method_str,
                                                 params)
        return result

    return caller


@curry
def retrieve_async_method_call_fn(
        brambl: "Brambl", module: "Module", method: Method[Callable[..., Any]]
) -> Callable[..., Coroutine[Any, Any, RPCResponse]]:
    async def caller(*args: Any, **kwargs: Any) -> RPCResponse:
        (method_str, params), response_formatters = method.process_params(module, *args, **kwargs)
        result = await brambl.manager.coro_request(method_str,
                                                   params)
        return result

    return caller


class Module:
    is_async = False

    def __init__(self, web3: "Brambl") -> None:
        if self.is_async:
            self.retrieve_caller_fn = retrieve_async_method_call_fn(web3, self)
        else:
            self.retrieve_caller_fn = retrieve_blocking_method_call_fn(web3, self)
        self.web3 = web3
