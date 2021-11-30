import logging
from typing import Any, Dict, Iterable, Optional, Tuple, Union
from brambl.client.base import JSONBaseClient
from brambl.datastructures import NamedElementOnion
from brambl.exception_retry_request import http_retry_request_middleware
from brambl.requests import get_default_http_endpoint, make_post_request
from brambl.types import URI, Middleware, RPCEndpoint, RPCResponse
from brambl.utils.functional import (
    to_dict
)
from brambl.utils.http import construct_user_agent


class HTTPClient(JSONBaseClient):
    logger = logging.getLogger("brambl.client.HTTPClient")
    endpoint_uri = None
    _request_args = None
    _request_kwargs = None
    _middlewares: Tuple[Middleware, ...] = NamedElementOnion([(http_retry_request_middleware, 'http_retry_request')])

    def __init__(
        self, endpoint_uri: Optional[Union[URI, str]] = None,
        request_kwargs: Optional[Any] = None
    ) -> None:
        if endpoint_uri is None:
            self.endpoint_uri = get_default_http_endpoint()
        else:
            self.endpoint_uri = URI(endpoint_uri)
        
        self._request_kwargs = request_kwargs or {}

        super().__init__()
    
    def __str__(self) -> str: 
        return "JSON-RPC Connection {0}".format(self.endpoint_uri)

    @to_dict
    def get_request_kwargs(self) -> Iterable[Tuple[str, Any]]:
        if 'headers' not in self._request_kwargs:
            yield 'headers', self.get_request_headers()
        for key, value in self._request_kwargs.items():
            yield key, value

    def get_request_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'User-Agent': construct_user_agent(str(type(self))),
        }
    
    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        request_data = self.encode_rpc_request(method, params)
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Method: %s, Response: %s",
                          self.endpoint_uri, method, response)
        return response
