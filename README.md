# ReqTools

is a python library which makes it easier to send complex HTTP requests. It is intended to simplify the life of security testers when tools like Burp can't help:
* it enables to import HTTP request coming from file (e.g. via Burp *copy to file* feature)
* it enable to easily configure the request to be send to a proxy
* it enable to easily change/replace HTTP request feature from both requests and responses
* it enables to define Macro, i.e. series of requests whereby the content of former requests or response influence the content of the current request being sent. Macro are a very powerfull Burp feature, however this feature in Burp also has some limitations that can be overcome with this library.


This library works with python3 and is mostly based on _Requests_ and _BassHTTPRequestHandler_ classes. 

## Examples
#### Import request from file, replace string value in request and send.

```python
from HTTPRequest import HTTPRequest
from Connection import Connection

req=HTTPRequest("./PATH/TO/REQUEST")
req.replaceString("String to be replaced" ,"Replacement string")
req.printFields()
req.send()
print(req.response.headers)
```
 
#### Import request from file and send (via HTTPS) it via a proxy without checking TLS certificate

```python
from HTTPRequest import HTTPRequest
from Connection import Connection

req=HTTPRequest("./PATH/TO/REQUEST",isTLS=True,proxies = { 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',},verify=False)
req.send()
print("time to process",req.elapsed)
```



#### Two requests send with the same connection (proxy) configuration

```python
from HTTPRequest import HTTPRequest
from Connection import Connection

con=Connection(isTLS=True,verify=False,proxies={ 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',})
req1=HTTPRequest("reqLoginBLNET1",connection=con)
req2=HTTPRequest("reqLoginBLNET2",connection=con)
req1.send()
req2.send()
```

## Working with Macros

* A macro contains an ordered set of requests that will be sent sequentially via run(). 
* Rules can be defined and added to a macro, they define how a string contained in one request or its (already received) response will be automatically added to request that will be send. 
* As an example we could define a macro with two requests: `request1` and `request2` (that will be sent in this order). If  `response1` (the response to request1) contains a sessionID in some header we can create a rule, such that this sessionID header get pasted to `request2`. This could then simulate automatic login.
* In order to define the string that needs to be used, we define a Macro variable. it defines, in a specific request and via a simple regex (the string contains between two other strings) the string that we are interested in (e.g. the sessionID in the previous example)
* A macro rule is then composed of two macro variable. The first one will replace the second one, when the macro is run().

#### Define a macro with two request

```python
from HTTPRequest import HTTPRequest
from Connection import Connection

con=Connection(isTLS=True,verify=False,proxies={ 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',})
macro=Macro(con, "reqLoginBLNET1", "reqLoginBLNET2")
var1=MacroVariable(0,True,"h=","\", \"") #MacroVariable(Request_Number, FromResponse? (otherwise from request), Regex_Begin_String, Regex_End_String)
var2=MacroVariable(1,False,"h=", " HTTP")
rule1=MacroRule(var1,var2)
macro.addRule(rule1)
macro.run()
print(req1.response.headers)
```