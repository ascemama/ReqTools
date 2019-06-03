from HTTPRequest import HTTPRequest
import re

# A macro is build around a list of requests. The requests will be send one after the other.
class Macro:
    def __init__(self,conn, *args):
        self.macroRequests=[]
        self.connection=conn
        self.instanciateRequests(*args)
        #each rule contain two macroVariables. The first variable replace the second when the macroRule is applied.
        self.macroRules=[]
        #a macroVariable identified a string in one of the macroRequests
        self.macroVariables=[]

    def instanciateRequests(self,*args):
        for req in args:
            self.macroRequests.append(HTTPRequest(req,connection=self.connection))

    def run(self):
        for idx,req in enumerate(self.macroRequests):
            print("send request:",idx)
            req.send()
            self.updateMacroRequests(idx)
            #req.printFields()


    def updateMacroRequests(self, idxOfNextRequest):
        print("updateMacroRequests idx:",idxOfNextRequest)
        relevantRules=self.findMacroRulesForIndex(idxOfNextRequest)
        for rule in relevantRules:
            print("relevantRules.macroVariableFrom.idx:",rule.macroVariableFrom.reqNumber)
            print("relevantRules.macroVariableTo.idx:",rule.macroVariableTo.reqNumber)
            self.applyMacroRule(rule)

    #In construction
    def applyMacroRule(self,rule):
        if(rule.macroVariableFrom.inResponse == True ):
            responseToUseFrom=self.macroRequests[rule.macroVariableFrom.reqNumber].response.text
            pattern="%s(.*)%s" %(rule.macroVariableFrom.delimiterBegin,rule.macroVariableFrom.delimiterEnd)
            txtToCopy=re.search(pattern,responseToUseFrom).group(1)
        else:
            requestToUseFrom=str(self.macroRequests[rule.macroVariableFrom.reqNumber].rfile.getvalue(),'utf-8')
            pattern="%s(.*)%s" %(rule.macroVariableFrom.delimiterBegin,rule.macroVariableFrom.delimiterEnd)
            txtToCopy=re.search(pattern,requestToUseFrom).group(1)
            
        
        requestToUseTo=str(self.macroRequests[rule.macroVariableTo.reqNumber].rfile.getvalue(),'utf-8')
        pattern="%s(.*)%s" %(rule.macroVariableTo.delimiterBegin,rule.macroVariableTo.delimiterEnd)
        txtToDelete=re.search(pattern,requestToUseTo).group(1)

        self.macroRequests[rule.macroVariableTo.reqNumber].replaceString(txtToDelete,txtToCopy)




    def findMacroRulesForIndex(self, idxOfNextRequest):
        relevantRules=[]
        for rule in self.macroRules: 
            if(rule.macroVariableFrom.reqNumber == idxOfNextRequest):
                relevantRules.append(rule)
        return relevantRules


    def addVariable(self,variable):
        #var=MacroVariable(name,reqNumber,inResponse,delimiterBegin,delimiterEnd)
        self.macroVariables.append(variable)
 
    def addRule(self,rule):
        self.macroRules.append(rule)

class MacroVariable:
    def __init__(self,reqNumber,inResponse,delimiterBegin,delimiterEnd):
        self.reqNumber=reqNumber
        self.inResponse=inResponse
        self.delimiterBegin=delimiterBegin
        self.delimiterEnd=delimiterEnd


class MacroRule:
    def __init__(self,macroVariableFrom, macroVariableTo):
        self.macroVariableFrom=macroVariableFrom
        self.macroVariableTo=macroVariableTo
