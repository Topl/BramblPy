import Requests
import json

def printJson(jsonData):
    print(json.dumps(jsonData, indent = 4));

print("------------- LokiPy tests ----------------")
LokiObj = Requests.LokiPy();
LokiObj.setApiKey('test_key');

print("-----------------------------")
print("getBalancesByKey result:")
printJson(LokiObj.getBalancesByKey('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb'));

print("-----------------------------")
print("getOpenKeyfiles result:")
printJson(LokiObj.getOpenKeyfiles());

print("-----------------------------")
print("generateKeyfile result:")
printJson(LokiObj.generateKeyfile("password"));

print("-----------------------------")
print("lockKeyfile result:")
printJson(LokiObj.unlockKeyfile("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "genesis"));

print("-----------------------------")
print("unlockKeyfile result:")
printJson(LokiObj.lockKeyfile("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "genesis"));

print("-----------------------------")
print("transferArbits result:")
printJson(LokiObj.transferArbits('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, ''));

print("-----------------------------")
print("transferArbitsByPublicKey result:")
printJson(LokiObj.transferArbitsByPublicKey('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, ''));

print("-----------------------------")
print("transferArbitsByPublicKey result:")
printJson(LokiObj.transferArbitsByPublicKey('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, '', publicKeysToSendFrom=['6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ'], publicKeyToSendChangeTo='6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ'));
