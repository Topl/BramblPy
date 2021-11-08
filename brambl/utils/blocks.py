from typing import Any

from toolz import curry

from brambl.base58 import isBase58
from brambl.types import RPCEndpoint
from brambl.utils.types import is_text, is_bytes, is_integer, is_string


def is_predefined_block_number(value: Any) -> bool:
    if is_text(value):
        value_text = value
    elif is_bytes(value):
        # `value` could either be random bytes or the utf-8 encoding of
        # one of the words in: {"latest", "pending", "earliest"}
        # We cannot decode the bytes as utf8, because random bytes likely won't be valid.
        # So we speculatively decode as 'latin-1', which cannot fail.
        value_text = value.decode('latin-1')
    elif is_integer(value):
        return False
    else:
        raise TypeError("unrecognized block reference: %r" % value)

    return value_text in {"latest", "head"}


def is_base58_encoded_block_id(value: Any) -> bool:
    if not is_string(value):
        return False
    return isBase58(value)


def is_hex_encoded_block_number(value: Any) -> bool:
    if not is_string(value):
        return False
    elif is_base58_encoded_block_id(value):
        return False
    try:
        value_as_int = int(value, 16)
    except ValueError:
        return False
    return 0 <= value_as_int < 2 ** 128


@curry
def select_method_for_block_identifier(
        value: Any, if_id: RPCEndpoint, if_number: RPCEndpoint, if_predefined: RPCEndpoint
) -> RPCEndpoint:
    if is_predefined_block_number(value):
        return if_predefined
    elif isinstance(value, bytes):
        return if_id
    elif is_base58_encoded_block_id(value):
        return if_id
    elif is_integer(value) and (0 <= value < 2 ** 128):
        return if_number
    elif is_hex_encoded_block_number(value):
        return if_number
    else:
        raise ValueError(
            "Value did not match any of the recognized block identifiers: {0}".format(value)
        )
