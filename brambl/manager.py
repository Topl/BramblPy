from logging import getLogger
from typing import TYPE_CHECKING, Callable, Any, Optional, Sequence, Tuple, Dict, List, Union, NoReturn
from uuid import UUID

from hexbytes import HexBytes
from toolz import pipe

from brambl.client.auto import AutoClient
from brambl.client.base import BaseClient
from brambl.datastructures import NamedElementOnion
from brambl.exceptions import BadResponseFormat
from brambl.middleware.attrdict import attrdict_middleware
from brambl.types import RPCResponse, Middleware, MiddlewareOnion, RPCEndpoint
from brambl.utils.threads import ThreadWithReturn

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401

NULL_RESPONSES = [None, HexBytes('0x'), '0x']


def apply_error_formatters(
        error_formatters: Callable[..., Any],
        response: RPCResponse,
) -> RPCResponse:
    if error_formatters:
        formatted_resp = pipe(response, error_formatters)
        return formatted_resp
    else:
        return response


def apply_null_result_formatters(
        null_result_formatters: Callable[..., Any],
        response: RPCResponse,
        params: Optional[Any] = None,
) -> RPCResponse:
    if null_result_formatters:
        formatted_resp = pipe(params, null_result_formatters)
        return formatted_resp
    else:
        return response


class RequestManager:
    logger = getLogger("brambl.RequestManager")

    def __init__(
            self,
            brambl: 'Brambl',
            client: Optional[BaseClient] = None,
            middlewares: Optional[Sequence[Tuple[Middleware, str]]] = None
    ) -> None:
        self.brambl = brambl
        self.pending_requests: Dict[UUID, ThreadWithReturn[RPCResponse]] = {}

        if middlewares is None:
            middlewares = self.default_middlewares(brambl)

        self.middleware_onion: MiddlewareOnion = NamedElementOnion(middlewares)

        if client is None:
            self.client = AutoClient()
        else:
            self.client = client

    brambl: 'Brambl' = None
    _client = None

    @property
    def client(self) -> BaseClient:
        return self._client

    @client.setter
    def client(self, client: BaseClient) -> None:
        self._client = client

    @staticmethod
    def default_middlewares(
            brambl: 'Brambl'
    ) -> List[Tuple[Middleware, str]]:
        """
        List the default middlewares for the request manager.
        Leaving ens unspecified will prevent the middleware from resolving names.
        """
        return [
            ##(pythonic_middleware, 'pythonic'),  #TODO Need to write the Pythonic Request and Result Formatters
            ##(validation_middleware, 'validation'),  #TODO Write validation middleware (for transactions primarily)
        ]

    #
    # Client requests and response
    #
    def _make_request(
            self, method: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
            params: Any
    ) -> RPCResponse:
        request_func = self.client.request_func(
            self.brambl,
            self.middleware_onion)
        self.logger.debug("Making request. Method: %s", method)
        return request_func(method, params)

    async def _coro_make_request(
            self, method: Union[RPCEndpoint, Callable[..., RPCEndpoint]], params: Any
    ) -> RPCResponse:
        # type ignored b/c request_func is an awaitable in async model
        request_func = await self.client.request_func(  # type: ignore
            self.brambl,
            self.middleware_onion)
        self.logger.debug("Making request. Method: %s", method)
        return await request_func(method, params)

    def formatted_response(
            self,
            response: RPCResponse,
            params: Any,
            error_formatters: Optional[Callable[..., Any]] = None,
            null_result_formatters: Optional[Callable[..., Any]] = None,
    ) -> Any:
        if "error" in response:
            apply_error_formatters(error_formatters, response)
            raise ValueError(response["error"])
        # NULL_RESPONSES includes None, so return False here as the default
        # so we don't apply the null_result_formatters if there is no 'result' key
        elif response.get('result', False) in NULL_RESPONSES:
            # null_result_formatters raise either a BlockNotFound
            # or a TransactionNotFound error, depending on the method called
            apply_null_result_formatters(null_result_formatters, response, params)
            return response['result']
        elif response.get('result') is not None:
            return response['result']
        else:
            raise BadResponseFormat(
                "The response was in an unexpected format and unable to be parsed. "
                f"The raw response is: {response}"
            )

    def request_blocking(
            self,
            method: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
            params: Any,
            error_formatters: Optional[Callable[..., Any]] = None,
            null_result_formatters: Optional[Callable[..., Any]] = None,
    ) -> Any:
        """
        Make a synchronous request using the client
        """
        response = self._make_request(method, params)
        return self.formatted_response(response,
                                       params,
                                       error_formatters,
                                       null_result_formatters)

    async def coro_request(
            self,
            method: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
            params: Any,
            error_formatters: Optional[Callable[..., Any]] = None,
            null_result_formatters: Optional[Callable[..., Any]] = None,
    ) -> Any:
        """
        Coroutine for making a request using the client
        """
        response = await self._coro_make_request(method, params)
        return self.formatted_response(response,
                                       params,
                                       error_formatters,
                                       null_result_formatters)

    def receive_blocking(self, request_id: UUID, timeout: Optional[float] = None) -> Any:
        raise NotImplementedError("Callback pattern not implemented. Here for future pub/sub expansion")

    def receive_async(self, request_id: UUID, *args: Any, **kwargs: Any) -> NoReturn:
        raise NotImplementedError("Callback pattern not implemented. Here for future pub/sub expansion")
