import sys
import os
import pathlib
import base58
import asyncio

path = os.getcwd() + '/brambl/modules/'
sys.path.insert(1,path)

import Requests
import KeyManager

path = os.getcwd() + '/brambl/utils/'
sys.path.insert(1,path)

import Hash
import CrypTools

path = os.getcwd() + '/brambl/lib/'
sys.path.insert(1,path)

import polling

validTxMethods = [
    'createAssetsPrototype',
    'transferAssetsPrototype',
    'transferTargetAssetsPrototype'
]


class Brambl():

    def __init__(self, params={}):
        try:
            self.keyManagerVar = params['KeyManager']
        except:
            self.keyManagerVar = {}

        try:
            self.requestsVar = params['Requests']
        except:
            self.requestsVar = {}


        if type(params) == type('string'):
            self.keyManagerVar['password'] = params

        try:
            self.requests = requestsVar['instance']
        except:
            try:
                self.requests = Requests.Requests(requestsVar['url'],requestsVar['apiKey'])
            except:
                self.requests = Requests.Requests()


        try:
            keyManagerVar['password']
        except:
            raise Exception('An encryption password is required to open a keyfile')


        try:
            self.keyManager = keyManagerVar['instance']
        except:
            try:
                self.keyManager = KeyManager.KeyManager(keyManagerVar['password'],{'keyPath': keyManagerVar['keyPath'], 'constants': keyManagerVar['constants']})
            except:
                self.keyManager = KeyManager.KeyManager(keyManagerVar['password'])

        self.utils = Hash

    async def addSigToTx(prototypeTx, userKeys):
        def getSig(keys,txBytes):
            fromEntries = {}
            for key in keys:
                fromEntries[key.pk] = base58.b58encode(key.sign(txBytes))
            return fromEntries

        keys = []
        if type(userKeys) != type(['list']):
            keys.append(userKeys)
        else:
            keys = userKeys

        #TODO add return statement


    async def signAndBroadcast(prototypeTx):
        formattedTx = self.addSigToTx(prototypeTx,self.keyManager)
        return self.requests.broadcastTx({'tx':formattedTx})


    async def transaction(method,params):
        if method not in validTxMethods:
            raise Exception('Invalid transaction method')

        if method == 'createAssetsPrototype':
            return await self.signAndBroadcast(self.requests.createAssetsPrototype(params))
        elif method == 'transferAssetsPrototype':
            return await self.signAndBroadcast(self.requests.transferAssetsPrototype(params))
        elif method == 'transferTargetAssetsPrototype':
            return await self.signAndBroadcast(self.requests.transferTargetAssetsPrototype(params))


    async def pollTx(txId,options={ 'timeout': 90, 'interval': 3, 'maxFailedQueries': 10 }):
        temp = polling.pollingTx(self.requests,txId,options)
        return temp.combined()
