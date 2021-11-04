from ast import Call
from telnetlib import RCP
from typing import Any, Callable, Collection, Type
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects
)
from brambl.types import RPCEndpoint, RPCResponse

whitelist = [
    "debug_delay",
    "debug_myBlocks",
    "debug_generators",
    "debug_idsFromHeight",
    "util_seed",
    "util_seedOfLength",
    "util_hashBlake2b256",
    "util_generateAssetCode",
    "util_checkValidAddress",
    "topl_head",
    "topl_balances",
    "topl_transactionById",
    "topl_blockById",
    "topl_blockByHeight",
    "topl_mempool",
    "topl_transactionFromMempool",
    "topl_info",
    "topl_rawAssetTransfer",
    "topl_rawArbitTransfer",
    "topl_rawPolyTransfer",
    "topl_broadcastTx",
    "admin_unlockKeyfile",
    "admin_lockKeyfile",
    "admin_generateKeyfile",
    "admin_importSeedPhrase",
    "admin_listOpenKeyfiles",
    "admin_startForging",
    "admin_stopForging",
    "admin_updateRewardsAddress",
    "admin_getRewardsAddress"
]

def check_if_retry_on_failure(method: RPCEndpoint) -> bool:
    root = method.split('_')[0]
    if root in whitelist:
        return True
    elif method in whitelist:
        return True
    else:
        return False

def exception_retry_middleware(
    make_request: Callable[[RPCEndpoint, Any], RPCResponse],
    brambl: "Brambl",
    errors: Collection[Type[BaseException]],
    retries: int = 3,
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPClient.
    """
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                except errors: 
                    if i < retries - 1:
                        continue
                    else:
                        raise
            return None
        else:
            return make_request(method, params)
    return middleware


def http_retry_request_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], brambl: "Brambl"
) -> Callable[[RPCEndpoint, Any], Any]: 
    return exception_retry_middleware(
        make_request,
        brambl,
        (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )

