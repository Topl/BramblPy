from typing import Callable, Dict, Any, Collection, Iterable, Union

from toolz import compose

from brambl.types import RPCEndpoint, TReturn
from brambl.utils.curried import apply_formatter_to_dict
from brambl.utils.formatters import remove_key_if
from brambl.utils.functional import to_tuple
from brambl.utils.rpc_api import RPC
from brambl.utils.validation import validate_addresses, validate_addresses_nested, validate_address

raw_poly_transaction_param_formatter = compose(
    remove_key_if('network_prefix', lambda txn: txn['network_prefix'] not in {"", b"", None}),
    remove_key_if('recipients', lambda txn: txn['recipients'] in [[], None]
                                            or not validate_addresses_nested(txn['recipients'], txn['network_prefix'])),
    remove_key_if('sender', lambda txn: txn['sender'] in [[], None]
                                        or not validate_addresses(txn['sender'], txn['network_prefix'])),
    remove_key_if('changeAddress', lambda txn: txn['changeAddress'] in {'', b'', None}
                                               or not validate_address(txn['changeAddress'], txn['network_prefix'])),
    remove_key_if('fee', lambda txn: txn['fee'] in {'', b'', None}),
)

PYTHONIC_REQUEST_FORMATTERS = {
    # Topl
    RPC.topl_rawPolyTransfer: apply_formatter_to_dict(raw_poly_transaction_param_formatter)
}


@to_tuple
def combine_formatters(
        formatter_maps: Collection[Dict[RPCEndpoint, Callable[..., TReturn]]], method_name: RPCEndpoint
) -> Iterable[Callable[..., TReturn]]:
    for formatter_map in formatter_maps:
        if method_name in formatter_map:
            yield formatter_map[method_name]


def get_request_formatters(
        method_name: Union[RPCEndpoint, Callable[..., RPCEndpoint]],
) -> Dict[str, Callable[..., Any]]:
    request_formatter_maps = (
        PYTHONIC_REQUEST_FORMATTERS,
    )
    formatters = combine_formatters(request_formatter_maps, method_name)
    return compose(*formatters)
