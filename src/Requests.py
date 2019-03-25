import requests
import json
import os
import base58
from pyblake2 import blake2b


class LokiPy(object):

    def __init__(self):
        self.url = 'http://localhost:9085/';
        self.defaultAccount = '6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ';
        self.headers = {
            'Content-Type': 'application/json-rpc',
            # 'Accept': 'application/json-rpc',
        };
        self.timeout = 5;

    # set the url to which requests are made
    def setUrl(self, url):
        self.url = url;

    # set the default account for this LokiPy instance
    def setDefaultAccount(self, defaultAccount):
        self.defaultAccount = defaultAccount;

    # set the api key field that should Blake2b256 hash to the apiKeyHash specified in the Bifrost node settings file
    def setApiKey(self, apiKey):
        self.headers = {
            'Content-Type': 'application/json-rpc',
            # 'Accept': 'application/json-rpc',
            'api_key': apiKey
        };

    # set the timeout for requests made using this instance of LokiPy
    def setTimeout(self, timeout):
        self.timeout = timeout;


##########################################################
################# Wallet Api Route #######################
##########################################################

########### getBalances #################

    def getBalances(self):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "balances",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### getBalancesByKey #################

    def getBalancesByKey(self, publicKey):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "balances",
            "params": [{
                "publicKey": publicKey
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### getOpenKeyfiles #################

    def getOpenKeyfiles(self):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "listOpenKeyfiles",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### generateKeyfile #################

    def generateKeyfile(self, password):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "generateKeyfile",
            "params": [{
                "password": password
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### lockKeyfile #################

    def lockKeyfile(self, publicKey, password):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "lockKeyfile",
            "params": [{
                "publicKey": publicKey,
                "password": password
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### unlockKeyfile #################

    def unlockKeyfile(self, publicKey, password):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "unlockKeyfile",
            "params": [{
                "publicKey": publicKey,
                "password": password
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### transferPolys #################

    def transferPolys(self, recipient, amount, fee, data):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "transferPolys",
            "params": [{
                "recipient": recipient,
                "amount": amount,
                "fee": fee,
                "data": data
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### transferArbits #################

    def transferArbits(self, recipient, amount, fee, data):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "transferArbits",
            "params": [{
                "recipient": recipient,
                "amount": amount,
                "fee": fee,
                "data": data
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### transferArbitsByPublicKey #################
# Optional parameters publicKeysToSendFrom and publicKeyToSendChangeTo may be
# specified, publicKeysToSendFrom must be a list of Base 58 encoded string addresses
# and publicKeyToSendChangeTo must be a Base58 encoded string

    def transferArbitsByPublicKey(self, recipient, amount, fee, data, publicKeysToSendFrom = [], publicKeyToSendChangeTo = ''):
        route = 'wallet/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "transferArbits",
            "params": [{
                "recipient": recipient,
                "publicKeysToSendFrom": publicKeysToSendFrom,
                "publicKeyToSendChangeTo": publicKeyToSendChangeTo,
                "amount": amount,
                "fee": fee,
                "data": data
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


##########################################################
################## Asset Api Route #######################
##########################################################

########### createAssets #################

    def createAssets(self, issuer, recipient, amount, assetCode, fee, data):
        route = 'asset/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "createAssets",
            "params": [{
                "issuer": issuer,
                "recipient": recipient,
                "amount": amount,
                "assetCode": assetCode,
                "fee": fee,
                "data": data
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########### transferAssets #################

    def transferAssets(self, issuer, recipient, amount, assetCode, fee, data):
        route = 'asset/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "transferAssets",
            "params": [{
                "issuer": issuer,
                "recipient": recipient,
                "amount": amount,
                "assetCode": assetCode,
                "fee": fee,
                "data": data
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


##########################################################
################# NodeView Api Route #####################
##########################################################

########## getTransactionById ###########

    def getTransactionById(self, transactionId):
        route = 'nodeView/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "transactionById",
            "params": [{
                "transactionId": transactionId
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


########## getTransactionFromMempool ###########

    def getTransactionFromMempool(self, transactionId):
        route = 'nodeView/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "getTransactionFromMempool",
            "params": [{
                "transactionId": transactionId
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


############### getMempool ###############

    def getMempool(self):
        route = 'nodeView/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "mempool",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


############# getBlockById #############

    def getBlockById(self, blockId):
        route = 'nodeView/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "blockById",
            "params": [{
                "blockId": blockId
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


##########################################################
################## Debug Api Route #######################
##########################################################

######### Get chain information #########

    def chainInfo(self):
        route = 'debug/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "info",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


######### Calculate block delay #########

    def calcDelay(self, blockId, numBlocks):
        route = 'debug/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "delay",
            "params": [{
                "blockId": blockId,
                "numBlocks": numBlocks
            }]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


######### Blocks generated by a node's keys #########

    def myBlocks(self):
        route = 'debug/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "myBlocks",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


######### Map block generators to blocks #########

    def blockGenerators(self):
        route = 'debug/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "generators",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


######### Print full chain #########

    def printChain(self):
        route = 'debug/';
        payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "chain",
            "params": [{}]
        };
        response = requests.request('POST', self.url + route, headers = self.headers, data = json.dumps(payload), allow_redirects = False, timeout = self.timeout);
        return json.loads(response.text);


##########################################################
################## Utils Api Route #######################
##########################################################

####### Generate random seed of specified length (default length is 32) #######

    def seed(self, seedLength=32):
        bytes = os.urandom(seedLength);
        return base58.b58encode(bytes).decode("utf-8");


############# Generate Blake2b256 hash of entered string ##############

    def blakeHash(self, message):
        encoded_message = message.encode("utf-8");
        h = blake2b(digest_size=32);
        h.update(encoded_message);
        return base58.b58encode(bytes.fromhex(h.hexdigest())).decode("utf-8");



##########################################################
########### Check if transaction is confirmed ############
##########################################################

# TODO imlement
# def onConfirm(self):
