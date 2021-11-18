from functools import wraps
from typing import Dict, Any

from brambl.client.rpc import HTTPClient
from brambl.typing.encoding import HexStr, Base58Str
from brambl.utils.conversions import to_bytes, Primitives, to_text, to_hex, to_int, to_base58
from brambl.utils.encoding import to_json
from brambl.manager import RequestManager as DefaultRequestManager

class Brambl:
    # Client
    HttpClient = HTTPClient

    # Request Manager
    RequestManager = DefaultRequestManager

    # Encoding and Decoding
    @staticmethod
    @wraps(to_bytes)
    def toBytes(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> bytes:
        return to_bytes(primitive, hexstr, text)

    @staticmethod
    @wraps(to_int)
    def toInt(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> int:
        return to_int(primitive, hexstr, text)

    @staticmethod
    @wraps(to_text)
    def toText(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> str:
        return to_text(primitive=primitive, hexstr=hexstr, text=text)

    @staticmethod
    @wraps(to_hex)
    def toHex(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> HexStr:
        return to_hex(primitive, hexstr, text)

    @staticmethod
    @wraps(to_base58)
    def toBase58(
            primitive: Primitives = None, base58str: Base58Str = None, text: str = None, hexstr: HexStr = None
    ) -> HexStr:
        return to_base58(primitive, base58str, text, hexstr)

    @staticmethod
    @wraps(to_json)
    def toJSON(obj: Dict[Any, Any]) -> str:
        return to_json(obj)
