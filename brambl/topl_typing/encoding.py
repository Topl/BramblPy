from typing import NewType, Union

Base58Str = NewType('Base58Str', str)
HexStr = NewType('HexStr', str)
Primitives = Union[bytes, int, bool]