from typing import Callable, Any, TYPE_CHECKING

from brambl.utils.types import is_dict
from toolz import assoc

from brambl.datastructures import AttributeDict
from brambl.types import RPCEndpoint, RPCResponse

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
                if 'rawTx' in result:
                    rawTx = result['rawTx']
                    result = assoc(
                        result, 'rawTx', AttributeDict.recursive(rawTx))
                if 'messageToSign' in result:
                    messageToSign = result['messageToSign']
                    result = assoc(
                        result, 'messageToSign', str(messageToSign)
                    )
                return result
            else:
                return response
        else:
            return response

    return middleware
