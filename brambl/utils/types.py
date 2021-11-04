import collections
from typing import Any

bytes_types = (bytes, bytearray)
integer_types = (int,)
string_types = (bytes, str, bytearray)
text_types = str


def is_integer(value: Any) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


def is_list_like(obj: Any) -> bool:
    return not is_string(obj) and isinstance(obj, collections.abc.Sequence)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes_types)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, collections.Mapping)


def is_text(value: Any) -> bool:
    return isinstance(value, text_types)


def is_boolean(value: Any) -> bool:
    return isinstance(value, bool)
