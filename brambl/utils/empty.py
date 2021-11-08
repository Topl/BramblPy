from typing import Literal


class Empty:
    def __bool__(self) -> Literal[False]:
        return False

    def __nonzero__(self) -> Literal[False]:
        return False


empty = Empty()
