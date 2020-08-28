# Brambl-Py
A Python API wrapper to communicate with the Topl blockchain via requests made using the requests module. (Recommended for use with Python 3.x)

# Installation & Usage
To install from pip run "pip install brambl-py" in your project directory<br/>

----------------------------------------------------------------------<br/>

Create an instance of Brambl-Py in your Python application by using:<br/>
* from brambl import Brambl;<br/><br/>

Create an instance of the Requests module in your Python application by using:<br/>
* from brambl.modules import Requests

Create an instance of the KeyManager module in your Python application by using:<br/>
* from brambl.modules import KeyManager

Most of the functions are contained within the Brambl module. Example usage:<br/>
* from brambl.Brambl import Brambl
* BramblObj = Brambl("password");<br/>
* print(BramblObj.requests.getMempool());<br/>

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


# License
Brambl-Py is licensed under the
[Mozilla Public License version 2.0 (MPL 2.0)](https://www.mozilla.org/en-US/MPL/2.0), also included
in our repository in the `LICENSE` file.
