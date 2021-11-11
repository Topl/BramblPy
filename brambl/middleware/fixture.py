from typing import Dict, Any, Callable, TYPE_CHECKING

from brambl.types import RPCEndpoint, Middleware, RPCResponse

if TYPE_CHECKING:
    from brambl.Brambl import Brambl


def construct_result_generator_middleware(
        result_generators: Dict[RPCEndpoint, Any]
) -> Middleware:
    """
    Constructs a middleware which intercepts requests for any method found in
    the provided mapping of endpoints to generator functions, returning
    whatever response the generator function returns.  Callbacks must be
    functions with the signature `fn(method, params)`.
    """

    def result_generator_middleware(
            make_request: Callable[[RPCEndpoint, Any], Any], brambl: "Brambl"
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method in result_generators:
                result = result_generators[method](method, params)
                return {'result': result}
            else:
                return make_request(method, params)

        return middleware

    return result_generator_middleware
