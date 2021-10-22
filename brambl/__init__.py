import functools
from typing import Any, Callable, Sequence

import pkg_resources
from brambl.Brambl import Brambl

from brambl.types import Middleware, RPCEndpoint, RPCResponse


def combine_middlewares(
    middlewares: Sequence[Middleware],
    brambl: 'Brambl',
    client_request_fn: Callable[[RPCEndpoint, Any], Any]
) -> Callable[..., RPCResponse]:
    """
    Returns a callable function which will call the provider.provider_request
    function wrapped with all of the middlewares.
    """
    return functools.reduce(
        lambda request_fn, middleware: middleware(request_fn, brambl),
        reversed(middlewares),
        client_request_fn,
    )

__version__ = pkg_resources.get_distribution("brambl").version