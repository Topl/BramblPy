from typing import overload, Dict, Any, Callable

from brambl.types import TReturn
from brambl.utils.conversions import text_if_str as non_curried_text_if_str
from brambl.utils.applicators import (
    apply_formatter_at_index,
    apply_formatters_to_dict as non_curried_apply_formatters_to_dict
)

from toolz import curry


@overload
def apply_formatters_to_dict(
        formatters: Dict[Any, Any]
) -> Callable[[Dict[Any, Any]], TReturn]:
    ...


@overload
def apply_formatters_to_dict(
        formatters: Dict[Any, Any], value: Dict[Any, Any]
) -> TReturn:
    ...


apply_formatter_at_index = curry(apply_formatter_at_index)
apply_formatters_to_dict = curry(non_curried_apply_formatters_to_dict)
text_if_str = curry(non_curried_text_if_str)

# Delete any methods and classes that are not intended to be importable from
#   brambl.utils.curried
# We do this approach instead of __all__ because this approach actually prevents
#   importing the wrong thing, while __all__ only affects `from brambl.utils.curried import *`

del non_curried_text_if_str
del non_curried_apply_formatters_to_dict
