from typing import Any

bytes_types = (bytes, bytearray)
string_types = (bytes, str, bytearray)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)
