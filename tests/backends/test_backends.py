import binascii

import pytest
from nacl.bindings import crypto_sign_SEEDBYTES, crypto_sign_PUBLICKEYBYTES
from nacl.encoding import HexEncoder, RawEncoder
from nacl.exceptions import BadSignatureError

from brambl.ed25519.backends import NativeECCBackend
from brambl.ed25519.datatypes import BaseSignature, PrivateKey, PublicKey
from brambl.utils.Hash import digestAndEncode, hashFunc
from build.lib.brambl.keys import Ed25519CredentialApi
from tests.utils import read_crypto_test_vectors, assert_equal, assert_not_equal

MSG = b'message'
MSG_TO_SIGN = digestAndEncode(hashFunc().update(MSG))

backends = [
    NativeECCBackend(),
]


def backend_id_fn(backend):
    return type(backend).__name__


@pytest.fixture(params=backends, ids=backend_id_fn)
def credential_api(request):
    return Ed25519CredentialApi(backend=request.param)


def ed25519_known_answers():
    # Known answers taken from: http://ed25519.cr.yp.to/python/sign.input
    # hex-encoded fields on each input line: sk||pk, pk, msg, signature||msg
    # known answer fields: sk, pk, msg, signature, signed
    DATA = "ed25519"
    lines = read_crypto_test_vectors(DATA, delimiter=b":")
    return [
        (
            x[0][:64],  # secret key
            x[1],  # public key
            x[2],  # message
            x[3][:128],  # signature
            x[3],  # signed message
        )
        for x in lines
    ]


def test_initialize_with_generate(credential_api):
    credential_api.PrivateKey.generate()


def test_wrong_length(credential_api):
    with pytest.raises(ValueError):
        credential_api.PrivateKey(b"")


def test_bytes(credential_api):
    seed = b"\x00" * crypto_sign_SEEDBYTES
    k = credential_api.PrivateKey(seed, encoder=RawEncoder)
    assert k._seed == b"\x00" * crypto_sign_SEEDBYTES


def test_equal_keys_are_equal(credential_api):
    k1 = credential_api.PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
    k2 = credential_api.PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
    assert_equal(k1, k1)
    assert_equal(k1, k2)


@pytest.mark.parametrize(
    "k2",
    [
        PrivateKey(b"\x01" * crypto_sign_SEEDBYTES),
        PrivateKey(b"\x00" * (crypto_sign_SEEDBYTES - 1) + b"\x01"),
    ],
)
def test_different_keys_are_not_equal(credential_api, k2):
    k1 = credential_api.PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
    assert_not_equal(k1, k2)


@pytest.mark.parametrize(
    "seed",
    [b"77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"],
)
def test_initialization_with_seed(credential_api, seed):
    credential_api.PrivateKey(seed, encoder=HexEncoder)


@pytest.mark.parametrize(
    ("seed", "_public_key", "message", "signature", "expected"),
    ed25519_known_answers(),
)
def test_message_signing(seed, _public_key, message, signature, expected, credential_api
                         ):
    signing_key = credential_api.PrivateKey(
        seed,
        encoder=HexEncoder
    )
    proof = credential_api.ecc_sign(binascii.unhexlify(message), signing_key, encoder=HexEncoder)

    assert proof == expected
    assert proof.message == message
    assert HexEncoder.encode(proof.signature.to_bytes()) == signature


def test_bytes(credential_api):
    k = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    assert k.to_bytes() == b"\x00" * crypto_sign_PUBLICKEYBYTES


def test_equal_keys_are_equal(credential_api):
    k1 = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    k2 = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    assert_equal(k1, k1)
    assert_equal(k1, k2)


def test_equal_keys_have_equal_hashes(credential_api):
    k1 = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    k2 = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    assert hash(k1) == hash(k2)
    assert id(k1) != id(k2)


@pytest.mark.parametrize(
    "k2",
    [
        PublicKey(b"\x01" * crypto_sign_PUBLICKEYBYTES),
        PublicKey(b"\x00" * (crypto_sign_PUBLICKEYBYTES - 1) + b"\x01"),
    ],
)
def test_different_keys_are_not_equal(k2, credential_api):
    k1 = credential_api.PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
    assert_not_equal(k1, k2)


@pytest.mark.parametrize(
    ("_seed", "public_key", "message", "signature", "signed"),
    ed25519_known_answers(),
)
def test_valid_signed_message(credential_api, _seed, public_key, message, signature, signed
                              ):
    key = credential_api.PublicKey(
        public_key,
        encoder=HexEncoder,
    )
    assert (
            binascii.hexlify(
                credential_api.ecc_verify(
                    BaseSignature(signature, encoder=HexEncoder), key, message, encoder=HexEncoder
                ),
            )
            == message
    )


def test_invalid_signed_message(credential_api):
    skey = credential_api.PrivateKey.generate()
    msg = b"A Test Message!"
    smessage = credential_api.ecc_sign(b"A Test Message!", private_key=skey, encoder=RawEncoder)
    signature, message = smessage.signature, b"A Forged Test Message!"

    # Small sanity check
    assert credential_api.ecc_verify(message=msg, signature=signature, public_key=skey.public_key, encoder=RawEncoder)

    with pytest.raises(BadSignatureError):
        credential_api.ecc_verify(message=message, signature=signature, public_key=skey.public_key, encoder=RawEncoder)


def test_invalid_signature_length(credential_api):
    skey = credential_api.PrivateKey.generate()
    message = b"hello"
    signature = credential_api.ecc_sign(message, private_key=skey, encoder=RawEncoder).signature

    # Sanity checks
    assert credential_api.ecc_verify(message=message, signature=signature, public_key=skey.public_key,
                                     encoder=RawEncoder)

    with pytest.raises(ValueError):
        credential_api.ecc_verify(message=message, signature=BaseSignature(b"", encoder=RawEncoder),
                                  public_key=skey.public_key,
                                  encoder=RawEncoder)


def check_type_error(expected, f, *args):
    with pytest.raises(TypeError) as e:
        f(*args)
    assert expected in str(e.value)


def test_wrong_types(credential_api):
    sk = credential_api.PrivateKey.generate()

    check_type_error(
        "PrivateKey must be created from a 32 byte seed", credential_api.PrivateKey, 12
    )
    check_type_error(
        "PrivateKey must be created from a 32 byte seed", credential_api.PrivateKey, sk
    )
    check_type_error(
        "PrivateKey must be created from a 32 byte seed",
        credential_api.PrivateKey,
        sk.public_key,
    )

    check_type_error("PublicKey must be created from 32 bytes", credential_api.PublicKey, 13)
    check_type_error("PublicKey must be created from 32 bytes", credential_api.PublicKey, sk)
    check_type_error(
        "PublicKey must be created from 32 bytes", credential_api.PublicKey, sk.public_key
    )
