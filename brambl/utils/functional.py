import functools
from typing import Callable, TypeVar

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

to_dict = apply_to_return_value(
    dict
)