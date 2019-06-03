""" import ssl
import http.client
from urllib.parse import urlparse
import re
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO



class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
 

    # def __init__(self):
    #     self.headers={}
    #     self.url=None
    #     self.protocol=None
    #     self.method=None
    #     self.host=None
    #     self.port=80
    #     self.path=None
    #     self.isPortInHostHeader=False
    #     self.isPortInUrl=False
    #     self.isPortInHostHeader=False

    def add_header(self,name,value):
        self.headers[name]=value

    def display_state(self):
        print ("Reqest URL:",self.url)
        print ("Reqest host:",self.host)
        print ("Request port:",self.port)
        print ("Request method:",self.method)
        print ("Request protocol:",self.protocol)
        print("Request headers: ", self.headers)

    def remove_header(self,name):
        del self.headers[name]

    def send_request(self,proxy_port):

        path=self.path
        if self.isPortInUrl:
            path=path+":"+str(self.port)

        if self.isPortInHostHeader:
            self.add_header("Host",self.host+":"+self.port)

        if self.protocol == 'HTTP':
            if proxy_port != 0:
                conn=http.client.HTTPConnection("localhost",proxy_port)
                conn.set_tunnel(self.host+":"+self.port)
            else:
                conn=http.client.HTTPConnection(self.host,self.port)
            conn.request(self.method,path,None,self.headers)
            response=conn.getresponse()
            return response

        elif self.protocol == 'HTTPS':
            ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            conn=http.client.HTTPSConnection(self.host,self.port,context=ssl_context)
            if proxy_port != 0:
                conn=http.client.HTTPSConnection("localhost",proxy_port)
                conn.set_tunnel(self.host+":"+self.port)
            else:
                conn=http.client.HTTPSConnection(self.host,self.port,context=ssl_context)
            conn.request(self.method,path,None,self.headers)
            response=conn.getresponse()
            return response

        return None


    def parse_request_from_file(self, request_file, remove_headers=None):
        with open(request_file,"r") as originalrequest:
            http_request_string=originalrequest.read()
            if remove_headers is None:
                remove_headers=['content-length', 'accept-encoding', 'accept-charset','accept-language', 'accept', 'keep-alive', 'connection', 'pragma','cache-control']
            for i, remove_header in enumerate(remove_headers):
                remove_headers[i] = remove_header.lower()
            if '\n\n' in http_request_string:
                headers, body = http_request_string.split('\n\n',1)
            else:
                headers = http_request_string
                body = None
            headers = headers.split('\n')
            request_line = headers[0]
            headers = headers[1:]
            self.method, rest = request_line.split(" ", 1)
            self.url, protocol = rest.rsplit(" ", 1)
            if re.match('HTTP[^S](.*)',protocol):
                self.protocol='HTTP'
            elif re.match('HTTPS(.*)',protocol):
                self.protocol='HTTPS'
            else:
                fatalError("Unknown protocol for this request")

            if self.url.startswith("http"):
                self.host=urlparse(self.url).hostname
                self.port=urlparse(self.url).port
                self.path=urlparse(self.url).path
            elif self.url.startswith("/"):
                self.path=self.url
                self.isPortInUrl=False
                host=self.find_header_by_name('host',headers)
                if  host:
                    self.host=host
                    self.url = self.protocol.lower()+'://'+host+self.url
                    host=host.split(':')
                    self.host=host[0]
                    if len(host) > 1:
                        self.port=host[1]
                        self.isPortInHostHeader=True
                else:
                    fatalError("Error with the URL, can't find host")
            else:
                fatalError("Protocol not supported. URL must start with http or /")
            for header in headers:
                name, value = header.split(": ", 1)
                if not name.lower() in remove_headers:
                    self.headers[name]=value

    @staticmethod
    def find_header_by_name(header_name,headers):
        for header in headers:
            name, value = header.split(": ", 1)
            if name.lower() == header_name:
                return value
        return None """