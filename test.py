import unittest
from runpy import run_path
from HTTPRequest import HTTPRequest
from Connection import Connection
 
class TestSimpleRequests(unittest.TestCase):
    
    def test_importRequest(self):
        req=HTTPRequest("tests/testReq1",isTLS=True,verify=False)
        self.assertEqual(req.command,"GET")
        self.assertEqual(len(req.headers),11)
        req=HTTPRequest("tests/testReqPost1",isTLS=True,verify=True)
        self.assertEqual(req.command,"POST")
        self.assertEqual(len(req.headers),12)
        self.assertTrue("antoine.scemama" in str(req.postBody)) 
        con=Connection(isTLS=True,verify=False,proxies={ 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',})
        req=HTTPRequest("tests/testReqPost1",connection=con)
        self.assertEqual(req.command,"POST")
        self.assertEqual(len(req.headers),12)
        self.assertTrue("antoine.scemama" in str(req.postBody)) 

    def test_sendRequest(self):
        req=HTTPRequest("tests/testReq1",isTLS=True,verify=False)
        req.send()
        self.assertTrue("buildVersion" in req.response.text)
        req=HTTPRequest("tests/testReqPost1",isTLS=True,verify=True)
        req.send()
        self.assertTrue("Brainloop Web" in req.response.text )
        con=Connection(isTLS=True,verify=False)
        req=HTTPRequest("tests/testReqPost1",connection=con)
        req.send()
        self.assertTrue("Brainloop Web" in req.response.text )
        req=HTTPRequest("tests/reqHEAD1",connection=con)
        req.send()
        self.assertTrue(req.response.status_code== 405  )


    def test_sendWithProxy(self):
        con=Connection(isTLS=True,verify=False,proxies={ 'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080',})
        req=HTTPRequest("tests/testReqPost1",connection=con)
        req.send()
        self.assertEqual(req.command,"POST")
        self.assertEqual(len(req.headers),12)
        self.assertTrue("antoine.scemama" in str(req.postBody))


    def test_replaceStringInRequest(self):
        req=HTTPRequest("tests/reqPost2",isTLS=True,verify=False)
        self.assertTrue("antoine.scemama"in str(req.postBody))
        req.replaceString("antoine","yo")
        self.assertTrue("yo.scemama"in str(req.postBody))

    def test_replaceStringInHeader(self):
        req=HTTPRequest("tests/reqPost2",isTLS=True,verify=False)
        req.replaceString("en-US","yo")
        self.assertTrue("yo" in req.headers["Accept-Language"])
        
    def test_replaceStringInURL(self):
        req=HTTPRequest("tests/reqPost2",isTLS=True,verify=False)
        req.replaceString("scope","yo")
        self.assertTrue("yo" in req.URL)




     
 
    
 
 
if __name__ == '__main__':
    unittest.main()