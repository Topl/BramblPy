from typing import Callable, Any, List, Generator

from brambl.utils.decorators import return_arg_type


@return_arg_type(2)
def apply_formatter_to_dict(
        formatter: Callable[..., Any], value: List[Any]
) -> Generator[List[Any], None, None]:
    return formatter(value)
