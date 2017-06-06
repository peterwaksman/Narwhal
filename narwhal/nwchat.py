from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *


"""
This defines the ChatNode base class and the ChatManager that
manages a system of multiple ChatNodes.
"""

class ChatNode():
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

    def readSlotEvents(nar, segment):
        return recordSlotEvents(nar,segment) 

    def getIBest(self):
        ibest = -1
        max = 0.0
        for i in range(len(self.nreaders)):
            N = self.nreaders[i]
            v = N.vault.maxGOF()
            if max < v:
                max = v
                ibest = i
        return ibest

  
    def read( self, segment, tokens ):
        """basic read method, do not call directly. Use respond() """
        for N in self.nreaders:
            N.readText(segment,tokens)
        ibest = self.getIBest()
        return ibest


    #----Typically the next two methods get overriden in derived classes

    def getContext(self):
        ibest = self.ibest
        return str(ibest)
  
    def respond(self, segment, tokens):

        ibest = self.read( segment, tokens)
           
        self.ibest = ibest # set, but also the return value

        if ibest<0:
            self.response = "Sorry, I did not understand."
            return ibest
    
        # For debug
        N = self.nreaders[ibest]   
        s = N.vault.lastConst() 
        h = self.getContext()
        print(h + " " + s)
        #print s
        print("\n")

        return ibest

    def respondText(self, text):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree,tokens)
        self.respond( segment, tokens )
        return self.response

 