import os
import sys
import settings
path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import Requests


b = Requests.Requests()
print(b.chainInfo())



