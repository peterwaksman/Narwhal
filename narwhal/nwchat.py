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
        self.nar.clear()
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
        v = self.reader.vault._vault
        if len(v)>0:
            self.nar = v[ len(v)-1 ].nar

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

class TopicFamily():
    def __init__(self, treeroot, datanodes):
        self.tree = treeroot.copy()
        self.nodes = datanodes
        self.maxGOF = 0.0
        self.numtokens = 0

        #self.context = [] # will be extended with segments during read, and
                          # and with response VARs during 
        self.C = SegmentBuffers(5)

 
 
 
    def read(self,text):
                # (inefficient but leaves the door open to tree specific customization)
        tokens = prepareTokens(text) 
        self.numtokens = len(tokens) #useful
        
        segment = PrepareSegment(self.tree, tokens) 
         
        self.C.addSegment(segment)
        
                # Sanity check. It is easy to fail this, but we want robuts code 
                # below, that works around the failure
        if len(segment) > len(tokens ):
            print("Oops your trees are messed up!. Multiple nodes match one token")
            bInsertSafe = False
        else:
            bInsertSafe = True
 
        self.maxGOF = 0.0
        for node in self.nodes:
            node.readSegment( segment, tokens )

            if self.maxGOF<node.GOF:  
                self.maxGOF= node.GOF

            if 0.25<= node.GOF and node.GOF<0.75:
                        # find the missing node (if there is just one)
                EBM = node.nar.getExpectedButMissing()
                if EBM==NULL_VAR : 
                    continue

                        #convert the context into children of that node
                a = self.C.getAll()  
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
                    node.readSegment( newseg, newtokens )

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
# init with an array of TopicFamilies
class NWChat():
    def __init__(self, topics):
        self.topics = topics
        self.updated = False # becomes true when stored data is changing
        self.numtokens = 0   #you'll see why this is helpful
        self.rawmode = False
        self.responseVARs = []

        self.log = NWLog()
        self.loggingOn = True

    def read(self, text ):
        if self.loggingOn:
            self.log.add("Q: "+text + "\n")

        for topic in self.topics:
            topic.read( text )         
            self.numtokens = topic.numtokens
            print( topic.summary() )

         # absorb the info
        self.updateAll()

    def updateAll(self):
        """ 
        To be overridden in derived classes. Assuming a derived class contains a data object "meta"
        and a narrative narX, we might call meta.updateX( narX ) after a read() and consider accessing 
        these sorts of values 
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
        x=2 # do nothing. override in derived classes


    def RespondNext( self ):
        x = 2 # override in derived classes


    def respondNext( self ):
        self.responseVARs = [] # to store internally generated VARs for addition to the context

        response = self.RespondNext() # also sets the self.responseVARs, per derived class

        for topic in self.topics:
            #topic.context.extend( self.responseVARs )
            topic.C.addSegment( self.responseVARs )

        if self.loggingOn:
            self.log.add("A: "+ response + "\n\n")

        return response

 
    def getTopic(self, id ):
        for topic in self.topics:
            if topic.tree.knames[0]==id :
                return topic

    # tid and nid are, respectively, names of a datanode and its TREE
    def getNode( self, tid, nid):
        topic = self.getTopic( tid )
        if topic:
            return topic.getNode( nid )



          