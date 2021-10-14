from base58 import b58decode
from brambl.consts import ADDRESS_LENGTH, PropositionType
from brambl.utils.Hash import digestAndEncode, hashFunc

class Address(object):
    """
    Topl Base Address class. Does no validation, it is up to the child classes.

    Compares with ``str`` and ``bytes`` objects

    :param addr: the address as ``str`` or ``bytes`` or ``Address``
    """
    _address = ""

    def __init__(self, addr):
        self._address = addr
    
    def __repr__(self):
        return str(self._address)
    
    def __eq__(self, other):
        if isinstance(other, Address):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        elif isinstance (other, bytes):
            return str(self).encode() == other
        return super(Address, self).__eq__(other)
    
    def __hash__(self):
        return hash(str(self))
    
    def __format__(self, spec):
        return format(str(self), spec)

class PublicKeyCurve25519Address(Address):
    propositionType = PropositionType.PUBLICKEYCURVE25519

class ThresholdCurve25519Address(Address):
    pass

class PublicKeyEd25519Address(Address):
    propositionType = PropositionType.PUBLICKEYED25519


VALID_NETWORKS = ('private', 'toplnet', 'valhalla')
PRIVATE_MAP = {'hex': hex(64), 'decimal': 64}
TOPLNET_MAP = {'hex': hex(1), 'decimal': 1}
VALHALLA_MAP = {'hex': hex(1), 'decimal': 16}
NETWORKS_DEFAULT = {
    "private": PRIVATE_MAP,
    "toplnet": TOPLNET_MAP,
    "valhalla": VALHALLA_MAP 
}

def address(addr, networkPrefix: str):
    if isinstance(addr, Address):
        return addr # already instantiated and should be of the proper class
    elif isinstance(addr, (bytes, bytearray)):
        addr = addr.decode()
    elif not isinstance(addr, str):
        raise TypeError(
            "address() argument must be str, bytes, bytearray, or Address instance"
        )
    #validation
    if (validateAddressByNetwork(networkPrefix = networkPrefix, address= addr)):
        return PublicKeyEd25519Address(addr)
    else:
        raise ValueError("String {} is not a valid Topl address".format(addr))

def validateAddressByNetwork(networkPrefix: str, address: str):
    """
       Checks if the address is valid by the following 4 steps:
    1. Verify that the address is not null.
    2. Verify that the address is 38 bytes long.
    3. Verify that it matches the network
    4. Verify that the hash matches the checksum
    The first argument is the prefix to validate against and the second argument is the address to run the validation on.
    Result object with whether or not the operation was successful and whether or not the address is valid for a given network
    """
    if (not isValidNetwork(networkPrefix)):
       raise ValueError(
           "Invalid network provided"
       )
    elif (address == ""):
        raise ValueError(
            "No Addresses provided"
        )
    # get the decimal of the network prefix. It should always be a valid network prefix due to the first conditional, but the language constraint requires us to check if it is null first.
    networkDecimal = NETWORKS_DEFAULT[networkPrefix]['decimal']

    # run validation on the address
    decodedAddress = b58decode(address)

    # validation: base58 38 byte obj that matches the networkPrefix hex value
    if (len(decodedAddress) != ADDRESS_LENGTH):
        raise ValueError(
            "Invalid address for network '{}'".format(networkPrefix)

        )
    elif (not verify_checksum(decodedAddress)):
        raise ValueError(
            'Supplied address has invalid checksum'
        )
    return True


def verify_checksum(address):
    """ Verify checksum for address

    :param address: incoming address
    
    :return return True if address checksum is correct  
    
    """
    #print("address: " + str(address))
    if address is None:
        return None
    if (not isinstance(address, (bytes, bytearray))):
        return None
    msgBuffer = address[:34]
    checksum = address[34:]
    #print("checksum: " + str(checksum))
    # hash message (bytes 0-33)
    computed_checksum = (hashFunc().update(msgBuffer).digest())[:4]
    #print("computed_checksum" + str(computed_checksum))
    # verify checksum bytes match
    return checksum == computed_checksum

def isValidNetwork(networkPrefix: str):
    """
        Validates whether the network passed in is valid
    """
    return networkPrefix in VALID_NETWORKS