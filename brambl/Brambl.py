import json
from functools import wraps
from typing import Dict, Any

import base58

from brambl.modules import Requests

from brambl.typing.encoding import Base58Str, HexStr
from brambl.utils import Hash

from brambl.utils.conversions import to_bytes, Primitives, to_text, to_hex, to_base58
from brambl.utils.encoding import to_json

# Constants definitions
validTxMethods = ['createAssetsPrototype', 'transferAssetsPrototype', 'transferTargetAssetsPrototype']


class Brambl:
    """
    Each sub-module may be initialized in one of three ways

    1.Providing a separetly initialized Request and KeyManager instance. Each of these instances may be initialized 
    using the static methods `Requests` or `KeyManager` available in the BramblJS class.

    2.Providing custom configuration parameters needed to create new instances of each sub-module with the specified 
    parameters

    3.Providing minimal inputs (i.e. calling Brambl with only a string constructor arguement). This will create new 
    instances of the sub-modules with default parameters. KeyManager will create a new keyfile and Requests will target
     a locally running instance of Bifrost.

    :param params: A password string or dictionary containing an instance of `Requests` and `KeyManager`
    :param params['KeyManager']: KeyManager object (may be either an instance or config parameters)
    :param params['KeyManager]['password']: The password used to encrpt the keyfile
    :param params['KeyManager']['instance']: A previously initialized instance of KeyManager
    :param params['KeyManager']['keyPath']: Path to a keyfile
    :param params['KeyManager']['constansts']: Parameters for encrypting the user's keyfile
    :param params['Requests']: Request object (may be either an instance or config parameters)
    :param params['Requests']['url']: The chain provider to send requests to
    :param params['Requests']['api_key']: Api key for authorizing access to the chain provider.
    :type params: dictionary
    :type params['KeyManager']: `KeyManager` object
    :type params['KeyManager]['password']: string
    :type params['KeyManager']['instance']: `KeyManager` instance
    :type params['KeyManager']['keyPath']: string
    :type params['KeyManager']['constansts']: dictionary
    :type params['Requests']: `Requests` object
    :type params['Requests']['url']: string
    :type params['Requests']['api_key']: string
    :return: `Brambl` object
    :rtype: instance of `Brambl`
    
    """

    def __init__(self, params):
        # default values for the constructor arguement
        try:
            self.keyManagerVar = params['KeyManager']
        except:
            self.keyManagerVar = {}

        try:
            self.requestsVar = params['Requests']
        except:
            self.requestsVar = {}

        # if only a string is given in the constructor, assuem it is the password
        # Therefore, target a local chain provider and make a new key
        if type(params) == type('string'):
            self.keyManagerVar['password'] = params

        # Setup requests object
        try:
            self.requests = self.requestsVar['instance']
        except:
            try:
                self.requests = Requests.Requests(self.requestsVar['url'], self.requestsVar['api_key'])
            except:
                self.requests = Requests.Requests()
        # Import utilities
        self.utils = Hash

    def Requests(test_url="http://localhost:9085/", api_key="topl_the_world!"):
        """
        Method for creating a separate Requests instance

        :param test_url: Chain provider location, defaults to "http://localhost:9085/" 
        :param api_key: Access key for authorizing requests to the client API, defaults to "topl_the_world!"
        :type test_url: string
        :type api_key: string
        :return: `Requests` object
        :rtype: instance of `Requests`
        """
        return Requests.Requests(test_url, api_key)

    async def addSigToTx(self, prototypeTx, userKeys):
        """
        Add a signature to a prototype transaction using the an unlocked key manager object

        :param prototypeTx: An unsigned transaction JSON object
        :param userKeys: A keyManager object containing the user's key (may be a list)
        :type arg1: JSON
        :type arg1: List or `KeyManager` instance
        :return: transaction object
        :rtype: JSON

        """

        # function for generating a signature in the correct format
        def getSig(ks, tx_bytes):
            from_entries = {}
            for k in ks:
                prop_01 = bytes.fromhex("01")
                prop = b''.join([prop_01, base58.b58decode(k.pk)])
                sig = b''.join([prop_01, k.sign(tx_bytes)])
                from_entries[base58.b58encode(prop).decode('utf-8')] = base58.b58encode(sig).decode('utf-8')
            return from_entries

        # incase a single given is given not as an array
        keys = []
        if isinstance(userKeys, list):
            keys.append(userKeys)
        else:
            keys = userKeys

        # add signatures of all given key files to the formatted transaction
        prototype_tx_dic = json.loads(prototypeTx)
        temp_dic = {}
        for key in prototype_tx_dic['result']['rawTx']:
            temp_dic[key] = prototype_tx_dic['result']['rawTx'][key]

        temp_dic['signatures'] = getSig(keys, base58.b58decode(prototype_tx_dic['result']['messageToSign']))
        return json.dumps(temp_dic)

    async def signAndBroadcast(self, prototypeTx):
        """
        Used to sign a prototype transaction and broadcast to a chain provider
        :param prototypeTx: An unsigned transaction JSON object
        :type prototypeTx: ? 
        :return: broadcastTx Request
        :rtype: JSON 

        """
        # may return dictionary?
        formatted_tx = self.addSigToTx(prototypeTx, self.keyManager)
        return self.requests.broadcastTx({'tx': formatted_tx})

    async def transaction(self, method, params):
        """
        Create a new transaction, then sign and broadcast

        :param method: The chain resource method (string) to create a transaction for
        :param params: parameters for chain request
        :type method: string
        :type params: type description
        :return: new transaction object
        :rtype: JSON

        """
        if method not in validTxMethods:
            raise Exception('Invalid transaction method')

        if method == 'createAssetsPrototype':
            return await self.signAndBroadcast(self.requests.createAssetsPrototype(params))
        elif method == 'transferAssetsPrototype':
            return await self.signAndBroadcast(self.requests.transferAssetsPrototype(params))
        elif method == 'transferTargetAssetsPrototype':
            return await self.signAndBroadcast(self.requests.transferTargetAssetsPrototype(params))

    # Encoding and Decoding
    @staticmethod
    @wraps(to_bytes)
    def toBytes(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> bytes:
        return to_bytes(primitive, hexstr, text)

    @staticmethod
    @wraps(to_text)
    def toText(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> str:
        return to_text(primitive=primitive, hexstr=hexstr, text=text)

    @staticmethod
    @wraps(to_hex)
    def toHex(
            primitive: Primitives = None, hexstr: HexStr = None, text: str = None
    ) -> HexStr:
        return to_hex(primitive, hexstr, text)

    @staticmethod
    @wraps(to_json)
    def toJSON(obj: Dict[Any, Any]) -> str:
        return to_json(obj)
