from base58 import b58decode
from brambl.address import Address
from brambl.metadata import Metadata
from brambl.utils.validation import validate_txId

class IOBase(object):

    """
        Underlying parent class for different representations of IO transactions

        :param sender: The address of the sender/s of this transaction.
        :param recipients: The recipient of this transaction. This is a required field.
        :param fee: The maximum amount of polys to spend on the network fee.
         If [fee] is `null`, this library will refer to the defaults
        for the given network.
        :param propositionType:   Type of proposition, eg., PublicKeyCurve25519, ThresholdCurve25519, PublicKeyEd25519
        :param data: Datastring which can be associated with this transaction (may be empty).
    """


    def __init__(self, fee = None, propositionType = None, data = None, minting = None, txType = None):
        self.fee = fee if fee is not None else 0
        self.propositionType = propositionType
        self.data = data if data is not None else Metadata()
        self.minting = minting
        self.txType = txType

class Input(IOBase):
    """
        Represents a Topl Transaction input

        :param changeAddress: The recipient of the returned UTXOs from poly transactions including left-over network fees. If [changeAddress] is `null`, this library will refer to the first sender included in the sender list
        :param fee: The maximum amount of polys to spend on the network fee.
         If [fee] is `null`, this library will refer to the defaults
        for the given network.
        Polys that are not used but included in [fee] will be returned to the
        changeAddress.
        :param recipients: The recipient of this transaction. This is a required field.
        :param consolidationAddress: The recipient of the change from the assetTransaction. This field can be set to null. It will most likely be set to null if the type is a polyTransaction
        :param minting: The minting parameter for asset transactions.
        :param assetCode: The encoded assetCode that the user wants to include on the asset box

    """
    sender = None
    changeAddress: None
    recipients: None
    consolidationAddress: None
    assetCode: None

    def __init__(self, sender = None, recipients = None, consolidationAddress = None, changeAddress = None, assetCode = None, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.sender = sender if sender is not None else []
        self.recipients = recipients if recipients is not None else []
        self.consolidationAddress = consolidationAddress
        self.changeAddress = changeAddress
        self.assetCode = assetCode

    def __repr__(self):
        return "<Topl tx: {:s}>".format(self.txid)

    def __format__(self, spec):
        return format(str(self), spec)
    
    def hash(self):
        return self.txid

class Output(IOBase):
    """
        Represents a Topl Transaction Output

        :param id: The hash of the message to sign.
        :param newBoxes: The number of boxes that were generated with this transaction.
        :param signatures: Proposition Type signature(s)
        :param timestamp: The time at which this transaction was received by the network
        :param boxesToRemove: The boxes that will be deleted as a result of this transaction
        :param messageToSign: The message that will have to be signed by the sender of this transaction
        :param status: Whether or not this transfer has been successfully confirmed into a block
        :param blockId: Hash of the messageToSign of this block where this transaction is in (32 bytes).
        :param blockNumber: The number of the block into which this transaction was forged
    """

    pass 
    