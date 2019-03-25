import Requests
import json

def printJson(jsonData):
    print(json.dumps(jsonData, indent = 4));

print("------------- LokiPy tests ----------------")
LokiObj = Requests.LokiPy();
LokiObj.setApiKey('test_key');

print("");
print(">>>>>>>>>>>>>>>>>>>>>> Wallet Api Route");
print("-----------------------------");
print("getBalancesByKey result:");
printJson(LokiObj.getBalancesByKey("A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb"));

print("-----------------------------");
print("getOpenKeyfiles result:");
printJson(LokiObj.getOpenKeyfiles());

print("-----------------------------");
print("generateKeyfile result:");
printJson(LokiObj.generateKeyfile("password"));

print("-----------------------------");
print("lockKeyfile result:");
printJson(LokiObj.unlockKeyfile("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "genesis"));

print("-----------------------------");
print("unlockKeyfile result:");
printJson(LokiObj.lockKeyfile("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "genesis"));

print("-----------------------------");
print("transferArbits result:");
printJson(LokiObj.transferArbits('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, ''));

print("-----------------------------");
print("transferArbitsByPublicKey result:");
printJson(LokiObj.transferArbitsByPublicKey('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, ''));

print("-----------------------------");
print("transferArbitsByPublicKey result:");
printJson(LokiObj.transferArbitsByPublicKey('A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb', 1, 0, '', publicKeysToSendFrom=['6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ'], publicKeyToSendChangeTo='6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ'));

print("")
print(">>>>>>>>>>>>>>>>>>>>>> Asset Api Route");
print("-----------------------------");
print("createAssets result:")
printJson(LokiObj.createAssets("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", 10, "testAssets", 0, ""));

print("-----------------------------");
print("transferAssets result:")
printJson(LokiObj.transferAssets("6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", "A9vRt6hw7w4c7b4qEkQHYptpqBGpKM5MGoXyrkGCbrfb", 10, "testAssets", 0, ""));

print("")
print(">>>>>>>>>>>>>>>>>>>>>> NodeView Api Route");
print("-----------------------------");
print("getTransactionFromMempool result:")
printJson(LokiObj.getTransactionById("GkDKSPNbRPPVVRbPPfJy4UiZonVR1AANdJhVGARj6WPB"));

print("")
print(">>>>>>>>>>>>>>>>>>>>>> Debug Api Route");
print("-----------------------------");
print("chainInfo result:")
printJson(LokiObj.chainInfo());


print("-----------------------------");
print("blockGenerators result:")
printJson(LokiObj.blockGenerators());

print("-----------------------------");
print("printChain result:")
printJson(LokiObj.printChain());

print("");
print(">>>>>>>>>>>>>>>>>>>>>> Utils Api Route");
print("-----------------------------");
print("seed result:");
print(LokiObj.seed(32));

print("-----------------------------");
print("blakeHash result:");
print(LokiObj.blakeHash("Hello World"));

print("-----------------------------");
print("test_key hash result:");
print(LokiObj.blakeHash("test_key"));
