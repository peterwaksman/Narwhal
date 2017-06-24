from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *

strAPOLOGY = "Sorry, I did not understand that."
strINFO = "Here is an link article about"
"""
This defines the NWChatnode base class and the ChatManager that
manages a system of multiple NWChatnodes.
"""

class NWResponder():
    def __init__(self):
        self.node = None

    def respond(self, text):
        s = self.node.respondText(text)
        if self.node.pending:
            s = self.node.respondText('')
        return s

    def getContext(self):
        s = self.node.getContext()
        return s

######################################

class NWChatnode():
    def __init__(self, treeroot, nars, cals = []):
        self.tree = treeroot.copy()
        self.nreaders = []
        i = 0
        for nar in nars:
            if len(cals)==0:
                self.nreaders.append( NWNReader( nar, False) )
            else:
                self.nreaders.append( NWNReader( nar, cals[i] ))
                i += 1
    
        self.ibest = -1    # index of bet fit narrative
        self.maxGOF = 0.0  # goodness of fit
        self.response = "" # what chatbot says back

        self.responder = None # needs to be set externally
        #self.responder = self # who currently answers questions

        self.parent = self # sub classes may take a parent CTOR argument
                           # it is used to return control
        self.lastConst = ""

        self.pending = False

    def updatePending(self):
        self.pending = False

    def bestFitI(self):
        ibest = -1
        max = 0.0
        lastConst = ""
        for i in range(len(self.nreaders)):
            N = self.nreaders[i]
            v = N.vault.maxGOF()
            if max < v:
                max = v
                ibest = i
                lastConst = N.vault.lastConst()

        self.maxGOF = max
        self.lastConst = lastConst
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
        #print("\n")
        return ibest


    def respondText(self, text):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree,tokens)
        self.read( segment, tokens )
        return self.response

   # if you cannot do this at construction, do it later
   # it does not change the responder, just this instance
    def setParentAndResponder(self, parent, responder):
        self.parent = parent        
        self.responder = responder  
 
    def getResponder(self):
        return self.responder

    def restoreParentControl(self):
        self.responder.node = self.parent  


class NWDatanode():
    def __init__(self, id, treeroot, nar, cal=False):
        self.id = id

        self.tree = treeroot.copy()
        self.nar = nar # convenient to use outside the reader
        self.reader = NWNReader( nar, cal )

        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''
        self.eventGOF = 0.0

    def clear(self):
        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''

    def read( self, text ):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree, tokens) #not efficient, could do this at higher level,

        self.clear()

        # look for structured data
        self.eventrecord = recordSlotEvents( self.nar, segment )
        self.eventGOF = maxEventGOF( self.eventrecord )

        # freeform read
        self.nar.clear()
        self.reader.readText(segment,tokens)
        self.GOF = self.reader.vault.maxGOF()
        self.lastConst = self.reader.vault.lastConst

    def getEvents(self):
        out = ''
        for event in self.eventrecord:
            out += event[1] + ", "
        return out
