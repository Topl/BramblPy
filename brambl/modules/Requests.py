"""
Requests.py
====================================

A Javascript API wrapper module for the Bifrost Protocol.
Currently supports version 4.1 of Bifrost's Brambl-Layer API
Documentation for Brambl-layer is available at https://Requests.docs.topl.co

"""
# Dependencies
import json
import requests
import asyncio
import os
import sys


def BramblRequest(self,routeInfo, params): #obj is meant for the self of request,rename method
    """
    General builder function for formatting API request

    :param routeInfo: object containing data neccesary for making requests
    :param routeInfo['route']: specified request route
    :param routeInfo['method']: request method used
    :param routeInfo['ID']: request id
    :param params: additional request parameters
    :type routeInfo: dictionary
    :type routeInfo['route']: string
    :type routeInfo['method']: string
    :type routeInfo['ID']: string
    :type params: dictionary
    :return: JSON response from the node
    :rtype: JSON

    """
    body = {
        "jsonrpc": "2.0",
        "id": routeInfo['id'],
        "method": routeInfo['method'],
        "params": params
    }
    response = requests.request('POST',self.url+routeInfo['route'], json= body, allow_redirects = True ,headers = self.headers)
    if response.status_code != 200:
        raise Exception('A connection could not be established')
        print(response.status_code())
    return response

class Requests():
    """
    A class for sending requests to the Brambl layer interface of the given chain provider

    :param url: Chain provider location, defaults to "http://localhost:9085/"
    :param apiKey: Access key for authorizing requests to the client API, defaults to "topl_the_world!"
    :type url: string
    :type apiKey: string
    :return: `Requests` object
    :rtype: instance of `Requests`

    """
    #constructor function
    def __init__(self,url = 'http://localhost:9085/', apiKey = 'topl_the_world!'):
        self.url = url
        self.apiKey = apiKey
        self.headers = {
            "Content-Type": "application/json",
             'x-api-key': self.apiKey
        }
    #Allow setting a different url than the default from which to create and accet RPC connections
    def setUrl(self,url):
        self.url = url

    def setApiKey(self,apiKey):
        self.headers['x-api-key'] = apiKey    
    #
    # Wallet Api Routes
    #

    def getBalancesByKey(self,params, ID = '1'):
        """
        Get the balances of a specified public key in the keyfiles directory of the node

        :param params: body parameters passed to the specified json-rpc method
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['publicKeys']
        except:
            raise Exception("A list of publicKeys must be specified")
        
        route = 'wallet/'
        method = 'balances'
        return BramblRequest(self, {'route':route,'method': method,'id':ID},params).text
  
    def listOpenKeyfiles(self, ID = '1'):
        """
        Get a list of all open keyfiles

        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        params = {}
        route = 'wallet/'
        method = 'listOpenKeyfiles'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text


    def generateKeyfile(self,params, ID = '1'):
        """
        Generate a new keyfile in the node keyfile directory

        :param params: body parameters passed to the specified json-rpc method
        :param params['password']: Password for encrypting the new keyfile
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['password']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        if not params:
            raise Exception('A parameter object must be specified')
        if 'password' not in params:
            raise Exception('A password must be provided to encrypt the keyfile')
        route = 'wallet/'
        method = 'generateKeyfile'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def lockKeyfile(self,params, ID = '1'):
        """
        Lock an open keyfile

        :param params: body parameters passed to the specified json-rpc method
        :param params['publicKey']: Base58 encoded public key to get the balance of
        :param params['password']: Password used to encrypt the keyfile
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['publicKey']: string
        :type params['password']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['publicKey']
        except:
            raise Exception("A publicKey field must be specified")

        try:
            params['password']
        except:
            raise Exception("A password must be provided to encrypt the keyfile")

        route = 'wallet/'
        method = 'lockKeyfile'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def unlockKeyfile(self,params, ID = '1'):
        """
        Unlock a keyfile in the node's keyfile directory

        :param params: body parameters passed to the specified json-rpc method
        :param params['publicKey']: Base58 encoded public key to get the balance of
        :param params['password']: Password used to encrypt the keyfile
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['publicKey']: string
        :type params['password']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['publicKey']
        except:
            raise Exception("A publicKey field must be specified")

        try:
            params['password']
        except:
            raise Exception("A password must be provided to encrypt the keyfile")

        route = 'wallet/'
        method = 'unlockKeyfile'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def signTransaction(self,params, ID = '1'):
        """
        Have the node sign a JSON formatted prototype transaction

        :param params: body parameters passed to the specified json-rpc method
        :param params['publicKey']: Base58 encoded public key to get the balance of
        :param params['tx']: a JSON formatted prototype transaction
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['publicKey']: string
        :type params['tx']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['publicKey']
        except:
            raise Exception("A publicKey field must be specified")

        try:
            params['tx']
        except:
            raise Exception("A tx object must be specified")

        route = 'wallet/'
        method = 'signTx'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def broadcastTx(self,params, ID = '1'):
        """
        Have the node sign a `messageToSign` raw transaction

        :param params: body parameters passed to the specified json-rpc method
        :param params['tx']: a JSON formatted transaction (must include signature(s))
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['tx']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['tx']
        except:
            raise Exception("A tx object must be specified")

        route = 'wallet/'
        method = 'broadcastTx'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferPolys(self,params, ID = '1'):
        """
        Transfer Polys to a specified public key.

        :param params: body parameters passed to the specified json-rpc method
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['sender']: Array of public keys which you can use to restrict sending from
        :param params['changeAddress']: Public key you wish to send change back to
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['sender']: list or string
        :type params['changeAddress']: string
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'wallet/'
        method = 'transferPolys'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferArbits(self,params, ID = '1'):
        """
        Transfer Arbits to a specified public key.

        :param params: body parameters passed to the specified json-rpc method
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['sender']: Array of public keys which you can use to restrict sending from
        :param params['changeAddress']: Public key you wish to send change back to
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['sender']: list or string
        :type params['changeAddress']: string
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON
        """
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'wallet/'
        method = 'transferArbits'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text
    #Asset Api Routes

    def createAssets(self,params, ID = '1'):
        """
        Create a new asset on chain

        :param params: body parameters passed to the specified json-rpc method
        :param params['issuer']: Public key of the asset issuer
        :param params['assetCode']: Identifier of the asset
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['issuer']: string
        :type params['assetCode']: string
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['issuer']
        except:
            raise Exception("An asset issuer must be specified")

        try:
            params['assetCode']
        except:
            raise Exception("An assetCode must be specified")
        
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'asset/'
        method = 'createAssets'

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def createAssetsPrototype(self,params, ID = '1'):
        """
        Create a new asset on chain

        :param params: body parameters passed to the specified json-rpc method
        :param params['issuer']: Public key of the asset issuer
        :param params['assetCode']: Identifier of the asset
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['issuer']: string
        :type params['assetCode']: string
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['issuer']
        except:
            raise Exception("An asset issuer must be specified")

        try:
            params['assetCode']
        except:
            raise Exception("An assetCode must be specified")
        
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'asset/'
        method = 'createAssetsPrototype'

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferAssets(self,params, ID = '1'):
        """
        Transfer an asset to a recipient

        :param params: body parameters passed to the specified json-rpc method
        :param params['issuer']: Public key of the asset issuer
        :param params['assetCode']: Identifier of the asset
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['sender']: Array of public keys which you can use to restrict sending from
        :param params['changeAddress']: Public key you wish to send change back to
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['issuer']: string
        :type params['assetCode']: string
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['sender']: list or string
        :type params['changeAddress']: string
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['issuer']
        except:
            raise Exception("An asset issuer must be specified")

        try:
            params['assetCode']
        except:
            raise Exception("An assetCode must be specified")
        
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'asset/'
        method = 'transferAssets'

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferAssetsPrototype(self,params, ID = '1'):
        """
        Transfer an asset to a recipient

        :param params: body parameters passed to the specified json-rpc method
        :param params['issuer']: Public key of the asset issuer
        :param params['assetCode']: Identifier of the asset
        :param params['recipient']: Public key of the transfer recipient
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['sender']: Array of public keys which you can use to restrict sending from
        :param params['changeAddress']: Public key you wish to send change back to
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['issuer']: string
        :type params['assetCode']: string
        :type params['recipient']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['sender']: list or string
        :type params['changeAddress']: string
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['issuer']
        except:
            raise Exception("An asset issuer must be specified")

        try:
            params['assetCode']
        except:
            raise Exception("An assetCode must be specified")
        
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['sender']
        except:
            raise Exception("A sender must be specified")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'asset/'
        method = 'transferAssetsPrototype'

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferTargetAssets(self,params, ID = '1'):
        """
        Transfer a specific asset box to a recipient

        :param params: body parameters passed to the specified json-rpc method
        :param params['recipient']: Public key of the asset recipient
        :param params['assetId']: BoxId of the asset to target
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['recipient']: string
        :type params['assetId']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['assetId']
        except:
            raise Exception("An assetId is required for this request")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")

        route = 'asset/'
        method = 'transferTargetAssets'

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferTargetAssetsPrototype(self,params, ID = '1'):
        """
        Get an unsigned targeted transfer transaction

        :param params: body parameters passed to the specified json-rpc method
        :param params['recipient']: Public key of the asset recipient
        :param params['sender']: Array of public keys of the asset senders
        :param params['assetId']: BoxId of the asset to target
        :param params['amount']: Amount of asset to send
        :param params['fee']: Fee to apply to the transaction
        :param params['data']: Data string which can be associated with this transaction (may be empty)
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['recipient']: string
        :type params['sender']: list or string
        :type params['assetId']: string
        :type params['amount']: number
        :type params['fee']: number
        :type params['data']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['recipient']
        except:
            raise Exception("A recipient must be specified")

        try:
            params['sender']
        except:
            raise Exception("A sender must be specified")

        try:
            params['assetId']
        except:
            raise Exception("An assetId is required for this request")

        try:
            params['amount']
        except:
            raise Exception("An amount must be specified")

        try:
            params['fee']
        except:
            raise Exception("A fee must be specified")

        if params['fee'] != 0:
            raise Exception("A fee must be specified")   

        route = 'asset/'
        method = 'transferTargetAssetsPrototype'     

        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    #NodeView Api Routes
 
    def getTransactionById(self,params, ID = '1'):
        """
        Lookup a transaction from history by the provided id

        :param params: body parameters passed to the specified json-rpc method
        :param params['transactionId']: Unique identifier of the transaction to retrieve
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['transactionId']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        try:
            params['transactionId']
        except:
            raise Exception("A transactionId must be specified")

        route = 'nodeView/'
        method = 'transactionById'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text
        
    def getTransactionFromMempool(self,params, ID = '1'):
        """
        Lookup a transaction from the mempool by the provided id

        :param params: body parameters passed to the specified json-rpc method
        :param params['transactionId']: Unique identifier of the transaction to retrieve
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['transactionId']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """

        try:
            params['transactionId']
        except:
            raise Exception("A transactionId must be specified")

        route = 'nodeView/'
        method = 'transactionFromMempool'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def getMempool(self, ID = '1'):
        """
        Get the balances of a specified public key in the keyfiles directory of the node

        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        params = {}
        route = 'nodeView/'
        method = 'mempool'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def getBlockById(self, params, ID = '1'):
        """
        Lookup a block from history by the provided id

        :param params: body parameters passed to the specified json-rpc method
        :param params['blockId']: Unique identifier of the block to retrieve
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['blockId']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        if not params:
            raise Exception('A parameter object must be specified')
        if 'blockId' not in params:
            raise Exception('A blockId must be specified')
        route = 'nodeView/'
        method = 'blockById'
        Id = '1'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    #Debug Api Routes

    def chainInfo(self, ID = '1'):
        """
        Return the chain information

        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        params = {}
        route = 'debug/'
        method = 'info'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def calcDelay(self,params, ID = '1'):
        """
        Get the average delay between blocks
        :param params: body parameters passed to the specified json-rpc method
        :param params['blockId']: Unique identifier of a block
        :param params['numBlocks']: Number of blocks to consider behind the specified block
        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type params: dictionary
        :type params['blockId']: string
        :type params['numBlocks']: string
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        if not params:
            raise Exception('A parameter object must be specified')
        if 'blockId' not in params:
            raise Exception('A blockId must be specified')
        if 'numBlocks' not in params:
            raise Exception('A number of blocks must be specified')
        route = 'debug/'
        method = 'delay'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def myBlocks(self, ID = '1'):
        """
        Return the number of blocks forged by keys held by this node

        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        params = {}
        route = 'debug/'
        method = 'myBlocks'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def blockGenerators(self, ID = '1'):
        """
        Return the blockIds that each accessible key has forged

        :param ID: identifying number for the json-rpc request, defaults to "1"
        :type ID: string
        :return: json-rpc response from the chain
        :rtype: JSON

        """
        params = {}
        route = 'debug/'
        method = 'generators'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text
