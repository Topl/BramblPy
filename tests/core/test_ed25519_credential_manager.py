import os

import pytest
from nacl.encoding import HexEncoder, RawEncoder

from brambl.credentials.credential_manager import Ed25519CredentialManager
from brambl.ed25519 import keys
from brambl.ed25519.utils.address import validateAddressByNetwork
from brambl.utils.conversions import to_bytes

import re

pattern = re.compile(r'\s+')

PRIVATE_KEY_AS_BYTES = b'\x9da\xb1\x9d\xef\xfdZ`\xba\x84J\xf4\x92\xec,\xc4DI\xc5i{2i\x19p;\xac\x03\x1c\xae\x7f`'
PRIVATE_KEY_AS_HEXSTR = '0x9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60'
PRIVATE_KEY_AS_INT = 0x9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60
PRIVATE_KEY_AS_OBJ = keys.SigningKey(PRIVATE_KEY_AS_BYTES)
ACCT_ADDRESS = 'AUENZqp67jaTKoXbgPXVMD4ZhWLHidKo115FEbacjPbHxhd8m2tM'

PRIVATE_KEY_AS_BYTES_ALT = b'L\xcd\x08\x9b(\xff\x96\xda\x9d\xb6\xc3F\xec\x11N\x0f[\x8a1\x9f5\xab\xa6$\xda\x8c\xf6\xedO\xb8\xa6\xfb'
PRIVATE_KEY_AS_HEXSTR_ALT = '0x4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb'
PRIVATE_KEY_AS_INT_ALT = 0x4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb
PRIVATE_KEY_AS_OBJ_ALT = keys.SigningKey(PRIVATE_KEY_AS_BYTES_ALT)


@pytest.fixture(
    params=[PRIVATE_KEY_AS_INT, PRIVATE_KEY_AS_HEXSTR, PRIVATE_KEY_AS_BYTES, PRIVATE_KEY_AS_OBJ])  # noqa: 501
def PRIVATE_KEY(request):
    return request.param


@pytest.fixture(params=[PRIVATE_KEY_AS_INT_ALT, PRIVATE_KEY_AS_HEXSTR_ALT, PRIVATE_KEY_AS_BYTES_ALT,
                        PRIVATE_KEY_AS_OBJ_ALT])  # noqa: 501
def PRIVATE_KEY_ALT(request):
    return request.param


@pytest.fixture(params=['instance', 'class'])
def key_man(request):
    if request.param == 'instance':
        return Ed25519CredentialManager()
    elif request.param == 'class':
        return Ed25519CredentialManager
    else:
        raise Exception("key manager invocation {request.param} is not supported")


@pytest.fixture(params=("text", "primitive", "hexstr"))
def message_encodings(request):
    if request == "text":
        return {"text": "hello world"}
    elif request == "primitive":
        return {"primitive": b"hello world"}
    else:
        return {"hexstr": "68656c6c6f20776f726c64"}


def test_brambl_key_manager_default_kdf(key_man, monkeypatch):
    assert os.getenv('TOPL_CREDENTIAL_KDF') is None
    assert key_man._default_kdf == 'scrypt'

    monkeypatch.setenv('TOPL_CREDENTIAL_KDF', 'pbkdf2')
    assert os.getenv('TOPL_CREDENTIAL_KDF') == 'pbkdf2'

    import importlib
    from brambl.credentials import credential_manager
    importlib.reload(credential_manager)
    assert credential_manager.Ed25519CredentialManager._default_kdf == 'pbkdf2'


def test_brambl_key_manager_create_variation(key_man):
    account1 = key_man.create(network_prefix=64)
    account2 = key_man.create(network_prefix=64)
    assert account1 != account2


def test_brambl_key_manager_equality(key_man, PRIVATE_KEY):
    acct1 = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    acct2 = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    assert acct1 == acct2


def test_brambl_key_manager_from_key_reproducible(key_man, PRIVATE_KEY):
    account1 = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    account2 = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    assert bytes(account1) == bytes(account2)
    assert isinstance(str(account1), str)


def test_brambl_key_manager_from_key_diverge(key_man, PRIVATE_KEY, PRIVATE_KEY_ALT):
    key_man1 = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    key_man2 = key_man.from_key(PRIVATE_KEY_ALT, network_prefix=64)
    assert bytes(key_man1) != bytes(key_man2)


def test_brambl_key_manager_from_key_restrictions(key_man):
    with pytest.raises(ValueError):
        key_man.from_key(b'', network_prefix=64)
    with pytest.raises(ValueError):
        key_man.from_key(b'\xff' * 31, network_prefix=64)
    with pytest.raises(ValueError):
        key_man.from_key(b'\xff' * 33, network_prefix=64)


def test_brambl_credential_manager_from_key_properties(key_man, PRIVATE_KEY):
    credential_manager = key_man.from_key(PRIVATE_KEY, network_prefix=64)
    assert callable(credential_manager.sign_transaction)
    assert callable(credential_manager.sign_message)
    assert validateAddressByNetwork('private', str(credential_manager.address))
    assert str(credential_manager.address) == ACCT_ADDRESS


def test_brambl_credential_manager_create_properties(key_man):
    account = key_man.create(64)
    assert callable(account.sign_transaction)
    assert callable(account.sign_message)
    assert validateAddressByNetwork('private', str(account.address))


@pytest.mark.parametrize(
    'keyed_credential, message, expected',
    [
        (
                Ed25519CredentialManager.from_key(PRIVATE_KEY_AS_BYTES, network_prefix=64),
                '',
                b'e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b'
        ),
        (
                Ed25519CredentialManager.from_key('0x4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb',
                                                  network_prefix=64),
                '0x72',
                b'92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00'
        ),
        (
                Ed25519CredentialManager.from_key('c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7',
                                                  network_prefix=64),
                '0xaf82',
                b'6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a'
        ),
        (
                Ed25519CredentialManager.from_key('f5e5767cf153319517630f226876b86c8160cc583bc013744c6bf255f5cc0ee5',
                                                  network_prefix=64),
                re.sub(pattern, "", """
                    08b8b2b733424243760fe426a4b54908632110a66c2f6591eabd3345e3e4eb98fa6e264bf09efe12ee50f8f54e9f77b1e355f6c50544e23fb1433ddf73be84d8
                    79de7c0046dc4996d9e773f4bc9efe5738829adb26c81b37c93a1b270b20329d658675fc6ea534e0810a4432826bf58c941efb65d57a338bbd2e26640f89ffbc
                    1a858efcb8550ee3a5e1998bd177e93a7363c344fe6b199ee5d02e82d522c4feba15452f80288a821a579116ec6dad2b3b310da903401aa62100ab5d1a36553e
                    06203b33890cc9b832f79ef80560ccb9a39ce767967ed628c6ad573cb116dbefefd75499da96bd68a8a97b928a8bbc103b6621fcde2beca1231d206be6cd9ec7
                    aff6f6c94fcd7204ed3455c68c83f4a41da4af2b74ef5c53f1d8ac70bdcb7ed185ce81bd84359d44254d95629e9855a94a7c1958d1f8ada5d0532ed8a5aa3fb2
                    d17ba70eb6248e594e1a2297acbbb39d502f1a8c6eb6f1ce22b3de1a1f40cc24554119a831a9aad6079cad88425de6bde1a9187ebb6092cf67bf2b13fd65f270
                    88d78b7e883c8759d2c4f5c65adb7553878ad575f9fad878e80a0c9ba63bcbcc2732e69485bbc9c90bfbd62481d9089beccf80cfe2df16a2cf65bd92dd597b07
                    07e0917af48bbb75fed413d238f5555a7a569d80c3414a8d0859dc65a46128bab27af87a71314f318c782b23ebfe808b82b0ce26401d2e22f04d83d1255dc51a
                    ddd3b75a2b1ae0784504df543af8969be3ea7082ff7fc9888c144da2af58429ec96031dbcad3dad9af0dcbaaaf268cb8fcffead94f3c7ca495e056a9b47acdb7
                    51fb73e666c6c655ade8297297d07ad1ba5e43f1bca32301651339e22904cc8c42f58c30c04aafdb038dda0847dd988dcda6f3bfd15c4b4c4525004aa06eeff8
                    ca61783aacec57fb3d1f92b0fe2fd1a85f6724517b65e614ad6808d6f6ee34dff7310fdc82aebfd904b01e1dc54b2927094b2db68d6f903b68401adebf5a7e08
                    d78ff4ef5d63653a65040cf9bfd4aca7984a74d37145986780fc0b16ac451649de6188a7dbdf191f64b5fc5e2ab47b57f7f7276cd419c17a3ca8e1b939ae49e4
                    88acba6b965610b5480109c8b17b80e1b7b750dfc7598d5d5011fd2dcc5600a32ef5b52a1ecc820e308aa342721aac0943bf6686b64b2579376504ccc493d97e
                    6aed3fb0f9cd71a43dd497f01f17c0e2cb3797aa2a2f256656168e6c496afc5fb93246f6b1116398a346f1a641f3b041e989f7914f90cc2c7fff357876e506b5
                    0d334ba77c225bc307ba537152f3f1610e4eafe595f6d9d90d11faa933a15ef1369546868a7f3a45a96768d40fd9d03412c091c6315cf4fde7cb68606937380d
                    b2eaaa707b4c4185c32eddcdd306705e4dc1ffc872eeee475a64dfac86aba41c0618983f8741c5ef68d3a101e8a3b8cac60c905c15fc910840b94c00a0b9d0
                """),
                b'0aab4c900501b3e24d7cdf4663326a3a87df5e4843b2cbdb67cbf6e460fec350aa5371b1508f9f4528ecea23c436d94b5e8fcd4f681e30a6ac00a9704a188a03'
        ),
(
                Ed25519CredentialManager.from_key('833fe62409237b9d62ec77587520911e9a759cec1d19755b7da901b96dca3d42',
                                                  network_prefix=64),
                '0xDDAF35A193617ABACC417349AE20413112E6FA4E89A97EA20A9EEEE64B55D39A2192992A274FC1A836BA3C23A3FEEBBD454D4423643CE80E2A9AC94FA54CA49F',
                b'dc2a4459e7369633a52b1bf277839a00201009a3efbf3ecb69bea2186c26b58909351fc9ac90b3ecfdfbc7c66431e0303dca179c138ac17ad9bef1177331a704'
        ),
    ],
    ids=['hexbytes_1', 'hex_bytes2', 'hex_bytes3', 'hex_bytes4', 'hex_bytes5']
)
def test_sign_message(keyed_credential, message, expected):
    # sign via message
    signed_via_message = keyed_credential.sign_message(to_bytes(hexstr=message), encoder=RawEncoder)
    assert HexEncoder.encode(signed_via_message.signature.to_bytes()) == expected
