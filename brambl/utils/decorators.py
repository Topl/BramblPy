import functools
import itertools
from typing import Callable, TypeVar

from dotenv import Any

from brambl.types import is_text

T = TypeVar("T")

def _has_one_val(*args: T, **kwargs: T) -> bool:
    vals = itertools.chain(args, kwargs.values())
    not_nones = list(filter(lambda val: val is not None, vals))
    return len(not_nones) == 1

def _assert_one_val(*args: T, **kwargs: T) -> None:
    if not _has_one_val(*args, **kwargs):
        raise TypeError(
            "Exactly one of the passed values can be specified. "
            "Instead, values were: %r, %r" % (args, kwargs)
        )

def _base58str_or_text_kwarg_is_text_type(**kwargs: T) -> bool:
    value = kwargs["base58str"] if "base58str" in kwargs else kwargs["text"]
    return is_text(value)


def _assert_hexstr_or_text_kwarg_is_text_type(**kwargs: T) -> None:
    if not _base58str_or_text_kwarg_is_text_type(**kwargs):
        raise TypeError(
            "Arguments passed as base58str or text must be of text type. "
            "Instead, value was: %r" % (repr(next(iter(list(kwargs.values())))))
        )


def _validate_supported_kwarg(kwargs: Any) -> None:
    if next(iter(kwargs)) not in ["primitive", "hexstr", "text"]:
        raise TypeError(
            "Kwarg must be 'primitive', 'hexstr', or 'text'. "
            "Instead, kwarg was: %r" % (next(iter(kwargs)))
        )

def validate_conversion_arguments(to_wrap: Callable[..., T]) -> Callable[..., T]:
    """
    Validates arguments for conversion functions.
    - Only a single argument is present
    - Kwarg must be 'primitive' 'base58str' or 'text'
    - If it is 'hexstr' or 'text' that it is a text type
    """

    @functools.wraps(to_wrap)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        _assert_one_val(*args, **kwargs)
        if kwargs:
            _validate_supported_kwarg(kwargs)

        if len(args) == 0 and "primitive" not in kwargs:
            _assert_hexstr_or_text_kwarg_is_text_type(**kwargs)
        return to_wrap(*args, **kwargs)

    return wrapper