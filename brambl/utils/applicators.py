from typing import Callable, Any, List, Generator, Dict, Tuple

from brambl.utils.functional import to_dict

from brambl.utils.decorators import return_arg_type


@to_dict
def apply_formatters_to_dict(
        formatters: Dict[Any, Any], value: Dict[Any, Any]
) -> Generator[Tuple[Any, Any], None, None]:
    for key, item in value.items():
        if key in formatters:
            try:
                yield key, formatters[key](item)
            except ValueError as exc:
                new_error_message = "Could not format invalid value %r as field %r" % (
                    item,
                    key,
                )
                raise ValueError(new_error_message) from exc
            except TypeError as exc:
                new_error_message = (
                        "Could not format invalid type of %r for field %r" % (item, key)
                )
                raise TypeError(new_error_message) from exc
        else:
            yield key, item


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
