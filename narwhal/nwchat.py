from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *

strAPOLOGY = "Sorry, I did not understand that."
"""
This defines the NWChatnode base class and the ChatManager that
manages a system of multiple NWChatnodes.
"""

class NWChatnode():
    def __init__(self,treeroot, nars, cals = []):
        self.tree = treeroot.copy()
        self.nreaders = []
        i = 0
        for nar in nars:
            if len(cals)==0:
                self.nreaders.append( NWNReader( nar, False) )
            else:
                self.nreaders.append( NWNReader( nar, cals[i] ))
                i += 1
    
        self.ibest = -1
        self.response = ""
        self.maxGOF = 0.0


    def bestFitI(self):
        ibest = -1
        max = 0.0
        for i in range(len(self.nreaders)):
            N = self.nreaders[i]
            v = N.vault.maxGOF()
            if max < v:
                max = v
                ibest = i

        self.maxGOF = max

        return ibest

  
    def readAll( self, segment, tokens ):
        """basic read method, do not call directly. Use respond() """
        for N in self.nreaders:
            N.readText(segment,tokens)
   

    #----Typically the next two methods get overriden in derived classe
    def getContext(self):
        ibest = self.ibest
        return str(ibest)
  
    def read(self, segment, tokens):
 
        self.readAll( segment, tokens)# does the read
 
        self.ibest = self.bestFitI() # collects the GOFs

        ibest = self.ibest
        if ibest<0:
            self.response = strAPOLOGY
            return ibest
    
        # For debug
        N = self.nreaders[ibest]   
        s = N.vault.lastConst() 
        h = self.getContext()
        print(h + " " + s)
        print("\n")
        return ibest

    def respondText(self, text):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree,tokens)
        self.read( segment, tokens )
        return self.response

 