#  Module should no longer have access to the full brambl api.
#  Only the calling functions need access to the request methods.
#  Any "re-entrant" shenanigans can go in the middlewares, which do
#  have brambl access.
from collections import Callable
from typing import Any, Coroutine

from toolz import curry, pipe

from brambl.Brambl import Brambl
from brambl.method import Method
from brambl.types import TReturn, RPCResponse


@curry
def apply_result_formatters(
    result_formatters: Callable[..., Any], result: RPCResponse
) -> RPCResponse:
    if result_formatters:
        formatted_result = pipe(result, result_formatters)
        return formatted_result
    else:
        return result


@curry
def retrieve_blocking_method_call_fn(
        brambl: "Brambl", method: Method[Callable[..., TReturn]]
) -> Callable[..., TReturn]:
    def caller() -> TReturn:
        (method_str, params), response_formatters = method.process_params()  # noqa: E501
        result_formatters, error_formatters, null_result_formatters = response_formatters
        result = brambl.manager.request_blocking(method_str,
                                                 params,
                                                 error_formatters,
                                                 null_result_formatters)
        return apply_result_formatters(result_formatters, result)

    return caller


@curry
def retrieve_async_method_call_fn(
        brambl: "Brambl", method: Method[Callable[..., Any]]
) -> Callable[..., Coroutine[Any, Any, RPCResponse]]:
    async def caller() -> RPCResponse:
        (method_str, params), response_formatters = method.process_params()
        result_formatters, error_formatters, null_result_formatters = response_formatters
        result = await brambl.manager.coro_request(method_str,
                                               params,
                                               error_formatters,
                                               null_result_formatters)
        return apply_result_formatters(result_formatters, result)

    return caller


class Module:
    is_async = False

    def __init__(self, web3: "Brambl") -> None:
        if self.is_async:
            self.retrieve_caller_fn = retrieve_async_method_call_fn(web3, self)
        else:
            self.retrieve_caller_fn = retrieve_blocking_method_call_fn(web3, self)
        self.web3 = web3
