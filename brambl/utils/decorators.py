import functools
import itertools

from typing import Callable, Any, Type, TypeVar

from brambl.utils.types import is_text

T = TypeVar("T")


def return_arg_type(at_position: int) -> Callable[..., Callable[..., T]]:
    """
    Wrap the return value with the result of `type(args[at_position])`.
    """

    def decorator(to_wrap: Callable[..., Any]) -> Callable[..., T]:
        @functools.wraps(to_wrap)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            result = to_wrap(*args, **kwargs)
            ReturnType = type(args[at_position])
            return ReturnType(result)  # type: ignore

        return wrapper

    return decorator


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


def _hexstr_or_base58_or_text_kwarg_is_text_type(**kwargs: T) -> bool:
    value = kwargs["hexstr"] if "hexstr" in kwargs else kwargs["text"] if "text" in kwargs else kwargs['base58str']
    return is_text(value)


def _assert_hexstr_or_base58_or_text_kwarg_is_text_type(**kwargs: T) -> None:
    if not _hexstr_or_base58_or_text_kwarg_is_text_type(**kwargs):
        raise TypeError(
            "Arguments passed as hexstr or text must be of text type. "
            "Instead, value was: %r" % (repr(next(iter(list(kwargs.values())))))
        )


def _validate_supported_kwarg(kwargs: Any) -> None:
    if next(iter(kwargs)) not in ["primitive", "hexstr", "text", "base58str"]:
        raise TypeError(
            "Kwarg must be 'primitive', 'hexstr', 'base58str', or 'text'. "
            "Instead, kwarg was: %r" % (next(iter(kwargs)))
        )


def validate_conversion_arguments(to_wrap: Callable[..., T]) -> Callable[..., T]:
    """
    Validates arguments for conversion functions.
    - Only a single argument is present
    - Kwarg must be 'primitive' 'base58str' 'hexstr' or 'text'
    - If it is 'base58str' 'hexstr' or 'text' that it is a text type
    """

    @functools.wraps(to_wrap)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        _assert_one_val(*args, **kwargs)
        if kwargs:
            _validate_supported_kwarg(kwargs)

        if len(args) == 0 and "primitive" not in kwargs:
            _assert_hexstr_or_base58_or_text_kwarg_is_text_type(**kwargs)
        return to_wrap(*args, **kwargs)

    return wrapper


class combomethod(object):
    def __init__(self, method: Callable[..., Any]) -> None:
        self.method = method

    def __get__(self, obj: T = None, objtype: Type[T] = None) -> Callable[..., Any]:
        @functools.wraps(self.method)
        def _wrapper(*args: Any, **kwargs: Any) -> Any:
            if obj is not None:
                return self.method(obj, *args, **kwargs)
            else:
                return self.method(objtype, *args, **kwargs)

        return _wrapper
