"""
Brambl.py
====================================
The core module
"""
#D Dependencies
import base58
import asyncio
import json

# Primary sub-modules
from .modules import Requests
from .modules import KeyManager

# Utilities
from .utils import Hash
from .utils import CrypTools

# Libraries
from .lib import polling

# Constants defininitions
validTxMethods = ['createAssetsPrototype','transferAssetsPrototype','transferTargetAssetsPrototype']

class Brambl():
    """
    Each sub-module may be initialized in one of three ways

    1.Providing a separetly initialized Request and KeyManager instance. Each of these instances may be initialized using the 
    static methods `Requests` or `KeyManager` available in the BramblJS class.

    2.Providing custom configuration parameters needed to create new instances of each sub-module with the specified parameters

    3.Providing minimal inputs (i.e. calling Brambl with only a string constructor arguement). This will create new instances of
    the sub-modules with default parameters. KeyManager will create a new keyfile and Requests will target a locally running
    instance of Bifrost.

    :param params: A password string or dictionary containing an instance of `Requests` and `KeyManager`
    :param params['KeyManager']: KeyManager object (may be either an instance or config parameters)
    :param params['KeyManager]['password']: The password used to encrpt the keyfile
    :param params['KeyManager']['instance']: A previously initialized instance of KeyManager
    :param params['KeyManager']['keyPath']: Path to a keyfile
    :param params['KeyManager']['constansts']: Parameters for encrypting the user's keyfile
    :param params['Requests']: Request object (may be either an instance or config parameters)
    :param params['Requests']['url']: The chain provider to send requests to
    :param params['Requests']['apikey']: Api key for authorizing access to the chain provider.
    :type params: dictionary
    :type params['KeyManager']: `KeyManager` object
    :type params['KeyManager]['password']: string
    :type params['KeyManager']['instance']: `KeyManager` instance
    :type params['KeyManager']['keyPath']: string
    :type params['KeyManager']['constansts']: dictionary
    :type params['Requests']: `Requests` object
    :type params['Requests']['url']: string
    :type params['Requests']['apikey']: string
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
                self.requests = Requests.Requests(self.requestsVar['url'],self.requestsVar['apiKey'])
            except:
                self.requests = Requests.Requests()

        # Setup KeyManager object
        try:
            self.keyManagerVar['password']
        except:
            raise Exception('An encryption password is required to open a keyfile')


        try:
            self.keyManager = self.keyManagerVar['instance']
        except:
            try:
                self.keyManager = KeyManager.KeyManager(self.keyManagerVar['password'],{'keyPath': self.keyManagerVar['keyPath'], 'constants': self.keyManagerVar['constants']})
            except:
                self.keyManager = KeyManager.KeyManager(self.keyManagerVar['password'])
        # Import utilities
        self.utils = Hash
    
    def Requests(testURL="http://localhost:9085/", apiKey="topl_the_world!"):
        """
        Method for creating a separate Requests instance

        :param testURL: Chain provider location, defaults to "http://localhost:9085/" 
        :param apiKey: Access key for authorizing requests to the client API, defaults to "topl_the_world!"
        :type testURL: string
        :type apiKey: string
        :return: `Requests` object
        :rtype: instance of `Requests`
        """
        return Requests.Requests(testURL,apiKey)
        


    
    def KeyManager(password,kwargs=''):
        """ 
        Methods for creating a separate KeyManager instance

        :param password: passwword for encrypting (decrypting) the keyfile
        :param kwargs: Used for importing keyfiles, efault emptry string
        :type password: string
        :type kwargs: string or dictionary
        :return: `KeyManager` object
        :rtype: instance of `KeyManager`

        """
        return KeyManager.KeyManager(password,kwargs)


    async def addSigToTx(self,prototypeTx, userKeys):
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
        def getSig(keys,txBytes):
            fromEntries = {}
            for key in keys:
                fromEntries[key.pk] = base58.b58encode(key.sign(txBytes))
            return fromEntries
        # incase a single given is given not as an array
        keys = []
        if type(userKeys) != type(['list']):
            keys.append(userKeys)
        else:
            keys = userKeys

        # add signatures of all given key files to the formatted transaction
        prototypeTxDic = json.loads(prototypeTx)
        tempDic = {}
        for key in prototypeTxDic['formattedTx']:
            tempDic[key] =  prototypeTxDic['formattedTx'][key]

        tempDic['signatures'] = getSig(keys,base58.b58decode(prototypeTxDic['messageToSign']))
        return json.dumps(tempDic)
    
    
    async def signAndBroadcast(self, prototypeTx):
        """
        Used to sign a prototype transaction and broadcast to a chain provider
        :param prototypeTx: An unsigned transaction JSON object
        :type prototypeTx: ? 
        :return: broadcastTx Request
        :rtype: JSON 

        """
        #may return dictionary?
        formattedTx = self.addSigToTx(prototypeTx,self.keyManager)
        return self.requests.broadcastTx({'tx':formattedTx})

    
    async def transaction(self,method,params):
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

    async def pollTx(self, txId,options={ 'timeout': 90, 'interval': 3, 'maxFailedQueries': 10 }):
        """
        A function to initiate polling of the chain provider for a specified transaction.
        This function begins by querying 'getTransactionById' which looks for confirmed transactions only.
        If the transaction is not confirmed, the mempool is checked using 'getTransactionFromMemPool' to
        ensure that the transaction is pending. The parameter 'numFailedQueries' specifies the number of consecutive
        failures (when resorting to querying the mempool) before ending the polling operation prematurely.
        
        :param txId: The unique transaction ID to look for
        :param options: Optional parameters in dictionary to control the polling behavior
        :param options['timeout']: The timeout (in seconds) before the polling operation is stopped
        :param options['interval']: The interval (in seconds) between attempts
        :param options['maxFailedQueries']: The maximum number of consecutive failures (to find the unconfirmed transaction) before ending the poll execution
        :type txId: type description
        :type options: type description
        :type options['timeout']: number
        :type options['interval']: number
        :type options['maxFailedQueries']: number
        :return: polling request
        :rtype: JSON

        """
        temp = polling.pollingTx(self.requests,txId,options)
        return temp.combined()
