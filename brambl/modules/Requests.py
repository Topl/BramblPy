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
        "params": [params]#should already be a json object
    }
    response = requests.request('POST',self.url+routeInfo['route'], json= body, allow_redirects = True ,headers = self.headers)
    if response.status_code != 200:
        raise Exception('A connection could not be established')
        pirnt(response.status_code())
    return response
'''
A class for sending requests to the Brambl layer interface of the given chain provider

{string} request url
{string} Valhalla API key
'''
class Requests():
    #constructor function
    def __init__(self,url = 'http://localhost:9085', apiKey = 'topl_the_world!'):
        self.url = url
        self.apiKey = apiKey
        self.headers = {
            "Content-Type": "application/json",
             'x-api-key': self.apiKey
        }


    #temp showcase of request with params
    def sendParamTest(self,params, ID = '1'):
        route = 'debug/'
        method = 'info'
        return BramblRequest(self,{'route':route,'method': method,'id':ID},params).text
        
    def getBalancesByKey(self,params, ID = '1'):
        pass

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
        pass

    def unlockKeyfile(self,params, ID = '1'):
        pass

    def signTransaction(self,params, ID = '1'):
        pass

    def broadcastTx(self,params, ID = '1'):
        pass

    def transferPolys(self,params, ID = '1'):
        pass

    def transferArbits(self,params, ID = '1'):
        pass

    def createAssets(self,params, ID = '1'):
        pass

    def createAssetsPrototype(self,params, ID = '1'):
        pass

    def transferAssets(self,params, ID = '1'):
        pass

    def transferAssetsPrototype(self,params, ID = '1'):
        pass

    def transferTargetAssets(self,params, ID = '1'):
        pass

    def transferTargetAssetsPrototype(self,params, ID = '1'):
        pass

    def getTransactionById(self,params, ID = '1'):
        pass

    def getTransactionFromMempool(self,params, ID = '1'):
        pass

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

