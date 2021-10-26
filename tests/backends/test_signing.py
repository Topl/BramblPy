import binascii

import pytest
from nacl.bindings import crypto_sign_SEEDBYTES, crypto_sign_PUBLICKEYBYTES
from nacl.encoding import HexEncoder, RawEncoder
from nacl.exceptions import BadSignatureError

from brambl.keys.datatypes import PrivateKey, PublicKey, BaseSignature
from brambl.utils.Hash import digestAndEncode, hashFunc
from tests.utils import read_crypto_test_vectors, assert_equal, assert_not_equal

MSG = b'message'
MSG_TO_SIGN = digestAndEncode(hashFunc().update(MSG))


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


class TestPrivateKey:

    def test_initialize_with_generate(self):
        PrivateKey.generate()

    def test_wrong_length(self):
        with pytest.raises(ValueError):
            PrivateKey(b"")

    def test_bytes(self):
        seed = b"\x00" * crypto_sign_SEEDBYTES
        k = PrivateKey(seed, encoder=RawEncoder)
        assert k._seed == b"\x00" * crypto_sign_SEEDBYTES

    def test_equal_keys_are_equal(self):
        k1 = PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
        k2 = PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
        assert_equal(k1, k1)
        assert_equal(k1, k2)

    @pytest.mark.parametrize(
        "k2",
        [
            PrivateKey(b"\x01" * crypto_sign_SEEDBYTES),
            PrivateKey(b"\x00" * (crypto_sign_SEEDBYTES - 1) + b"\x01"),
        ],
    )
    def test_different_keys_are_not_equal(self, k2):
        k1 = PrivateKey(b"\x00" * crypto_sign_SEEDBYTES)
        assert_not_equal(k1, k2)

    @pytest.mark.parametrize(
        "seed",
        [b"77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"],
    )
    def test_initialization_with_seed(self, seed):
        PrivateKey(seed, encoder=HexEncoder)

    @pytest.mark.parametrize(
        ("seed", "_public_key", "message", "signature", "expected"),
        ed25519_known_answers(),
    )
    def test_message_signing(
            self, seed, _public_key, message, signature, expected
    ):
        signing_key = PrivateKey(
            seed,
            encoder=HexEncoder
        )
        signed = signing_key.sign_msg_hash(
            binascii.unhexlify(message),
            encoder=HexEncoder
        )

        assert signed == expected
        assert signed.message == message
        assert HexEncoder.encode(signed.signature.to_bytes()) == signature


class TestPublicKey:

    def test_bytes(self):
        k = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        assert k.to_bytes() == b"\x00" * crypto_sign_PUBLICKEYBYTES

    def test_equal_keys_are_equal(self):
        k1 = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        k2 = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        assert_equal(k1, k1)
        assert_equal(k1, k2)

    def test_equal_keys_have_equal_hashes(self):
        k1 = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        k2 = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        assert hash(k1) == hash(k2)
        assert id(k1) != id(k2)

    @pytest.mark.parametrize(
        "k2",
        [
            PublicKey(b"\x01" * crypto_sign_PUBLICKEYBYTES),
            PublicKey(b"\x00" * (crypto_sign_PUBLICKEYBYTES - 1) + b"\x01"),
        ],
    )
    def test_different_keys_are_not_equal(self, k2):
        k1 = PublicKey(b"\x00" * crypto_sign_PUBLICKEYBYTES)
        assert_not_equal(k1, k2)

    @pytest.mark.parametrize(
        ("_seed", "public_key", "message", "signature", "signed"),
        ed25519_known_answers(),
    )
    def test_valid_signed_message(
            self, _seed, public_key, message, signature, signed
    ):
        key = PublicKey(
            public_key,
            encoder=HexEncoder,
        )

        assert (
                binascii.hexlify(
                    key.verify_msg_hash(signed, encoder=HexEncoder),

                )
                == message
        )
        assert (
                binascii.hexlify(
                    key.verify_msg_hash(
                        message, BaseSignature(signature, encoder=HexEncoder), encoder=HexEncoder
                    ),
                )
                == message
        )

    def test_invalid_signed_message(self):
        skey = PrivateKey.generate()
        msg = b"A Test Message!"
        smessage = skey.sign_msg(b"A Test Message!", encoder=RawEncoder)
        signature, message = smessage.signature, b"A Forged Test Message!"

        # Small sanity check
        assert skey.public_key.verify_msg(message=msg, signature=signature, encoder=RawEncoder)

        with pytest.raises(BadSignatureError):
            skey.public_key.verify_msg(message, signature, encoder=RawEncoder)

        with pytest.raises(ValueError):
            forged = BaseSignature(signature.to_bytes() + message, encoder=RawEncoder)
            skey.public_key.verify_signature(signature=forged, encoder=RawEncoder)

    def test_invalid_signature_length(self):
        skey = PrivateKey.generate()
        message = b"hello"
        signature = skey.sign_msg(message, encoder=RawEncoder).signature

        # Sanity checks
        assert skey.public_key.verify_msg(message, signature, encoder=RawEncoder)

        with pytest.raises(ValueError):
            skey.public_key.verify_msg(message, BaseSignature(b"", encoder=RawEncoder), encoder=RawEncoder)

        with pytest.raises(ValueError):
            skey.public_key.verify_msg(message, BaseSignature(signature.to_bytes() * 2, encoder=RawEncoder),
                                       encoder=RawEncoder)


def check_type_error(expected, f, *args):
    with pytest.raises(TypeError) as e:
        f(*args)
    assert expected in str(e.value)


def test_wrong_types():
    sk = PrivateKey.generate()

    check_type_error(
        "PrivateKey must be created from a 32 byte seed", PrivateKey, 12
    )
    check_type_error(
        "PrivateKey must be created from a 32 byte seed", PrivateKey, sk
    )
    check_type_error(
        "PrivateKey must be created from a 32 byte seed",
        PrivateKey,
        sk.public_key,
    )

    check_type_error("PublicKey must be created from 32 bytes", PublicKey, 13)
    check_type_error("PublicKey must be created from 32 bytes", PublicKey, sk)
    check_type_error(
        "PublicKey must be created from 32 bytes", PublicKey, sk.public_key
    )
