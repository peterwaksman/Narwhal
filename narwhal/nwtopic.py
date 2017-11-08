from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *
from narwhal.nwcontext import *
from narwhal.nwsegment import *



"""
An NWTopicReader is a NAR wrapped with recording mechanisms.
An NWTopicData is a data object along with canned responses, in  
the form of canned response text and canned response VARs. 

The NWTopic brings a family of readers into combination with a data object so
it can manage conversations in its topic area. It supports a basic read/write,
which is (supposed to be) the basis of "communities" of topics.
During a read() it will:



"""



""" 
 NWTopicReader
 This merges reading from NWNReader and from ReadSlotEvents()
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

    def clear(self):
        self.nar.clear()
        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''

    def readSegment( self, segment, tokens ):
        self.clear()

        # look for structured data
        self.eventrecord = recordSlotEvents( self.nar, segment )
        self.eventGOF = maxEventGOF( self.eventrecord )

        # freeform read
        self.nar.clear()
        self.reader.readText(segment,tokens)
        self.GOF = self.reader.vault.maxGOF()
        V = self.reader.vault._vault
        if len(V)>0:
            self.nar = V[ len(V)-1 ].nar

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


##############################################
##############################################
##############################################

class NWTopicData:
    def __init__(self, Responses, ResponseVARs, data ):
        self.responses = Responses
        self.responseVARs = ResponseVARs
        self.NumStages = min( len( Responses), len(ResponseVARs)) #should be same
        self.stage = 0
        self.data = data 

    def getResponse(self):
        return self.responses[ self.stage ]

    def getResponseVARs(self):
        return self.responseVARs[ self.stage ]

    def update(self, readers):
        x = 2 # override in subclass

##############################################
##############################################
##############################################

class NWTopic():
    def __init__(self, treeroot, topic_readers):
        self.tree = treeroot.copy()
        self.readers = topic_readers
        self.maxGOF = 0.0
        self.context = SegmentBuffers(8) # stores last 4 input/output
        
        self.numtokens = 0  

        self.data = None # override in subclasses

    def read(self,text):
                # (inefficient but leaves the door open to tree specific customization)
        tokens = prepareTokens(text) 
        self.numtokens = len(tokens)  
        
        segment = PrepareSegment(self.tree, tokens) 
         
        self.context.addSegment(segment)
        
                # Sanity check. It is easy to fail this, but we want robuts code 
                # below, that works around the failure
        if len(segment) > len(tokens ):
            print("Oops your trees are messed up!. Multiple nodes match one token")
            bInsertSafe = False
        else:
            bInsertSafe = True
 
        self.maxGOF = 0.0
        for reader in self.readers:
            reader.readSegment( segment, tokens )

            if self.maxGOF<reader.GOF:  # update even when continue occurs below
                self.maxGOF= reader.GOF

            if 0.25<= reader.GOF and reader.GOF<0.75:
                        # find the missing node (if there is just one)
                EBM = reader.nar.getExpectedButMissing()
                if EBM==NULL_VAR : 
                    continue

                        #convert the context into children of that node
                a = self.context.getAll()  
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

    def getReader(self, id ):
        for reader in self.readers:
            if reader.id==id :
                return reader

    def summary(self):
        out = self.tree.knames[0] + ":\n"
        for reader in self.reader:
            out += reader.summary() + "\n"
        return out

    def update(self):
        """ 
        To be overridden in derived classes. Assuming a derived class contains a self.data object  
        and a narrative narX of a topic reader, we might call data.updateX( narX ) after a read()
        and consider accessing these sorts of values. Each consists of an aspect of what was read. 
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

