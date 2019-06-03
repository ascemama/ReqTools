from HTTPRequest import HTTPRequest
from Connection import Connection
import sys
import urllib.parse
import time


cmd=sys.argv[1]
cmd=urllib.parse.quote(cmd)
#print ("Cmd:"+cmd) 
#req=HTTPRequest("/root/Projects/Security/ReqTools/arkham",isTLS=False)
req=HTTPRequest("/root/Projects/Security/ReqTools/arkham",isTLS=False, proxies = { 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',})
req.replaceString("CMD",cmd)
#req.printFields()
#time.sleep(2)
req.send()