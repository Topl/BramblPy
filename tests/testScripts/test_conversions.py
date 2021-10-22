from typing import Dict
import pytest

from brambl import Brambl
from brambl.utils.conversions import Base58Str, HexStr, Primitives

@pytest.mark.parametrize(
    'val, expected',
    (
        (b'\x01', b'\x01'),
        (b'\xff', b'\xff'),
        (b'\x00', b'\x00'),
        (0x1, b'\x01'),
        (0x0001, b'\x01'),
        (0xFF, b'\xff'),
        (0, b'\x00'),
        (256, b'\x01\x00'),
        (True, b'\x01'),
        (False, b'\x00'),
    ),
)

@pytest.mark.parametrize(
    'val, expected',
    (
        ('0x', b''),
        ('0x0', b'\x00'),
        ('0x1', b'\x01'),
        ('0', b'\x00'),
        ('1', b'\x01'),
        ('0xFF', b'\xff'),
        ('0x100', b'\x01\x00'),
        ('0x0000', b'\x00\x00'),
        ('0000', b'\x00\x00'),
    ),
)
def test_to_bytes_hexstr(val, expected):
    assert Brambl.toBytes(hexstr=val) == expected

@pytest.mark.parameterize(
    'val, expected',
    (
        ('16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM', Brambl.toBytes(hexstr='00010966776006953D5567439E5E39F86A0D273BEED61967F6')),
        ('1v3VUYGogXD7S1E8kipahj7QXgC568dz1', Brambl.toBytes(hexstr = '000A08201462985DF5255E4A6C9D493C932FAC98EF791E2F22')),
        ('1axVFjCkMWDFCHjQHf99AsszXTuzxLxxg', Brambl.toBytes(hexstr = '00066C0B8995C7464E89F6760900EA6978DF18157388421561' ))
    )
)

def test_to_bytes_base58str(val, expected):
    assert(Brambl.toBytes(base58str = val) == expected)

@pytest.mark.parametrize(
    'val, expected',
    (
        ('cowmö', b'cowm\xc3\xb6'),
        ('', b''),
    ),
)
def test_to_bytes_text(val, expected):
    assert Brambl.toBytes(text=val) == expected

def test_to_text_identity():
    assert Brambl.toText(text='pass-through') == 'pass-through'

@pytest.mark.parametrize(
'val, expected',
(
    (b'', ''),
    ('0x', ''),
    (b'cowm\xc3\xb6', 'cowmö'),
    ('0x636f776dc3b6', 'cowmö'),
    (0x636f776dc3b6, 'cowmö'),
    ('0xa', '\n'),
),
)
def test_to_text(val, expected):
    assert Brambl.toText(val) == expected

@pytest.mark.parametrize(
    'val, expected',
    (
        (b'\x00', '0x00'),
        (b'\x01', '0x01'),
        (b'\x10', '0x10'),
        (b'\x01\x00', '0x0100'),
        (b'\x00\x0F', '0x000f'),
        (b'', '0x'),
        (0, '0x0'),
        (1, '0x1'),
        (16, '0x10'),
        (256, '0x100'),
        (0x0, '0x0'),
        (0x0F, '0xf'),
        (False, '0x0'),
        (True, '0x1'),
    ),
)
def test_to_hex(val, expected):
    assert Brambl.toHex(val) == expected

@pytest.mark.parameterize(
    'val, expected',
    (
        (61, '2g'),
        (626262, 'a3gV'),
        (636363, 'aPEr'),
    )
)

def test_int_to_base58(val, expected):
    assert Brambl.toBase58(primitive = val) == expected

@pytest.mark.parameterize(
    'val, expected',
    (
        ('73696d706c792061206c6f6e6720737472696e67', '2cFupjhnEsSn59qHXstmK2ffpLv2'),
        ('00eb15231dfceb60925886b67d065299925915aeb172c06647', '1NS17iag9jJgTHD1VXjvLCEnZuQ3rJDE9L'),
        ('516b6fcd0f', 'ABnLTmg'),
        ('bf4f89001e670274dd', '3SEo3LWLoPntC'),
        ('572e4794', '3EFU7m'),
        ('ecac89cad93923c02321', 'EJDM8drfXA6uyA'),
        ('10c8511e', 'Rt5zm'),
        ('00000000000000000000', '1111111111'),
        ('000111d38e5fc9071ffcd20b4a763cc9ae4f252bb4e48fd66a835e252ada93ff480d6dd43dc62a641155a5', '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
        ('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff', '1cWB5HCBdLjAuqGGReWE3R3CguuwSjw6RHn39s2yuDRTS5NsBgNiFpWgAnEx6VQi8csexkgYw3mdYrMHr8x9i7aEwP8kZ7vccXWqKDvGv3u1GxFKPuAkn8JCPPGDMf3vMMnbzm6Nh9zh1gcNsMvH3ZNLmP5fSG6DGbbi2tuwMWPthr4boWwCxf7ewSgNQeacyozhKDDQQ1qL5fQFUW52QKUZDZ5fw3KXNQJMcNTcaB723LchjeKun7MuGW5qyCBZYzA1KjofN1gYBV3NqyhQJ3Ns746GNuf9N2pQPmHz4xpnSrrfCvy6TVVz5d4PdrjeshsWQwpZsZGzvbdAdN8MKV5QsBDY')
    )
)

def test_hex_to_base58(val, expected):
    assert Brambl.toBase58(hexstr = val) == expected

@pytest.mark.parameterize(
'val, expected',
(
    (Brambl.toBytes(hexstr='00010966776006953D5567439E5E39F86A0D273BEED61967F6'), '16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM'),
    (Brambl.toBytes(hexstr = '000A08201462985DF5255E4A6C9D493C932FAC98EF791E2F22'), '1v3VUYGogXD7S1E8kipahj7QXgC568dz1'),
    (Brambl.toBytes(hexstr = '00066C0B8995C7464E89F6760900EA6978DF18157388421561' ), '1axVFjCkMWDFCHjQHf99AsszXTuzxLxxg')
)
)

def test_hex_to_base58(val, expected):
    assert Brambl.toBase58(primitive = val) == expected

@pytest.mark.parametrize(
    'val', 'expected',
    (
        (False, '0'),
        (True, '1')
    )
)

def test_bool_to_base58(val, expected):
    assert Brambl.toBase58(primitive = val) == expected

@pytest.mark.parametrize(
    'val', 'expected',
    (
        ('Hello World!', '2NEpo7TZRRrLZSi2U'),
        ('The quick brown fox jumps over the lazy dog.', 'USm3fpXnKG5EUBx2ndxBDMPVciP5hGey2Jh4NDv6gmeo1LkMeiKrLJUUBk6Z')
    )
)

def test_text_to_base58(val, expected):
    assert Brambl.toBase58(text = val) == expected

@pytest.mark.parametrize(
    'val, expected',
    (
        (Dict({'one': HexStr('0x1')}), '{"one": "0x01"}'),
        (Dict({'two': 2}), '{"two": "0x02"}'),
        (Dict({
            'three': Dict({
                'four': 4
            })
        }), '{"three": {"four": 4}}'),
        ({'three': 3}, '{"three": 3}'),
    ),
)
def test_to_json(val, expected):
    assert Brambl.toJSON(val) == expected

@pytest.mark.parametrize(
    'tx, expected',
    (
        (
            Dict({
                'blockId': Base58Str("yrAKht95CnZsv7VoW5rYeTMyt9BmkpUzjtu5jHr7xppR"),
                'blockNumber': 6928809,
                'from': ['3NLe6SSEccbD74NzwjLbPK9hsxjQfrVNuBuwsX4xxT6qKBsHNTjN'],
                'fee': 21000,
                'messageToSign': Base58Str("TGuwdJazPpdzen3EpM2Rw1L9FmYypxZ87jp8op94qe7pXz6pGmeT1Ne5BwVDyq4KA1GLTwtg9zuGvvbiYDkhAgxubBxapoAdw57dZWzBoZ95mPL6geKwhyqtCAXsK7cEE9WUtxkryxh5chQq1ujV6G2YqAtthdJDgENJYPq6Fh8x6bSfkitSdxJQAQJ74R5fQ6uXrr9fcpa3cg27NEpeivYvRGzSMoLZFwxsszrUnBNWZ1fypms25okopNnJdTqjdpiuU2cTNvxtjFFbUhun3AvaCpeMCQ33rsj1aWAiYS19kXWjaCSyeY7VAL83PQZCS2eHDBWkFNE19ViHPXz414dv1QWM5DdPHzFrQ7tuE"),
                'txType': 'AssetTransfer',
                'timestamp': 1634928659584,
                'signatures': {} ,
                'propositionType': 'PublicKeyEd25519',
                'txId': Base58Str('kya765xFsbhjg8LSECCd21WN8qvCM7VsbDjmwBHPKw7t'),
                'minting': True
            }),
            '{"blockId": "yrAKht95CnZsv7VoW5rYeTMyt9BmkpUzjtu5jHr7xppR", "blockNumber": 6928809, "from": ["3NLe6SSEccbD74NzwjLbPK9hsxjQfrVNuBuwsX4xxT6qKBsHNTjN"], "fee": 21000, "messageToSign": "TGuwdJazPpdzen3EpM2Rw1L9FmYypxZ87jp8op94qe7pXz6pGmeT1Ne5BwVDyq4KA1GLTwtg9zuGvvbiYDkhAgxubBxapoAdw57dZWzBoZ95mPL6geKwhyqtCAXsK7cEE9WUtxkryxh5chQq1ujV6G2YqAtthdJDgENJYPq6Fh8x6bSfkitSdxJQAQJ74R5fQ6uXrr9fcpa3cg27NEpeivYvRGzSMoLZFwxsszrUnBNWZ1fypms25okopNnJdTqjdpiuU2cTNvxtjFFbUhun3AvaCpeMCQ33rsj1aWAiYS19kXWjaCSyeY7VAL83PQZCS2eHDBWkFNE19ViHPXz414dv1QWM5DdPHzFrQ7tuE", "txType": "AssetTransfer", "timestamp": 1634928659584, "signatures": {}, "propositionType": "PublicKeyEd25519", "txId": "kya765xFsbhjg8LSECCd21WN8qvCM7VsbDjmwBHPKw7t", "minting": True}'  # noqa: E501
        ),
    ),
)
def test_to_json_with_transaction(tx, expected):
    assert Brambl.toJSON(tx) == expected