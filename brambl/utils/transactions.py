from requests import Timeout

from brambl.exceptions import TransactionNotFound
from brambl.types import ModifierId, Transaction


def wait_for_transaction_receipt(
        brambl: "Brambl", txn_id: ModifierId, timeout: float, poll_latency: float
) -> Transaction:
    with Timeout(timeout) as _timeout:
        while True:
            try:
                txn_receipt = brambl.eth.get_transaction_receipt(txn_id)
            except TransactionNotFound:
                txn_receipt = None
            if txn_receipt is not None:
                break
            _timeout.sleep(poll_latency)
    return txn_receipt
