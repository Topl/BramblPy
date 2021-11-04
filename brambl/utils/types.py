import collections
from typing import Any

bytes_types = (bytes, bytearray)
string_types = (bytes, str, bytearray)
text_types = str


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, collections.Mapping)


def is_text(value: Any) -> bool:
    return isinstance(value, text_types)
