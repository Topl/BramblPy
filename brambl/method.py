import warnings
from typing import Generic, TypeVar, Callable, Any, Optional, Union, Type

from brambl.types import RPCEndpoint

TFunc = TypeVar('TFunc', bound=Callable[..., Any])


class Method(Generic[TFunc]):
    """Method object for Bifrost client methods

    Calls to the Method go through these steps:

    1. method selection - The json_rpc_method argument can be method string or a
    function that returns a method string. If a callable is provided the processed
    method inputs are passed to the method selection function, and the returned
    method string is used.
"""

    def __init__(self,
                 json_rpc_method: Optional[RPCEndpoint] = None
                 ):
        self.json_rpc_method = json_rpc_method

    def __get__(self, obj: Optional["Module"] = None,
                obj_type: Optional[Type["Module"]] = None) -> TFunc:
        if obj is None:
            raise TypeError(
                "Direct calls to methods are not supported. "
                "Methods must be called from an module instance, "
                "usually attached to a brambl instance.")
        return obj.retrieve_caller_fn(self)

    @property
    def method_selector_fn(self) -> Callable[..., Union[RPCEndpoint, Callable[..., RPCEndpoint]]]:
        """Gets the method selector from the config.
        """
        if callable(self.json_rpc_method):
            return self.json_rpc_method
        elif isinstance(self.json_rpc_method, (str,)):
            return lambda *_: self.json_rpc_method
        raise ValueError("``json_rpc_method`` config invalid.  May be a string or function")

    def process_params(
            self
    ) -> Callable[..., Union[RPCEndpoint, Callable[..., RPCEndpoint]]]:
        return self.method_selector_fn()


class DeprecatedMethod(object):
    """
        Method object for deprecated Bifrost methods. As we continue to build out Bifrost, methods will become deprecated
        so BramblPy anticipates that eventuality with this class.
    """
    def __init__(self, method: Method[Callable[..., Any]], old_name: str, new_name: str) -> None:
        self.method = method
        self.old_name = old_name
        self.new_name = new_name

    def __get__(self, obj: Optional["Module"] = None,
                obj_type: Optional[Type["Module"]] = None) -> Any:
        warnings.warn(
            "{self.old_name} is deprecated in favor of {self.new_name}",
            category=DeprecationWarning,
        )
        return self.method.__get__(obj, obj_type)
