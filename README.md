# LokiPy
A Python API wrapper to communicate with the Topl blockchain via requests made using the requests module. (Recommended for use with Python 3.x)

# Installation & Usage
To install from pip run "pip install LokiPy" in your project directory<br/><br/>

Create an instance of LokiPy in your Python application by using:<br/>
* from LokiPy import Requests;<br/><br/>
Most of the functions return jsons loaded from requests made using the requests module. Example usage: <br/>
* LokiObj = Requests.LokiPy();<br/>
* print(LokiObj.getMempool());<br/><br/>

Getting a response once a transaction is confirmed and included in a block:<br/>
* LokiObj.createAssets(issuer="6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", recipient="6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", amount=10, assetCode="testAssets", fee=0, data="", onConfirm = True, interval = 3, repeats = 3); <br/>

Setting the 'onConfirm' field to be True in certain requests (those that generate transactions) returns a response once that transaction is confirmed and included in a block instead of once it is created and sent to the mempool. The 'interval' parameter can be defined to specify the interval in seconds before repeating the findTransactionById request contained within the function and the 'repeats' field can be defined to specify the number of times the findTransactionById request should be repeated at the specified interval. Both these fields assume a default value of 3 if not explicitly specified. Leaving out these 3 fields initiates a transaction without awaiting confirmation.<br/>

The following methods extend the onConfirm functionality:<br/>
* createAssets<br/>
* transferAssets<br/>
* transferPolys<br/>
* transferArbits<br/>
* transferArbitsByPublicKey<br/><br/>

See the Requests.py file for various other methods that can be invoked by your LokiPy instance to communicate with the Topl blockchain.


# Api-Key protection
To api-key protect your node and requests follow these steps:<br/>
1. Choose an api-key (some string)<br/>
2. Find the Blake2b256 hash of this string (can be found using the blakeHash function in this module)<br/>
3. Set the "apiKeyHash" field in the settings file of your node to be the blakeHash of your chosen api-key as found in the previous step<br/>
4. Use the setApiKey function in this module to set your chosen api-key for all requests made using a LokiJS instance in your application<br/>

# License
LokiJS is licensed under the
[Open Software License v. 3.0 (OSL-3.0)](https://opensource.org/licenses/OSL-3.0), also included
in our repository in the `LICENSE` file.
