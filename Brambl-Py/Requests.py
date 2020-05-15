
import json
import requests
import asyncio
import os
import sys
import settings
print('everything is working')
url = "https://valhalla.torus.topl.co/" #temp name, make sure to change and clean

'''
General builder function for formatting API request

{dict} routeInfo {route, method,ID}
{object} obj - internal reference for accessing constructor data
returns {object} JSON response from the node
'''
def BramblRequest(routeInfo, params, obj): #obj is meant for the self of request,rename method
    params = json.dumps(params)
    body = {
        "jsonrpc": "2.0",
        "id": routeInfo[2],
        "method": routeInfo[1],
        "params": [params]#should already be a json object
    }
    response = requests.request('POST',obj.url+routeInfo[0], json= body, allow_redirects = True ,headers = obj.headers)
    if response.status_code != 200:
        raise Exception('A connection could not be established')
    return response
'''
A class for sending requests to the Brambl layer interface of the given chain provider

{string} request url
{string} Valhalla API key
'''
class Requests():
    #constructor function
    def __init__(self,url,apiKey):
        self.url = url
        self.apiKey = apiKey
        self.headers = {
            "Content-Type": "application/json",
             'x-api-key': self.apiKey
        }
    #temp showcase of request with params
    def sendParamTest(self,params):
        route = 'debug/'
        method = 'info'
        Id = "1"
        return (BramblRequest([route,method,Id],params,self)).text
        
    def getBalancesByKey(self,params):
        pass

    def listOpenKeyfiles(self):
        params = {}
        route = 'wallet/'
        method = 'listOpenKeyfiles'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def generateKeyfile(self,params):
        if not params:
            raise Exception('A parameter object must be specified')
        if 'password' not in params:
            raise Exception('A password must be provided to encrypt the keyfile')
        route = 'wallet/'
        method = 'generateKeyfile'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def lockKeyfile(self,params):
        pass

    def unlockKeyfile(self,params):
        pass

    def signTransaction(self,params):
        pass

    def broadcastTx(self,params):
        pass

    def transferPolys(self,params):
        pass

    def transferArbits(self,params):
        pass

    def createAssets(self,params):
        pass

    def createAssetsPrototype(self,params):
        pass

    def transferAssets(self,params):
        pass

    def transferAssetsPrototype(self,params):
        pass

    def transferTargetAssets(self,params):
        pass

    def transferTargetAssetsPrototype(self,params):
        pass

    def getTransactionById(self,params):
        pass

    def getTransactionFromMempool(self,params):
        pass

    def getMempool(self):
        params = {}
        route = 'nodeView/'
        method = 'mempool'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def getBlockById(self, params):
        if not params:
            raise Exception('A parameter object must be specified')
        if 'blockId' not in params:
            raise Exception('A blockId must be specified')
        route = 'nodeView/'
        method = 'blockById'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def chainInfo(self):
        params = {}
        route = 'debug/'
        method = 'info'
        Id = "1"
        return BramblRequest([route,method,Id],params,self).text

    def calcDelay(self,params):
        if not params:
            raise Exception('A parameter object must be specified')
        if 'blockId' not in params:
            raise Exception('A blockId must be specified')
        if 'numBlocks' not in params:
            raise Exception('A number of blocks must be specified')
        route = 'debug/'
        method = 'delay'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def myBlocks(self):
        params = {}
        route = 'debug/'
        method = 'myBlocks'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

    def blockGenerators(self):
        params = {}
        route = 'debug/'
        method = 'generators'
        Id = '1'
        return BramblRequest([route,method,Id],params,self).text

