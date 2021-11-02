from brambl.utils.conversions import text_if_str as non_curried_text_if_str

from toolz import curry

text_if_str = curry(non_curried_text_if_str)

# Delete any methods and classes that are not intended to be importable from
#   brambl.utils.curried
# We do this approach instead of __all__ because this approach actually prevents
#   importing the wrong thing, while __all__ only affects `from brambl.utils.curried import *`

del non_curried_text_if_str