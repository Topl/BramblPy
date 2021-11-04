import functools
from typing import TYPE_CHECKING, Sequence, Callable, Any

from brambl.types import Middleware, RPCEndpoint, RPCResponse

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401


def combine_middlewares(
    middlewares: Sequence[Middleware],
    brambl: 'Brambl',
    client_request_fn: Callable[[RPCEndpoint, Any], Any]
) -> Callable[..., RPCResponse]:
    """
    Returns a callable function which will call the client.client_request
    function wrapped with all of the middlewares.
    """
    return functools.reduce(
        lambda request_fn, middleware: middleware(request_fn, brambl),
        reversed(middlewares),
        client_request_fn,
    )