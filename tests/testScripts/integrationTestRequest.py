import unittest
import os
import sys
import json
import pathlib
path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import Requests

class TestIntegrationRequests(unittest.TestCase):
    
    def setUp(self):
        self.brambl = Requests.Requests()#implement check if local node is running

    def testChainInfo(self):
        self.assertEqual(json.loads(self.brambl.chainInfo())['jsonrpc'],'2.0')

    

if __name__ == '__main__':
    unittest.main()

