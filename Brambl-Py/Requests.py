
import json
import requests
import asyncio
import os
import sys
import settings
print('everything is working')
url = "https://valhalla.torus.topl.co/" #temp name, make sure to change and clean

def testfunc():
    print('i am here')

'''routeInfo = [route, method,ID]'''
def BramblRequest(method,routeInfo, params, obj): #obj is meant for the self of request,rename method
    body = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "info",
            "params": [{}]
        }
    response = requests.request(str(method).upper(),obj.url+routeInfo[0], json= body, allow_redirects = True,headers = obj.headers)
    return response


class Requests():
    def __init__(self,url,apiKey):
        self.url = url
        self.apiKey = apiKey
        self.headers = {
            "Content-Type": "application/json",
             'x-api-key': self.apiKey
        }

        

    def chainInfo(self):
        params = {}
        route = 'debug/'
        method = 'info'
        Id = "1"
        connectMethod = 'POST'
        return BramblRequest(connectMethod,[route,method,Id],params,self)
    
    def sendParam(self,params):
        params = json.dumps(params)
        route = 'debug/'
        method = 'info'
        Id = "1"
        connectMethod = 'POST'
        return BramblRequest(connectMethod,[route,method,Id],params,self)



b = Requests(url,os.getenv('VALHALLA_KEY'))

x = b.chainInfo()
print(x.text)


y = b.sendParam({'Test':'qwert','test2':'ewrwe'})
print(y.text)




