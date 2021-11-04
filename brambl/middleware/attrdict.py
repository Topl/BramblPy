from typing import Callable, Any, TYPE_CHECKING

from toolz import assoc

from brambl.datastructures import AttributeDict
from brambl.types import RPCEndpoint, RPCResponse, is_dict

if TYPE_CHECKING:
    from brambl import Brambl


def attrdict_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], brambl: "Brambl"
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Converts any result which is a dictionary into an a
    """

    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        response = make_request(method, params)

        if 'result' in response:
            result = response['result']
            if is_dict(result) and not isinstance(result, AttributeDict):
                return assoc(response, 'result', AttributeDict.recursive(result))
            else:
                return response
        else:
            return response

    return middleware
