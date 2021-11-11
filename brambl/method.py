import functools
import warnings
from typing import Generic, TypeVar, Callable, Any, Optional, Union, Type, Sequence, Tuple, List, TYPE_CHECKING, Dict

from toolz import pipe

from brambl.types import RPCEndpoint, TReturn
from brambl.utils.functional import to_tuple
from brambl.utils.method_formatters import get_request_formatters

TFunc = TypeVar('TFunc', bound=Callable[..., Any])

Munger = Callable[..., Any]

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401
    from brambl.module import Module  # noqa: F401


@to_tuple
def _apply_request_formatters(
        params: Any, request_formatters: Dict[RPCEndpoint, Callable[..., TReturn]]
) -> Tuple[Any, ...]:
    if request_formatters:
        formatted_params = pipe(params, request_formatters)
        return formatted_params
    return params


def _munger_star_apply(fn: Callable[..., TReturn]) -> Callable[..., TReturn]:
    @functools.wraps(fn)
    def inner(args: Any) -> TReturn:
        return fn(*args)

    return inner


def default_munger(module: "Module", *args: Any, **kwargs: Any) -> Tuple[()]:
    if args is not None and kwargs is not None:
        return ()
    else:
        raise TypeError("Parameters passed to method without parameter "
                        "mungers defined.")


def default_root_munger(module: "Module", *args: Any) -> List[Any]:
    return [*args]


def return_args_directly(module: "Module", *args: Any) -> Any:
    return [*args][0]


class Method(Generic[TFunc]):
    """Method object for Bifrost client methods

    1. input munging - includes normalization, parameter checking, early parameter
    formatting.  Any processing on the input parameters that need to happen before
    json_rpc method string selection occurs.

            A note about mungers: The first (root) munger should reflect the desired
        api function arguments. In other words, if the api function wants to
        behave as: `get_balance(address)`, the root munger
        should accept these same arguments, with the addition of the module as
        the first argument e.g.:

        ```
        def get_balance_root_munger(module, address):
            return module, address
        ```

        all mungers should return an argument list.

        if no munger is provided, a default munger expecting no method arguments
        will be used.

    2. method selection - The json_rpc_method argument can be method string or a
    function that returns a method string. If a callable is provided the processed
    method inputs are passed to the method selection function, and the returned
    method string is used.

    3. request formatters are set - formatters are retrieved
    using the json rpc method string.

    4. After the parameter processing from steps 1-2 the request is made using
    the calling function returned by the module attribute ``retrieve_caller_fn``
    and the response formatters are applied to the output.
"""

    def __init__(self,
                 json_rpc_method: Optional[RPCEndpoint] = None,
                 mungers: Optional[Sequence[Munger]] = None,
                 request_formatters: Optional[Callable[..., TReturn]] = None,
                 method_choice_depends_on_args:
                 Optional[Callable[..., RPCEndpoint]] = None,
                 ):
        self.json_rpc_method = json_rpc_method
        self.mungers = mungers or [default_munger]
        self.request_formatters = request_formatters or get_request_formatters
        self.method_choice_depends_on_args = method_choice_depends_on_args

    def __get__(self, obj: Optional["Module"] = None,
                obj_type: Optional[Type["Module"]] = None) -> TFunc:
        if obj is None:
            raise TypeError(
                "Direct calls to methods are not supported. "
                "Methods must be called from an module instance, "
                "usually attached to a brambl instance.")
        return obj.retrieve_caller_fn(self)

    def input_munger(
            self, module: "Module", args: Any, kwargs: Any
    ) -> List[Any]:
        # This function takes the "root_munger" - (the first munger in
        # the list of mungers) and then pipes the return value of the
        # previous munger as an argument to the next munger to return
        # an array of arguments that have been formatted.
        # See the test_process_params test
        # in tests/core/method-class/test_method.py for an example
        # with multiple mungers.
        # TODO: Create friendly error output.
        mungers_iter = iter(self.mungers)
        root_munger = next(mungers_iter)
        munged_inputs = pipe(
            root_munger(module, *args, **kwargs),
            *map(lambda m: _munger_star_apply(functools.partial(m, module)), mungers_iter))

        return munged_inputs

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
            self, module: "Module", *args: Any, **kwargs: Any
    ) -> Tuple[Union[RPCEndpoint, Callable[..., RPCEndpoint]], Tuple[Any, ...]]:
        params = self.input_munger(module, args, kwargs)

        if self.method_choice_depends_on_args:
            # If the method choice depends on the args that get passed in,
            # the first parameter determines which method needs to be called
            self.json_rpc_method = self.method_choice_depends_on_args(value=params[0])

        method = self.method_selector_fn()
        request = (method,
                   _apply_request_formatters(params, self.request_formatters(method)))
        return request


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
