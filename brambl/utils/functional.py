import functools
from collections import Iterable, Mapping
from typing import Callable, TypeVar, Union, Tuple, Dict

T = TypeVar("T")


def apply_to_return_value(
        callback: Callable[..., T]
) -> Callable[..., Callable[..., T]]:
    def outer(fn: Callable[..., T]) -> Callable[..., T]:
        # We would need to type annotate *args and **kwargs but doing so segfaults
        # the PyPy builds. We ignore instead.
        @functools.wraps(fn)
        def inner(*args, **kwargs) -> T:  # type: ignore
            return callback(fn(*args, **kwargs))

        return inner

    return outer


TVal = TypeVar("TVal")
TKey = TypeVar("TKey")

to_dict = apply_to_return_value(
    dict
)
# type: Callable[[Callable[..., Iterable[Union[Mapping[TKey, TVal], Tuple[TKey, TVal]]]]], Callable[..., Dict[TKey, TVal]]]
