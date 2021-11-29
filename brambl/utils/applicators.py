from typing import Callable, Any, List, Generator

from brambl.utils.decorators import return_arg_type


@return_arg_type(2)
def apply_formatter_at_index(
        formatter: Callable[..., Any], at_index: int, value: List[Any]
) -> Generator[List[Any], None, None]:
    if at_index + 1 > len(value):
        raise IndexError(
            "Not enough values in iterable to apply formatter.  Got: {0}. "
            "Need: {1}".format(len(value), at_index + 1)
        )
    for index, item in enumerate(value):
        if index == at_index:
            yield formatter(item)
        else:
            yield item