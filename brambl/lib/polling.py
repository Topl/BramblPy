import threading
import asyncio

class pollingTx():
    def __init__(self,requests,txId,options):
        self.requests = requests
        self.txId = txId
        self.options = options
        self.numFailedQueries = 0

    def setInterval(self,func,time):
        e = threading.Event()
        while not e.wait(time):
            func()
    
    async def finalResolve(self):
        numFailedQueries = 0

    async def transactionByIdResolve(self,temp):
        try:
            pass
        except:
            print("Unexepected API response from findTransactionById")
            
    async def ByIdRejection(self):
        try:
            response = await asyncio.wait_for(self.requests.getTransactionFromMempool({'transactionId': self.txId}),timeout=self.options['timeout'])
        except:#reject
            numFailedQueries += 1
            if numFailedQueries >= self.options['maxFailedQuieries']:
                raise Exception('Unable to find the transaction in the mempool')

        await finalResolve()


    async def transactionById(self):
        try:
            response = await asyncio.wait_for(self.requests.getTransactionById({'transactionId': self.txId}),timeout=self.options['timeout'])
        except:#reject
            ByIdRejection()

        await transactionByIdResolve(response)
    
    async def combined(self):
        setInterval(transactionById,self.options['interval'])
    




    
