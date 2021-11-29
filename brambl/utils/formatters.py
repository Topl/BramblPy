from typing import Callable, Dict, Any

from toolz import curry, dissoc


@curry
def remove_key_if(
    key: Any, remove_if: Callable[[Dict[Any, Any]], bool], input_dict: Dict[Any, Any]
) -> Dict[Any, Any]:
    if key in input_dict and remove_if(input_dict):
        return dissoc(input_dict, key)
    else:
        return input_dict