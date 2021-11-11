from typing import TYPE_CHECKING, cast

import pytest

from brambl.credentials.local import LocalCredential
from brambl.ed25519.utils.address import Address
from brambl.exceptions import InvalidAddress
from brambl.types import PolyRawTxParams, Poly
from brambl.typing.encoding import Base58Str

from brambl.utils.types import is_dict, is_integer, is_list_like

if TYPE_CHECKING:
    from brambl import Brambl


def test_brambl_topl_info(brambl: "Brambl") -> None:
    with pytest.warns(DeprecationWarning,
                      match="This mbramblod has been deprecated in some clients"):
        topl_info = brambl.requests.node_info

    assert is_dict(topl_info)


def test_brambl_current_block(brambl: "Brambl") -> None:
    current_block = brambl.requests.current_block
    assert is_dict(current_block)
    assert int(current_block['height']) >= 0


def test_brambl_get_current_block(brambl: "Brambl") -> None:
    current_block = brambl.requests.get_current_block({})
    assert is_dict(current_block)
    assert int(current_block['height']) >= 0


def test_brambl_get_balance(default_address, brambl: "Brambl") -> None:
    balance = brambl.requests.get_balance({'addresses': [str(default_address.address)]})

    assert is_dict(balance)
    assert int(balance[str(default_address.address)]['Balances']['Polys']) >= 0
    assert int(balance[str(default_address.address)]['Balances']['Arbits']) >= 0
    assert is_list_like(balance[str(default_address.address)]['Boxes']['AssetBox'])


def test_brambl_send_transaction_addr_checksum_required(brambl: "Brambl", default_address: LocalCredential
                                                        ) -> None:
    non_checksum_addr = str(default_address.address)[:-1] + "1"
    txn_params: PolyRawTxParams = {
        'sender': [str(default_address.address)],
        'recipients': [[str(default_address.address), Poly("0")]],
        "propositionType": "PublicKeyEd25519",
        "boxSelectionAlgorithm": "All",
        "changeAddress": str(default_address.address)
    }

    with pytest.raises(InvalidAddress):
        invalid_params = cast(PolyRawTxParams, dict(txn_params, **{'sender': [non_checksum_addr]}))
        brambl.requests.send_raw_poly_transaction(invalid_params)

    with pytest.raises(InvalidAddress):
        invalid_params = cast(PolyRawTxParams, dict(txn_params, **{'recipients': [[non_checksum_addr, Poly("0")]]}))
        brambl.requests.send_raw_poly_transaction(invalid_params)
