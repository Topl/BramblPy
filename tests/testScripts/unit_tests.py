import os
import sys
import settings
path = os.getcwd() + '/brambl/modules/' #update path once directory rename is sorted
sys.path.insert(1,path)
import Requests

url = "https://valhalla.torus.topl.co/"

b = Requests.Requests(url,os.getenv('VALHALLA_KEY'))
print(b.chainInfo())
