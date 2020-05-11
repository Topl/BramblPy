
import json
import requests
import asyncio

print('everything is working')
url = "https://valhalla.torus.topl.co/" #temp name, make sure to change and clean

def testfunc():
    print('i am here')


async def BramblRequest(routeInfo, params, obj): #obj is meant for the self of request
    print('this is a placeholder')
    route = routeInfo.route#edit
    



class Requests():

    

    def __init__(self,url,apiKey):
        self.url = url
        self.apiKey = apiKey
        
    payload = {
            "jsonrpc": "2.0",
            "id": "30",
            "method": "info",
            "params": [{}]
        }
    payload = json.dumps(payload)

    def chainInfo(self):
        route = 'debug/'
        response = requests.request('POST',self.url+route, allow_redirects = False, timeout = 5)#temp value
        return response#not presenting correctly

    def paramReq(self):
        route = 'debug/'
        response = requests.request('POST',self.url+route, data = payload, allow_redirects = False, timeout = 5)#temp value
        return response#not presenting correctly 
