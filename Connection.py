import json

class Connection:
    def __init__(self, **kwargs):
        #a connection object was passed as argument
        if 'connection' in kwargs:
            self.instanciateConnectionFromConnectionObject(**kwargs)
        #connection parameters passed separately
        else:
            self.verifyTLSCert=kwargs.get('verify',True)
            self.proxies= kwargs.get('proxies',None)
            self.isTLS=kwargs.get('isTLS',True)

    @staticmethod
    def getConnection(**kwargs):
        return Connection(kwargs)


    def instanciateConnectionFromConnectionObject(self,**kwargs):
        con=kwargs.get('connection')
        self.isTLS=con.isTLS
        self.verifyTLSCert=con.verifyTLSCert
        self.proxies=con.proxies