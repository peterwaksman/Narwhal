from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *

from stdtrees.quantities import QUANTITY

strAPOLOGY = "Sorry, I did not understand that."
strINFO = "Here is an link article about"

""" NWDatanode
 Poorly named. This merges reading from NWNReader and from ReadSlotEvents()
 (only for NARs of order <=1). The word "node" is a legacy from when conversations 
 moving from node to node.

"""
class NWDatanode():
    def __init__(self, id, treeroot, nar, cal=False):
        self.id = id

        self.tree = treeroot.copy()
        self.nar = nar.copy() # convenient to use outside the reader
        self.reader = NWNReader( self.nar, cal )

        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''
        self.eventGOF = 0.0

    def clear(self):
        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''

        # deprecated
    def read( self, text ):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree, tokens) #not efficient, could do this at higher level,
        self.readSegment( segment, tokens)
   

    def readSegment( self, segment, tokens ):
        self.clear()

        # look for structured data
        self.eventrecord = recordSlotEvents( self.nar, segment )
        self.eventGOF = maxEventGOF( self.eventrecord )

        # freeform read
        self.nar.clear()
        self.reader.readText(segment,tokens)
        self.GOF = self.reader.vault.maxGOF()
        self.lastConst = self.reader.vault.lastConst #the method not the value

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

class TopicTree():
    def __init__(self, treeroot, datanodes):
        self.tree = treeroot.copy()
        self.nodes = datanodes
        self.maxGOF = 0.0

    def read(self,text):
        # (inefficient but leaves the door open to tree specific customization)
        tokens = prepareTokens(text) 
 
        segment = PrepareSegment(self.tree, tokens) 

        self.maxGOF = 0.0
        for node in self.nodes:
            node.readSegment( segment, tokens )

            if self.maxGOF<node.GOF: #update
                self.maxGOF= node.GOF

    def summary(self):
        out = self.tree.knames[0] + ":\n"
        for node in self.nodes:
            out += node.summary() + "\n"
        return out

    def getNode(self, id ):
        for node in self.nodes:
            if node.id==id :
                return node
   
#######################################################
#######################################################
#######################################################
# init with an array of TopicTrees
class NWChat():
    def __init__(self, topics):
        self.topics = topics
        self.updated = False # becomes true when stored data is changing

    def read(self, text ):
        for topic in self.topics:
            topic.read( text )         
            print( topic.summary() )

         # absorb the info
        self.updateAll()

    def updateAll(self):
        x=2 # do nothing. override in derived class


    def getTopic(self, id ):
        for topic in self.topics:
            if topic.tree.knames[0]==id :
                return topic
 
    def getNode( self, tid, nid):
        topic = self.getTopic( tid )
        if topic:
            return topic.getNode( nid )



          