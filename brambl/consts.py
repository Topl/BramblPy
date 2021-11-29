import enum

ADDRESS_LENGTH = 38
BLAKE2B256_DIGEST_SIZE = 32
TRANSACTION_ID_SIZE = BLAKE2B256_DIGEST_SIZE + 1
TRANSACTION_MODIFIER_TYPE = 2


class PropositionType(enum.IntEnum):
    """
    Represents Topl proposition types
    .. warning:: ** Do NOT use the integer values directly. **
        There are potentially going to be new proposition types introduced. However, you may use comparison operators between them since they will be sorted chronologically by when they were introduced into the Topl ecosystem 
    """

    PUBLICKEYCURVE25519 = 1
    THRESHOLDKEYCURVE25519 = 2
    PUBLICKEYED25519 = 3


TOPLNET = 'Mainnet';
TOPLNET_FEE = 1000000000;
VALHALLA = 'ValhallaTestnet';
VALHALLA_FEE = 100;
PRIVATE = 'PrivateTestnet';
