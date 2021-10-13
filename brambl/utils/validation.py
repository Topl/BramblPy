from base58 import b58decode


def validate_txId(txid):
    if (not isinstance(txid, str)):
        raise TypeError("TransactionId must be a str object")
    try: 
        decodedTxId = b58decode(txid)
        if (decodedTxId.__len__ != 33):
            raise ValueError(
                "TransactionId must be 33 bytes long after being decoded fromBase58, not" "'{}'".format(decodedTxId.__len__)
            )
    except ValueError as e:
        raise ValueError(
            "Transaction ID must be a Base58 encoded string, not "
            "'{}'".format(txid)
        )
    return txid