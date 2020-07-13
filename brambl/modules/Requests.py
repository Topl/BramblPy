import json
import requests
import asyncio
import os
import sys
url = "https://valhalla.torus.topl.co/" #temp name, make sure to change and clean


'''
General builder function for formatting API request

{dict} routeInfo {route, method,ID}
{object} obj - internal reference for accessing constructor data
returns {object} JSON response from the node
'''
def BramblRequest(self,routeInfo, params): #obj is meant for the self of request,rename method
    params = json.dumps(params)
    body = {
        "jsonrpc": "2.0",
        "id": routeInfo['id'],
        "method": routeInfo['method'],
        "params": [params]
    }
    response = requests.request('POST',self.url+routeInfo['route'], json= body, allow_redirects = True ,headers = self.headers)
    if response.status_code != 200:
        raise Exception('A connection could not be established')
        print(response.status_code())
    return response
'''
A class for sending requests to the Brambl layer interface of the given chain provider

{string} request url
{string} Valhalla API key
'''
class Requests():
    #constructor function
    def __init__(self,url = 'http://localhost:9085/', apiKey = 'topl_the_world!'):
        self.url = url
        self.apiKey = apiKey
        self.headers = {
            "Content-Type": "application/json",
             'x-api-key': self.apiKey
        }
    def setUrl(self,url):
        self.url = url

    def setApiKey(self,apiKey):
        self.headers['x-api-key'] = apiKey    
    
    def getBalancesByKey(self,params, ID = '1'):
        try:#TODO implement list check
            params['publicKeys']
        except:
            raise Exception("A list of publicKeys must be specified")
        
        route = 'wallet/'
        method = 'balances'
        return BramblRequest(self, {'route':route,'method': method,'id':ID},params).text

    def listOpenKeyfiles(self, ID = '1'):
        params = {}
        route = 'wallet/'
        method = 'listOpenKeyfiles'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def generateKeyfile(self,params, ID = '1'):
        if not params:
            raise Exception('A parameter object must be specified')
        if 'password' not in params:
            raise Exception('A password must be provided to encrypt the keyfile')
        route = 'wallet/'
        method = 'generateKeyfile'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def lockKeyfile(self,params, ID = '1'):
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
        try:
            params['tx']
        except:
            raise Exception("A tx object must be specified")

        route = 'wallet/'
        method = 'broadcastTx'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def transferPolys(self,params, ID = '1'):
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

    def createAssets(self,params, ID = '1'):
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

    def getTransactionById(self,params, ID = '1'):
        try:
            params['transactionId']
        except:
            raise Exception("A transactionId must be specified")

        route = 'nodeView/'
        method = 'transactionById'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text
        


    def getTransactionFromMempool(self,params, ID = '1'):
        try:
            params['transactionId']
        except:
            raise Exception("A transactionId must be specified")

        route = 'nodeView/'
        method = 'transactionFromMempool'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def getMempool(self, ID = '1'):
        params = {}
        route = 'nodeView/'
        method = 'mempool'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def getBlockById(self, params, ID = '1'):
        if not params:
            raise Exception('A parameter object must be specified')
        if 'blockId' not in params:
            raise Exception('A blockId must be specified')
        route = 'nodeView/'
        method = 'blockById'
        Id = '1'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def chainInfo(self, ID = '1'):
        params = {}
        route = 'debug/'
        method = 'info'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def calcDelay(self,params, ID = '1'):
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
        params = {}
        route = 'debug/'
        method = 'myBlocks'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

    def blockGenerators(self, ID = '1'):
        params = {}
        route = 'debug/'
        method = 'generators'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text

