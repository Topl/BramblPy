from base58 import b58decode

from brambl.consts import TRANSACTION_ID_SIZE, TRANSACTION_MODIFIER_TYPE


def validate_txId(txid):
    if (not isinstance(txid, str)):
        raise TypeError("TransactionId must be a str object")
    try: 
        decodedTxId = b58decode(txid)
        if (len(decodedTxId) != TRANSACTION_ID_SIZE):
            raise ValueError(
                "TransactionId must be {:d} bytes long after being decoded fromBase58, not" "'{}'".format(TRANSACTION_ID_SIZE, len(decodedTxId))
            )
        elif (decodedTxId[0] != TRANSACTION_MODIFIER_TYPE):
            raise ValueError(
                "TransactionId has incorrect modifierType. The correct type is {}, not '{}'".format(TRANSACTION_MODIFIER_TYPE, decodedTxId[0])
            )
    except ValueError as e:
        raise ValueError(
            "Transaction ID must be a Base58 encoded string, not "
            "'{}'".format(txid)
        )
    return txid