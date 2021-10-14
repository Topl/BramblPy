from base58 import b58decode, b58encode


class AssetCode(object):
    """
        Represents the ID of a native Topl asset. It consists of the asset name in addition to the issuer address. It renders as a string representation of ``asset_name:issuer_address``. 

        The ``asset_name`` is always less than or equal to 8 Latin-1 encoded characters (string) and must be passed to the constructor as such.

        The ``.encoded`` property is a :class: `string` encoded representation of the requisite parts listed above. Because Topl allows the full Latin1 set to be used in asset names, some of them are not safe to be displayed directly. 
    """

    asset_name = ""
    issuer_address = None
    encoded = None

    def __init__(self, asset_name, issuer_address):
        """
        Please note that the issuer_address is assumed to be valid. This implementation does not check the validity of the issuer_address
        """
        asset_name = asset_name if asset_name is not None else self.asset_name
        issuer_address = issuer_address or self.issuer_address
        if len(asset_name) > 8:
            raise ValueError("Asset short names must be less than 8 Latin-1 encoded characters")
        if isinstance(asset_name, bytes):
            self.asset_name = asset_name.decode('latin-1').ljust(8, bytes([0]).decode('latin-1'))
        elif isinstance(asset_name, str):
            self.asset_name = asset_name.ljust(8, bytes([0]).decode('latin-1'))
        else:
            raise ValueError(
                "The asset_name is neither str or bytes but {}".format(type(self.asset_name))
            )
        self.issuer_address = issuer_address

    def serialize(self):
        addressBytes = b58decode(str(self.issuer_address))
        slicedAddress = addressBytes[:34]
        # concat 01 [version] + 34 bytes [address] + ^8bytes [asset name]
        version = bytes([1])
        concatValues = version + slicedAddress + bytes(self.asset_name, 'latin-1')
        return b58encode(concatValues)

    def __repr__(self):
        return "{:s}:{:s}".format(self.asset_name, self.issuer_address)

    def __eq__(self, other):
        if isinstance(other, AssetCode):
            return str(self) == str(other)
        elif isinstance(other, str):
            return self.serialize().decode('latin-1') == other
        elif isinstance(other, bytes):
            return b58decode(self.serialize()) == other
        return super(AssetCode, self).__eq__(other)

    def __hash__(self):
        return hash(str(self))
