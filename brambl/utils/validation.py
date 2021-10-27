from typing import Any

from base58 import b58decode

from brambl.consts import TRANSACTION_ID_SIZE, TRANSACTION_MODIFIER_TYPE
from brambl.utils.exceptions import ValidationError
from brambl.utils.types import is_bytes


def validate_tx_id(txid: Any) -> str:
    if not isinstance(txid, str):
        raise TypeError("TransactionId must be a str object")
    try:
        decoded_tx_id = b58decode(txid)
        if len(decoded_tx_id) != TRANSACTION_ID_SIZE:
            raise ValueError(
                "TransactionId must be {:d} bytes long after being decoded fromBase58, not" "'{}'".format(
                    TRANSACTION_ID_SIZE, len(decoded_tx_id))
            )
        elif decoded_tx_id[0] != TRANSACTION_MODIFIER_TYPE:
            raise ValueError(
                "TransactionId has incorrect modifierType. The correct type is {}, not '{}'".format(
                    TRANSACTION_MODIFIER_TYPE, decoded_tx_id[0])
            )
    except ValueError as e:
        raise ValueError(
            "Transaction ID must be a Base58 encoded string, not "
            "'{}'".format(txid)
        )
    return txid


def validate_bytes(value: Any) -> None:
    if not is_bytes(value):
        raise ValidationError("Value must be a byte string.  Got: {0}".format(type(value)))


def validate_bytes_length(value: bytes, expected_length: int, name: str) -> None:
    actual_length = len(value)
    if actual_length != expected_length:
        raise ValidationError(
            "Unexpected {name} length: Expected {expected_length}, but got {actual_length} "
            "bytes".format(
                name=name,
                expected_length=expected_length,
                actual_length=actual_length,
            )
        )


def validate_uncompressed_public_key_bytes(value: Any) -> None:
    validate_bytes(value)
    validate_bytes_length(value, 32, "uncompressed public key")


def validate_private_key_bytes(value: Any) -> None:
    validate_bytes(value)
    validate_bytes_length(value, 64, "private key")


def validate_message_hash(value: Any) -> None:
    validate_bytes(value)
