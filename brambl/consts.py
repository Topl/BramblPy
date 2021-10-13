import enum

ADDRESS_LENGTH = 38

class PropositionType(enum.IntEnum):
    """
    Represents Topl proposition types
    .. warning:: ** Do NOT use the integer values directly. **
        There are potentially going to be new proposition types introduced. However, you may use comparison operators between them since they will be sorted chronologically by when they were introduced into the Topl ecosystem 
    """

    PUBLICKEYCURVE25519 = 1
    THRESHOLDKEYCURVE25519 = 2
    PUBLICKEYED25519 = 3
