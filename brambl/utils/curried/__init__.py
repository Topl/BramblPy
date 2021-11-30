from toolz import curry

from brambl.utils.applicators import (
    apply_formatter_to_dict as non_curried_apply_formatter_to_dict
)
from brambl.utils.conversions import text_if_str as non_curried_text_if_str

apply_formatter_to_dict = curry(non_curried_apply_formatter_to_dict)
text_if_str = curry(non_curried_text_if_str)

# Delete any methods and classes that are not intended to be importable from
#   brambl.utils.curried
# We do this approach instead of __all__ because this approach actually prevents
#   importing the wrong thing, while __all__ only affects `from brambl.utils.curried import *`

del non_curried_text_if_str
