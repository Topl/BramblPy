from typing import Any, Callable, Literal, NewType, Optional, TypedDict, Union, TypeVar, TYPE_CHECKING, Tuple, Sequence

from brambl.datastructures import NamedElementOnion
from brambl.ed25519.utils.address import Address
from brambl.typing.encoding import Base58Str, HexStr

TReturn = TypeVar("TReturn")
RPCEndpoint = NewType("RPCEndpoint", str)

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401

Poly = NewType('Poly', int)
Arbit = NewType('Arbit', int)
SecurityRoot = NewType("SecurityRoot", bytes)
ModifierId = NewType("ModiferId", str)
BoxId = NewType("BoxId", str)
Evidence = NewType("Evidence", str)
Proposition = NewType("Proposition", str)
Proof = NewType("Proof", str)
Digest32 = NewType("Digest32", str)
Version = NewType("Version", int)


class RPCError(TypedDict):
    code: int
    message: str
    data: Optional[str]


class RPCResponse(TypedDict, total=False):
    error: Union[RPCError]
    id: int
    jsonrpc: Literal["2.0"]
    result: Any


class SimpleValue(TypedDict):
    quantity: Union[Poly, Arbit]
    type: Literal["Simple"]


class AssetValue(TypedDict):
    quantity: Union[str, int]
    security_root: SecurityRoot
    metadata: Union[bytes, HexStr, Base58Str]
    type: Literal['Asset']


Middleware = Callable[[Callable[[RPCEndpoint, Any], RPCResponse], "Brambl"], Any]
MiddlewareOnion = NamedElementOnion[str, Middleware]

URI = NewType('URI', str)
BlockNumber = NewType('BlockNumber', int)
BlockParams = Literal["latest", "earliest", "pending"]
BlockIdentifier = Union[BlockParams, BlockNumber, Base58Str, int]
Timestamp = NewType("Timestamp", int)
Nonce = NewType('Nonce', int)

AssetRawTxParams = TypedDict("AssetRawTxParams", {
    "propositionType": str,
    "data": Union[bytes, HexStr, Base58Str],
    # addrs
    "sender": Sequence[Union[Address, str]],
    "recipients": Sequence[Tuple[Union[Address, str], AssetValue]],
    "fee": Poly,
    "changeAddress": Union[Address, str],
    "consolidationAddress": Union[Address, str],
    "minting": bool,
    "boxSelectionAlgorithm": str,
}, total=False)

AssetTxParams = TypedDict("AssetTxParams", {
    # addrs
    "from": Sequence[Tuple[Union[Address, str], Nonce]],
    "to": Sequence[Tuple[Union[Address, str], AssetValue]],
    "fee": Poly,
    "timestamp": Timestamp,
    "data": Union[bytes, HexStr, Base58Str],
    "minting": bool,
    "propositionType": str
}, total=False)

PolyRawTxParams = TypedDict("PolyRawTxParams", {
    "propositionType": str,
    "data": Union[bytes, HexStr, Base58Str],
    # addrs
    "sender": Sequence[Union[Address, str]],
    "recipients": Sequence[Tuple[Union[Address, str], SimpleValue]],
    "fee": Poly,
    "changeAddress": Union[Address, str],
    "boxSelectionAlgorithm": str,
}, total=False)

PolyTxParams = TypedDict("PolyTxParams", {
    # addrs
    "from": Sequence[Tuple[Union[Address, str], Nonce]],
    "to": Sequence[Tuple[Union[Address, str], SimpleValue]],
    "fee": Poly,
    "timestamp": Timestamp,
    "data": Union[bytes, HexStr, Base58Str],
    "propositionType": str
}, total=False)

ArbitRawTxParams = TypedDict("ArbitRawTxParams", {
    "propositionType": str,
    "data": Union[bytes, HexStr, Base58Str],
    # addrs
    "sender": Sequence[Union[Address, str]],
    "recipients": Sequence[Tuple[Union[Address, str], SimpleValue]],
    "fee": Poly,
    "changeAddress": Union[Address, str],
    "consolidationAddress": Union[Address, str],
    "boxSelectionAlgorithm": str,
}, total=False)

ArbitTxParams = TypedDict("ArbitTxParams", {
    # addrs
    "from": Sequence[Tuple[Union[Address, str], Nonce]],
    "to": Sequence[Tuple[Union[Address, str], SimpleValue]],
    "fee": Poly,
    "timestamp": Timestamp,
    "data": Union[bytes, HexStr, Base58Str],
    "propositionType": str,
    "minting": bool
}, total=False)


class Box(TypedDict, total=False):
    id: BoxId
    type: str
    evidence: Evidence
    value: SimpleValue
    nonce: Nonce


class Transaction(TypedDict, total=False):
    txId: ModifierId
    txType: str
    propositionType: str
    newBoxes: Sequence[Box]
    boxesToRemove: Sequence[BoxId]
    signatures: Sequence[Tuple[Proposition, Proof]]
    fee: Poly
    timestamp: Timestamp
    minting: bool
    data: Union[bytes, HexStr, Base58Str]


class BlockHeader(TypedDict, total=False):
    id: ModifierId
    parentId: ModifierId
    timestamp: Timestamp
    generatorBox: Box
    publicKey: Proposition
    signature: Proof
    height: int
    difficulty: int
    txRoot: Digest32
    bloomFilter: Sequence[int]
    version: Version


class BlockBody(TypedDict, total=False):
    id: ModifierId
    parentId: ModifierId
    txs: Sequence[Transaction]
    version: Version


class Block(TypedDict, total=False):
    header: BlockHeader
    body: BlockBody
    blockSize: int


class BlockData(TypedDict, total=False):
    height: int
    score: int
    bestBlockId: ModifierId
    bestBlock: Block
