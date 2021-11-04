from typing import Optional, Sequence, Union, Callable, Type, Any

from brambl.client.base import BaseClient
from brambl.client.rpc import HTTPClient
from brambl.exceptions import CannotHandleRequest
from brambl.types import RPCEndpoint, RPCResponse


class AutoClient(BaseClient):
    default_clients = (
        HTTPClient
    )
    _active_client = None

    def __init__(
            self,
            potential_clients: Optional[Sequence[Union[Callable[..., BaseClient],
                                                       Type[BaseClient]]]] = None
    ) -> None:
        """
        :param iterable potential_clients: ordered series of client classes to attempt with

        AutoClient will initialize each potential client (without arguments),
        in an attempt to find an active node. The list will default to
        :attribute:`default_clients`.
        """
        if potential_clients:
            self._potential_clients = potential_clients
        else:
            self._potential_clients = self.default_clients

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        try:
            return self._proxy_request(method, params)
        except IOError:
            return self._proxy_request(method, params, use_cache=False)

    def isConnected(self) -> bool:
        client = self._get_active_client(use_cache=True)
        return client is not None and client.isConnected()

    def _proxy_request(self, method: RPCEndpoint, params: Any,
                       use_cache: bool = True) -> RPCResponse:
        client = self._get_active_client(use_cache)
        if client is None:
            raise CannotHandleRequest(
                "Could not discover client while making request: "
                "method:{0}\n"
                "params:{1}\n".format(
                    method,
                    params))

        return client.make_request(method, params)

    def _get_active_client(self, use_cache: bool) -> Optional[BaseClient]:
        if use_cache and self._active_client is not None:
            return self._active_client

        for Client in self._potential_clients:
            client = Client()
            if client is not None and client.isConnected():
                self._active_client = client
                return client

        return None
