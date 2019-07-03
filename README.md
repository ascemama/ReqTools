# ReqTools

is a python library which makes it easier to send complex HTTP requests. It is intended to simplify the life of security testers when tools like Burp can't help:
* it enables to import HTTP request coming from file (e.g. via Burp copy to file feature)
* it enable to easily configure the request to be send to a proxy
* it enable to easily change/replace HTTP request feature from both requests and responses
* it enables to define Macro, i.e. series of requests whereby the content of former requests or response influence the content of the current request being sent. Macro are a very powerfull Burp feature, however this feature in Burp also has some limitations that can be overcome with this library.


This library works with python3 and is mostly based on _Requests_ and _BassHTTPRequestHandler_ classes.

Examples

Import request from file, replace string value in request and send.

```python
req=HTTPRequest("./PATH/TO/REQUEST")
req.replaceString("String to be replaced" ,"Replacement string")
req.printFields()
```
 