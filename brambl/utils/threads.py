import threading
from typing import Generic, Callable, Any
from brambl.types import TReturn

"""
A minimal implementation of the various gevent APIs used within this codebase.
"""


class ThreadWithReturn(threading.Thread, Generic[TReturn]):
    def __init__(
            self, target: Callable[..., TReturn] = None, args: Any = None, kwargs: Any = None
    ) -> None:
        super().__init__(
            target=target,
            args=args or tuple(),
            kwargs=kwargs or {},
        )
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        self._return = self.target(*self.args, **self.kwargs)

    def get(self, timeout: float = None) -> TReturn:
        self.join(timeout)
        try:
            return self._return
        except AttributeError:
            raise RuntimeError("Something went wrong.  No `_return` property was set")
