from http.server import BaseHTTPRequestHandler
import http.cookies
from io import BytesIO, StringIO
import Connection
import requests
import http.cookies
import re




#HTTP request class derived from BaseHTTPRequestHandler
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, reqFile=None, **kwargs):
        self.regexContentLengthPattern=re.compile(r"\s*[c|C]ontent-[l|L]ength:\s*([0-9]+)\s*")
        self.session = kwargs.get('session',None)
        if self.session == None:
            self.session = requests.Session()
        self.instanciateConnection(**kwargs)
        if reqFile !=None:
            with open(reqFile, 'rb') as requestFile:
                self.updateRequestFromRawValue(requestFile.read())
 
    #instanciate the request from raw
    def updateRequestFromRawValue(self,raw):
        self.rfile=BytesIO(raw)
        self.raw_requestline=self.rfile.readline()
        #self.raw_requestline=requestFile.readline()
        self.error_code = self.error_message = None
        #from BaseHTTPRequesetHandler class
        self.parse_request()
        #the above function does not parse request body
        self.parseRequestBody()
        #transfer cookies (from requestFile) from header to Cookie param
        self.parseCookiesFromHeaders()
        #response filled later
        self.response=None
        self.addURLToRequest()

    def instanciateConnection(self,**kwargs):
        self.connection=Connection.Connection(**kwargs)

    def printFields(self):
        print("Error Code: ",self.error_code)       # None  (check this first)
        print("Command: ",self.command)      # "GET"
        print("Path: ",self.path)             # "/who/ken/trust.html"
        #print self.request_version  # "HTTP/1.1"
        print("Nb of Headers: ",len(self.headers))     # 3
        print("Header keys: ", self.headers.keys())   # ['accept-charset', 'host', 'accept']
        print("URL: ",self.URL)
        print(self.cookies.output(attrs=[], header="Cookie:"))
        if self.command=="POST":
            print("Post body.:",self.postBody)
        print("rfile:",self.rfile.getvalue())
        
    # create the URL from host, path and protocol    
    def addURLToRequest(self):
        url=self.headers['host']+self.path
        if self.connection.isTLS:
            url="https://"+url
        else:
            url="http://"+url
        
        self.URL=url

    def parseRequestBody(self):
        if 'content-length' in self.headers.keys():   
            content_len = int(self.headers['content-length'], 0)
            self.postBody = self.rfile.read(content_len)
        elif 'Content-Length' in self.headers.keys() :
            content_len = int(self.headers['Content-Length'], 0)
            self.postBody = self.rfile.read(content_len)
        else:
            self.postBody=None
    
    def updateContentLengthInRawReq(self,newLength):
        if  self.command == "POST":
            #return to the beginning
            self.rfile.seek(0)
            #the first line contain the command
            self.rfile.readline()
            while True:
                line=str(self.rfile.readline(),'utf-8')
                if not line:
                    break
                pattern=self.regexContentLengthPattern.search(line)
                if pattern:
                    raw=str(self.rfile.getvalue(),'utf-8').replace(pattern.string,"content-length: "+str(newLength)+" \r\n")
                    self.updateRequestFromRawValue(bytes(raw,'utf-8'))
                    break
    
    def getContentLengthInRawReq(self):
        if  self.command == "POST":
            #return to the beginning
            self.rfile.seek(0)
            #the first line contain the command
            self.rfile.readline()
            while True:
                line=str(self.rfile.readline(),'utf-8')
                if not line:
                    break
                pattern=self.regexContentLengthPattern.search(line)
                if pattern:
                    return int(pattern.group(1))



    def parseCookiesFromHeaders(self):
        #add to the cookie param
        self.cookies=http.cookies.SimpleCookie()
        if 'cookie' in self.headers.keys():    
            self.cookies.load('Cookie: '+self.headers['cookie'])
            #remove the cookie from the (normal) header
            del self.headers['cookie']
        if 'Cookie' in self.headers.keys():
            self.cookies.load('Cookie: '+self.headers['Cookie'])
            del self.headers['Cookie']

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

    #to be optimized later (the whole request is put to memory then replace then re-write, not so efficient)
    def replaceString(self,strToBeDel,strToBePst):
        if strToBeDel in str(self.rfile.getvalue(),'utf-8'):
            strng=str(self.rfile.getvalue(),'utf-8').replace(strToBeDel,strToBePst)
            self.updateRequestFromRawValue(bytes(strng,'utf-8'))
            previousContLeng=self.getContentLengthInRawReq()
            #for now only utf-8 is supported, so the length should be in bytes here.
            delta=len(strToBePst)-len(strToBeDel)
            self.updateContentLengthInRawReq(previousContLeng+delta)
             
        

    def send(self):
        #cookies must be formatted for Requests lib
        cookies = {}
        for key, morsel in self.cookies.items():
            cookies[key] = morsel.value
        
        if self.command == "GET":
            self.response=self.session.get(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert) 
        if self.command == "POST":
            self.response=self.session.post(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
        if self.command == "HEAD":
            self.response=self.session.head(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
        if self.command == "PUT":
            self.response=self.session.put(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
        if self.command == "DELETE":
            self.response=self.session.delete(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 

        self.elapsed=self.response.elapsed.total_seconds()
#   """   def sendGet(self,cookies=None):
#         self.response=self.session.get(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert) 
#         print("response: ",self.response.text)
    
#     def sendPost(self,cookies=None):
#         self.response=self.session.post(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
#         print("response: ",self.response.text)
    
#     def sendHead(self,cookies=None):
#         self.response=self.session.head(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
#         print("response: ",self.response.text)
    
#     def sendPut(self,cookies=None):
#         self.response=self.session.head(self.URL,headers=self.headers,proxies=self.connection.proxies,cookies=cookies, verify=self.connection.verifyTLSCert,data=self.postBody) 
#         print("response: ",self.response.text)

#  """


 


