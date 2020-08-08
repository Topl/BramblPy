# Brambl-Py
A Python API wrapper to communicate with the Topl blockchain via requests made using the requests module. (Recommended for use with Python 3.x)

# Installation & Usage
To install from pip run "pip install brambl" in your project directory<br/>

----------------------------------------------------------------------<br/>

Create an instance of Brambl-Py in your Python application by using:<br/>
* from brambl import Brambl;<br/><br/>

Create an instance of the Requests module in your Python application by using:<br/>
* from brambl.modules import Requests

Create an instance of the KeyManager module in your Python application by using:<br/>
* from brambl.modules import KeyManager

Most of the functions return jsons loaded from requests made using the requests module. Example usage:<br/>
* from brambl.modules import Requests
* BramblObj = Requests.Requests();<br/>
* print(BramblObj.getMempool());<br/>

----------------------------------------------------------------------<br/>

Getting a response once a transaction is confirmed and included in a block:<br/>
* BramblObj.createAssets({'issuer': "6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", 'assetCode': "testAssets", 'recipient': "6sYyiTguyQ455w2dGEaNbrwkAWAEYV1Zk6FtZMknWDKQ", 'amount': 10, 'fee': 0, 'data': ""}); <br/>

Setting the 'onConfirm' field to be True in certain requests (those that generate transactions) returns a response once that transaction is confirmed and included in a block instead of once it is created and sent to the mempool. The 'interval' parameter can be defined to specify the interval in seconds before repeating the findTransactionById request contained within the function and the 'repeats' field can be defined to specify the number of times the findTransactionById request should be repeated at the specified interval. Both these fields assume a default value of 3 if not explicitly specified. Leaving out these 3 fields initiates a transaction without awaiting confirmation.<br/>

The following methods extend the onConfirm functionality:<br/>
* createAssets<br/>
* transferAssets<br/>
* transferPolys<br/>
* transferArbits<br/>
* transferArbitsByPublicKey<br/>

----------------------------------------------------------------------<br/>

See the Requests.py file for various other methods that can be invoked by your Brambl-Py instance to communicate with the Topl blockchain.


# Api-Key protection
To api-key protect your node and requests follow these steps:<br/>
1. Choose an api-key (some string)<br/>
2. Find the Blake2b256 hash of this string (can be found using the blakeHash function in this module)<br/>
3. Set the "apiKeyHash" field in the settings file of your node to be the blakeHash of your chosen api-key as found in the previous step<br/>
4. Use the setApiKey function in this module to set your chosen api-key for all requests made using a Brambl-Py instance in your application<br/>

# License
Brambl-Py is licensed under the
[Mozilla Public License version 2.0 (MPL 2.0)](https://www.mozilla.org/en-US/MPL/2.0), also included
in our repository in the `LICENSE` file.
