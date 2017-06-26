from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *

from stdtrees.quantities import QUANTITY

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

    def summary(self):
        g = self.GOF
        k = int(1000*g)
        g = float(k)/1000.0
        if self.nar.polarity==False and g>0:
            g = -g
        e = self.eventGOF
        L = self.getEvents()
        ID = self.id.ljust(15)
        out = ID +  "g=" + str(g).ljust(5) + " " + "    e=" + str(e).ljust(5) + "    events=" + L
        return out


    #######################

def bool32( ):
    array = []
    for i in range(33):
        array.append(False)
    return array
def str32():
    array = []
    for i in range(33):
        array.append('')
    return array


class NWChat():
    def __init__(self, R):
        self.nodes = R

    def read(self, text ):
        for node in R:
            node.read( text )

    def getNode(self, id ):
        for node in self.nodes:
            if node.id==id :
                return node
   


class NBChat( NWChat ):
    def __init__(self, R):
        
        NWChat.__init__(self,R )

        # these should form the backbone of the data
        self.teeth = bool32()

        self.abtmaterial = str32() #will use slot 0 for name without toothnumber

        self.abutmentsOK = False
        self.crownsOK = False

            
    # after a read
    def updateTeeth( self ):
        t = self.getNode('toothno')
        for event in t.eventrecord:
            if event[0]<0.5:
                continue
            if not Value(event[1]):
                continue
            ntooth = int( Value(event[1]) )

            if 0<ntooth and ntooth<33:
                self.teeth[ntooth] = True

    def updateAbutments( self ):
        mkorder = self.getNode('makeorder')

        polarity = mkorder.nar.polarity # can negate an order
          
        for event in mkorder.eventrecord:
            if event[0] >= 0.5:
                r = Relation( event[1] )
                if r=='abutment':
                    self.abutmentsOK = polarity
                elif r=='crown':
                    self.crownsOK = polarity
     
    def updateMaterial( self ):
        getMat = self.getNode('getmaterial') 
        for event in getMat.eventrecord:   
            r = Relation( event[1] )
            v = Value(event[1])
            if event[0]>0.3 :
                if r == 'titanium' or r=='zirconia':
                    self.abtmaterial[0] = r
                if asInt( v ):
                    n = int( asInt(v) )
                    if 0<n and n<33 :
                        self.abtmaterial[0] = r
                        self.abtmaterial[n] = r
        x = 2     
                           
    def updata( self ):
        self.updateTeeth()
        self.updateAbutments()
        self.updateMaterial()
        x = 2

    def respondNext( self ):
        r = ""
        if countBool( self.teeth ) ==0:
            r += "Please enter the tooth numbers"

        elif countStr( self.abtmaterial )==0:
            r += "Do you want titanium or zirconia abutments?"

        elif not self.abutmentsOK : #or crownsOK):
            r += "Do you want abutment for those teeth?"

        else:
            n = countBool( self.teeth )
            mat = self.abtmaterial[0]
            r += "OK, I have got " + str(n) + " unit(s) of " + mat + " on teeth: "
            for i in range(1,len(self.abtmaterial)):
                if self.abtmaterial[i]:
                    r += str(i) + ", "
        return r
            