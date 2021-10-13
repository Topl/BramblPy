from brambl.modules.Requests import validate_txId

class IOBase(object):
    def __init__(self, sender = None, recipient = None, fee = None):
        self.sender = None if address is None else 


class Input(object):
    """
        Represents a Topl Transaction input

        :param propositionType:   Type of proposition, eg., PublicKeyCurve25519, ThresholdCurve25519, PublicKeyEd25519
        :param sender: The address of the sender/s of this transaction.
        :param changeAddress: The recipient of the returned UTXOs from poly transactions including left-over network fees. If [changeAddress] is `null`, this library will refer to the first sender included in the sender list
        :param fee: The maximum amount of polys to spend on the network fee.
         If [fee] is `null`, this library will refer to the defaults
        for the given network.
        Polys that are not used but included in [fee] will be returned to the
        changeAddress.
        :param data: Datastring which can be associated with this transaction (may be empty).
        :param recipients: The recipient of this transaction. This is a required field.
        :param consolidationAddress: The recipient of the change from the assetTransaction. This field can be set to null. It will most likely be set to null if the type is a polyTransaction
        :param minting: The minting parameter for asset transactions.
        :param assetCode: The encoded assetCode that the user wants to include on the asset box

    """

    propositionType = None
    fee = None
    sender = None
    changeAddress: None
    data: None
    recipients: None
    consolidationAddress: None
    minting: None
    assetCode: None

    def __init__(self, txid=None, **kwargs):
        self.txid = txid or self.txid
        validate_txId(self.txid)
        fee = kwargs.pop("fee", None)
        self.fee = fee if fee is not None else self.fee
        self.sender = kwargs.pop("sender", []) or (
            self.sender if self.sender is not None else []
        )    
        self.recipients = kwargs.pop("recipients", []) or (
            self.recipients if self.recipients is not None else []
        )
        self.propositionType = kwargs.pop("propositionType", None) or self.propositionType
        self.data = kwargs.pop("data", None) or self.data
        self.consolidationAddress = kwargs.pop('consolidationAddress', None) or self.consolidationAddress
        self.changeAddress = kwargs.pop('changeAddress', None) or self.changeAddress
        self.minting = kwargs.pop('minting', None) or self.minting
        self.assetCode = kwargs.pop('assetCode', None) or self.assetCode

    def __repr__(self):
        return "<Topl tx: {:s}>".format(self.txid)

    def __format__(self, spec):
        return format(str(self), spec)
    
    def hash(self):
        return self.txid

class Output