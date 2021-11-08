import os
# Dependencies
from typing import Any, Union, Callable

import requests_cache
from hexbytes import HexBytes
from requests import Timeout
from toolz import assoc

from brambl.credentials.credential_manager import Ed25519CredentialManager
from brambl.ed25519.utils.address import Address, validateAddressByNetwork
from brambl.exceptions import TimeExhausted
from brambl.method import Method, default_root_munger
from brambl.module import Module
from brambl.types import URI, BlockIdentifier, AssetTxParams, ArbitTxParams, PolyTxParams, AssetRawTxParams, \
    ArbitRawTxParams, PolyRawTxParams, RPCResponse, ModifierId, BlockData, BlockNumber, Transaction
from brambl.utils.blocks import select_method_for_block_identifier
from brambl.utils.empty import Empty, empty
from brambl.utils.rpc_api import RPC
from brambl.utils.transactions import wait_for_transaction_receipt


class BaseBifrostRequest(Module):
    _default_address: Union[Address, Empty] = empty
    _default_block: BlockIdentifier = "latest"
    _default_network: str = "private"

    """ properties """

    @property
    def default_block(self) -> BlockIdentifier:
        return self._default_block

    @default_block.setter
    def default_block(self, value: BlockIdentifier) -> None:
        self._default_block = value

    @property
    def default_address(self) -> Union[Address, Empty]:
        return self._default_address

    def send_raw_transaction_munger(self, transaction: Union[AssetTxParams, ArbitTxParams, PolyTxParams]) \
            -> Union[AssetTxParams, ArbitTxParams, PolyTxParams]:
        if 'sender' not in transaction and validateAddressByNetwork(self._default_network, str(self.default_address)):
            transaction = assoc(transaction, 'sender', self.default_address)

        return transaction

    _send_transaction: Method[Callable[[Union[PolyTxParams, ArbitTxParams, AssetTxParams]], RPCResponse]] = Method(
        RPC.topl_broadcastTx,
        mungers=[send_raw_transaction_munger]
    )

    _send_raw_poly_transaction: Method[Callable[[PolyRawTxParams], RPCResponse]] = Method(
        RPC.topl_rawPolyTransfer,
        mungers=[default_root_munger],
    )

    _send_raw_arbit_transaction: Method[Callable[[ArbitRawTxParams], RPCResponse]] = Method(
        RPC.topl_rawArbitTransfer,
        mungers=[default_root_munger],
    )

    _send_raw_asset_transaction: Method[Callable[[AssetRawTxParams], RPCResponse]] = Method(
        RPC.topl_rawAssetTransfer,
        mungers=[default_root_munger],
    )

    _get_transaction: Method[Callable[[ModifierId], Transaction]] = Method(
        RPC.topl_transactionById,
        mungers=[default_root_munger]
    )

    _get_pending_transaction: Method[Callable[[ModifierId], RPCResponse]] = Method(
        RPC.topl_transactionFromMempool,
        mungers=[default_root_munger]
    )

    """
        `topl_blockById`
        `topl_blockByHeight`
        `topl_head`
    """

    _get_block: Method[Callable[..., BlockData]] = Method(
        method_choice_depends_on_args=select_method_for_block_identifier(
            if_predefined=RPC.topl_head,
            if_id=RPC.topl_blockById,
            if_number=RPC.topl_blockByHeight,
        ),
        mungers=[default_root_munger],
    )

    get_block_number: Method[Callable[[], BlockNumber]] = Method(
        RPC.topl_head,
        mungers=None,
    )


class BifrostRequest(BaseBifrostRequest, Module):
    credentialManager = Ed25519CredentialManager()

    _node_info: Method[Callable[[], str]] = Method(
        RPC.topl_info,
        mungers=None,
    )

    @property
    def node_info(self) -> str:
        return self._node_info

    get_delay: Method[Callable[[], int]] = Method(
        RPC.debug_delay,
        mungers=None,
    )

    @property
    def delay(self) -> int:
        return self.get_delay()

    @property
    def block_number(self) -> BlockNumber:
        return self.get_block_number()

    """ property default_address """

    @property
    def default_address(self) -> Union[Address, Empty]:
        return self._default_address

    @default_address.setter
    def default_address(self, address: Union[Address, Empty]) -> None:
        self._default_address = address

    def get_block(
            self, block_identifier: BlockIdentifier
    ) -> BlockData:
        return self._get_block(block_identifier)

    def get_transaction(self, transaction_id: ModifierId) -> Transaction:
        return self._get_transaction(transaction_id)

    def get_pending_transaction(self, transaction_id: ModifierId) -> RPCResponse:
        return self._get_pending_transaction(transaction_id)

    def wait_for_transaction_receipt(
            self, transaction_hash: ModifierId, timeout: int = 120, poll_latency: float = 0.1
    ) -> Transaction:
        try:
            return wait_for_transaction_receipt(self.web3, transaction_hash, timeout, poll_latency)
        except Timeout:
            raise TimeExhausted(
                "Transaction {!r} is not in the chain, after {} seconds".format(
                    HexBytes(transaction_hash),
                    timeout,
                )
            )

    def send_transaction(self, transaction: Union[PolyTxParams, ArbitTxParams, AssetTxParams]) -> HexBytes:
        return self._send_transaction(transaction)

    def send_raw_poly_transaction(self, transaction: PolyRawTxParams) -> RPCResponse:
        return self._send_raw_poly_transaction(transaction)

    def send_raw_asset_transaction(self, transaction: AssetRawTxParams) -> RPCResponse:
        return self._send_raw_asset_transaction(transaction)

    def send_raw_arbit_transaction(self, transaction: ArbitRawTxParams) -> RPCResponse:
        return self._send_raw_arbit_transaction(transaction)


def get_default_http_endpoint() -> URI:
    return URI(os.environ.get('BRAMBL_HTTP_CLIENT_URI', 'http://localhost:9085'))


def _get_session() -> requests_cache.CachedSession:
    return requests_cache.CachedSession('request_cache')


def make_post_request(endpoint_uri: URI, data: str, *args: Any, **kwargs: Any) -> bytes:
    kwargs.setdefault('timeout', 10)
    session = _get_session()
    # https://github.com/python/mypy/issues/2582
    response = session.post(endpoint_uri, data=data, *args, **kwargs)  # type: ignore
    response.raise_for_status()

    return response.content
