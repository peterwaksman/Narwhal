from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *
from narwhal.nwcontext import *
from narwhal.nwsegment import *

from narwhal.nwlog import NWLog


from stdtrees.quantities import QUANTITY

strAPOLOGY = "Sorry, I did not understand that."
strINFO = "Here is an link article about"
strDETAILS = "Are there any details you would like to add?"

""" NWTopicReader
 This merges reading from NWNReader and from ReadSlotEvents()
 (only for NARs of order <=1). 

"""
class NWTopicReader():
    def __init__(self, id, treeroot, nar, cal=False):
        self.id = id

        self.tree = treeroot.copy()
        self.nar = nar.copy() # convenient to use outside the reader
        self.reader = NWNReader( self.nar, cal )

        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''
        self.eventGOF = 0.0
        self.lastEvent = None

    def clear(self):
        self.nar.clear()
        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''

        # deprecated
    def read( self, text ):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree, tokens) #not efficient, could do this at higher level,
        self.readSegment( segment, tokens)
   

        # not to be confused with ReadSegment() implemented in nwsegment.py
    def readSegment( self, segment, tokens ):
        self.clear()

        # look for structured data
        self.eventrecord = recordSlotEvents( self.nar, segment )
        if self.eventrecord:
            self.eventGOF = maxEventGOF( self.eventrecord )
        else:
            self.eventGOF = 0.0

        if self.eventGOF>0:
            self.lastEvent = self.eventrecord[ len(self.eventrecord)-1]


        # freeform read
        self.nar.clear()
        self.reader.readText(segment,tokens)
        self.GOF = self.reader.vault.maxGOF()
        v = self.reader.vault._vault
        if len(v)>0:
            self.nar = v[ len(v)-1 ].nar

        self.lastConst = self.reader.vault.lastConst #the method not the value [??]

    def getEvents(self):
        if not self.eventrecord:
            return ''

        out = ''
        for event in self.eventrecord:
            out += event[1] + ", "
        return out

    def getLastThing(self):
        event = self.nar.lastConst
        return Thing(event)

    def getLastThingVAR(self):
        T = self.nar.thing
        return self.tree.lookup(T.lastConst)

    def getLastAction(self):
        event = self.nar.lastConst
        return Action(event)

    def getLastActionVAR(self):
        A = self.nar.action 
        return self.tree.lookup( A.lastConst )

    def getLastRelation(self):
        event = self.nar.lastConst
        return Relation(event)

    def getLastRelationVAR(self):
        R = self.nar.relation
        event = self.nar.lastConst
        return self.tree.lookup(R.lastConst)

    def getLastValue(self):
        event = self.nar.lastConst
        return Value(event)

    def getLastValueVAR(self):
        V = self.nar.value
        return self.tree.lookup(V.lastConst)

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

class NWTopic():
    def __init__(self, treeroot, readers):
        self.tree = treeroot.copy()
        self.readers = readers
        self.maxGOF = 0.0
        self.numtokens = 0
                # These will be extended with segments during read(), and
                # and with response VARs during write(). Saves the last
                # 4 exchanges - a short term context
        self.Context = SegmentBuffers(8)  
     
  
    def read(self,text):
                # (inefficient but leaves the door open to tree specific customization)
        tokens = prepareTokens(text) 
        self.numtokens = len(tokens) #useful
        
        segment = PrepareSegment(self.tree, tokens) 
         
        self.Context.addSegment(segment)
        
                # Sanity check. It is easy to fail this test, but we want robust  
                # code below, that works around the failure.
                # Cause is a tree with different nodes matching the token. Inserting
                # makes the indexing be out of sync between tokens and VARs in the segment
        if len(segment) > len(tokens ):
            print("warning: several VARs match one token")
            bInsertSafe = False
        else:
            bInsertSafe = True
 
        self.maxGOF = 0.0
        for reader in self.readers:
            reader.readSegment( segment, tokens )

            if self.maxGOF<reader.GOF:  
                self.maxGOF= reader.GOF

            if 0.25<= reader.GOF and reader.GOF<0.75:
                        # find the missing node (if there is just one)
                EBM = reader.nar.getExpectedButMissing()
                if EBM==NULL_VAR : 
                    continue

                        #convert the context into children of that node
                a = self.Context.getAll()  
                a2  = EBM.filter(a)
                if len(a2)==0:
                    continue
                              
                ext = []
                newseg = []
                if bInsertSafe:
                    itok = 0
                    newtokens = [] # prepare for inserting
                else:
                    newtokens = tokens 
                        # in this case "insertions" happen at the end of the array

                for var in segment:
                    newseg.append(var)
                    if bInsertSafe:
                        newtokens.append( tokens[itok] )
                        itok += 1

                    if var.contextFn:
                        
                        ext = var.contextFn( a2 )
                         
                        newseg.extend( ext ) #insert or append
                        for var1 in ext:
                            newtokens.append( var1.lastConst )

                if len(ext)>0:
                    reader.readSegment( newseg, newtokens )

            if self.maxGOF<reader.GOF: #update
                self.maxGOF= reader.GOF

    def summary(self):
        out = self.tree.knames[0] + ":\n"
        for reader in self.readers:
            out += reader.summary() + "\n"
        return out

    def getReader(self, id ):
        for reader in self.readers:
            if reader.id==id :
                return reader
       
    def getBestReader( self ):
        for reader in self.readers:
              if reader.GOF==self.maxGOF:
                  return reader


#################################
# This model of data is that of a collection of bins, 
# Each empty or containing something interesting. 
# They are put in a preferred sequence but
# may end up being filled non-sequentially
# At the current abstract stage, a responder is
# a pair of dictionaries - of response strings, and respond VARs
# The sequentional nature is NOT required.
#################################
NULLSTAGE = 0
# Note that response[] and responseVARs[] are constant dictionaries
# and a class instance will be constant
class NWTopicResponder:
    def __init__(self, response, responseVARs ):
        self.response = response  
        self.responseVARs = responseVARs
        self.NumStages = min( len(response), len(responseVARs) ) #should be same
        self.stage = NULLSTAGE
        self.extratext = ''

    def getExtraResponse(self):
        return self.extratext

    # in case you want to default to the plain message
    def getStageResponse(self):
        s = self.response[ self.stage ] 
        return s

    def getAllResponse(self):
        s = self.getExtraResponse() + "\n" + self.getStageResponse()
        return s

    def getResponseVARs(self):
        return self.responseVARs[ self.stage ]


#--------------------------------------
# Default responder
AOK = 0 # agree
ANOK = 1 # apologize but "no"
AQU = 2 # ask clarifaction
aResponse = {
    AOK : "ok",
    ANOK: "I {}",
    AQU : "please clarify {}"
    }
aResponseV = {
    AOK : [],
    ANOK : [],
    AQU : []
    }

class DefaultResponder( NWTopicResponder ):
    def __init__(self):
        NWTopicResponder.__init__( self, aResponse, aResponseV)
         

 
###########################
class TChat:
    # public API
    def __init__(self):
        self.gof = 0.0

    def Read(self, text):
        x = 2

    def Write(self):
        x = 2

       
        #  Derived classes can reference the same data
    def SetData(self, data):
        x = 2

    def GOF():
        return self.gof

    def __add__(self, other):
        return CompositeChat(self, other)

    # Implements tchat1 + tchat2
class CompositeChat( TChat ):
    def __init__(self, A, B):
        if isinstance(A, CompositeChat ):
            a = A.chats
        else:
            a = [A]
        if isinstance(B, CompositeChat ):
            b = B.chats
        else:
            b = [B]

        self.chats = a + b 
        self.gof = 0.0

    def Read( self, text ):
        for chat in self.chats:
            chat.Read( text )

    def Write(self):
        s = ''
        maxGOF = 0.0
        first = True
        for chat in self.chats:
            if maxGOF<chat.GOF():
                maxGOF = chat.GOF()
            w = chat.Write() 
            if chat.GOF()<0.5:
                continue         
            if len(w)>0:
                if first:
                    first = False
                else:
                    s += '\n'
                s += w 

        self.gof = maxGOF

        if maxGOF>=0.5 : # cutoff on response
            return s
        else:
            return ''

    def SetData(self, data):
        for chat in self.chats:
           chat.SetData(data)


# "tchat" combines NWTopic (a family of NAR readers) and NWResponder  
#
# Derived classes will implement data, and its modification by input text
#
# TChat's streamiled API of Read/Write/GOF score might be visualized
# as a box with an input wire, an output wire, and a light bulb that
# is bright or dim according to the GOF - colored accoring to the
# completion state of the data. 
#
# NO. A chatbot community will be structured like the data that is 
# central to its topics. Note the NWTopicChat, does not implement SetData()

class NWTopicChat(TChat):
    def __init__(self, topic, responder): 
        self.topic = topic
        self.responder = responder
        self.gof = 0

        self.data     = 0
        self.prevdata = 0
        self.caveat = ''   # for out-of-bounds warning 

    ### Public API for a topic chat ######
        
    def Read(self, text ):  
        self.caveat = ''
        self.prevdata = self.data # keep copy
            
        self.topic.read( text )  
        self.gof = self.topic.maxGOF
        print( self.topic.summary() )
                # transfer info from subreaders of the topic into the data structure
        self.update()

    def GOF(self):
        return self.gof

    def Write( self ):
        outtext = self.write() # also changes the responseVARs 
        self.topic.Context.addSegment( self.responder.getResponseVARs() )
        return outtext

        ### Private implementation for an topic chat ######

    """ update()
    To be overridden in derived classes. Assuming a derived class contains a data object "data"
    and a narrative narX, we might call data.updateX( narX ) after a read() and consider accessing 
    these sorts of values. Mostly these are on the screen after a read, due to the active printing
    funcitons. So you can see what you have to work with.
        - is narX==None?
        - is narX.GOF>=0.5? (The goodness of fit of the narX to the text)
        - is narX.polarity True or False? (False means a negative of some kind)
        - is len( narX.eventRecord )>0?
        for event in narX.eventRecord:
        access event[0], the event GOF 
        access event[1] content with Thing(event[1]), Action(event[1]), 
        Relation(event[1]), or Value(event[1]) 
    access narX.lastConst (also via the Thing(), Action(), Relation(), Value() functions
    """
    def update(self):
        self.responder.extratext = ''
        x=2 # do nothing. override in derived classes

        # override in derived classes. This is called after a read()
        # it sets a response and a responseVARs slot.
    def write( self ):
        return self.responder.getStageResponse()
