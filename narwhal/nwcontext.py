import collections

from narwhal.nwtypes import *
from narwhal.nwcontrol import *
from narwhal.nwsegment import *


""" 
----------------------------------------------------------
ContextFrames will be of the form 
        self.ID = id          # should be unique string
        self.ENV = env        # None or another ID, could be dynamically assigned
        self.MODS = modifiers # list of enum vals
        self.PARTS = parts    # list of IDs
        self.RELS = relations # tbd
        self.var =            # a VAR based on KList defining identity of self. 
                              # var.knames[0] should match id

This can be encoded in a dictionary entry of the form
 #  id     : [env,   mods ,  parts ,  rels , var]

Where id and env are strings; mods is a list of predefined constants; 
parts is a list of strings; rel is a list of tbd-type; and var is a 
predefinedVAR.

A dictionary of such entries is passed to the ContextManager (defined below)
And it's __init__() creates a collection of ContextFrames linked by shared IDs

Why use int encodings of mods rather than strings? To emphasize that mods
are not parts and eah one corresponds to a single slot of information filled 
by one of the "RELS" handler functions. So we use those int constants as 
keys to a dictionary of handler functions. 

The RELS is tbd but it looks like it is a dictionary of handler functions.

"""

class ContextFrame:
    def __init__(self, id, env, modifiers, parts, relations, var=NULL_VAR):
        self.ID = id         # should be a unique string
        self.ENV = env       # None or another ID 
        self.PARTS = parts   # list of other IDs
        self.MODS = modifiers # list of enum vals
        self.RELS = relations # list of procedures, on per modifier

        self.var = var        # keywords that detect this frame
        

    def getMODTree(self, modVARs):
        tree = KList(self.ID+'MODS', "").var()
        for mod in self.MODS:
            tree.sub( modVARs[mod] )
        return tree


"""
ContextRecord will be of the form
        [ID, val, val, val....] 
Where the ID is for the context being recorded and where val is 
None or a string filled by a handler, one for each of the MODS
"""
class ContextRecord:
    def __init__(self, context, iparent = [] ):
        self.id = context.ID

        self.mods = []
        for mod in context.MODS: 
            self.mods.append('')

        self.iparent = iparent # list of indeces of records in parent that are
                               # understood to share this record 'child'
        self.done = False

    def str(self):
                        # id
        out = self.id + ": "
                        # mods
        for mod in self.mods:
            if mod:
                out += mod + ","
            else:
                out += '*' + ","

                       # parent record indices
        out += " ["
        if self.iparent:
            for i in self.iparent:
                out += str(i)
                if i< len(self.iparent)-1:
                    out += ","
        out += "] "

        return out

    def copy(self, other):
        other.id = self.id
        other.mods = []
        for mod in self.mods: 
            other.mods.append('')
        other.parent = self.parent 
        other.done = self.done

    def isBlank(self):
        for v in self.mods:
            if v!='':
                return False
        return True

    def isCompatible(self, other):
        if not self.iparent==other.iparent:
            return False
        if not self.id==other.id:
            return False
        s = self.mods
        k = other.mods
        for i in range(0, min( len(s), len(k))):
            if s[i]==k[i] or s[i]=='' or k[i]=='':
                continue
            else:
                return False
        return True

    def merge(self,other):   
        s = self.mods
        k = other.mods 
        for i in range(0, min( len(s), len(k))):
            if k[i]!='':
                s[i] = k[i]
 

""" 
ContextManager is a collection of ContextFrames linked together by IDs shared through
the ENV and PARTs of the ContextFrames. Initialized from a dictionaary and based on
constants
""" 
class ContextManager :

    # go all levels in
    def buildSelfTree( self, id ):
        tree = self.getVar(id) 
        for part in self.context[id].PARTS:
            tree.sub( self.buildSelfTree( part ) )
        return tree       

                 # need error checking that dict and modvars are already OrderedDict type.
    def  __init__(self, dict, modvars, rootID):
        self.context = collections.OrderedDict()
        self.records = collections.OrderedDict()
        
        self.rootID = rootID 
        self.lastActiveID = rootID

            # create frames, making self.context an OrderedDict
        for id in dict:
            x = dict[id]
            context = ContextFrame(id, x[0], x[1], x[2], x[3], x[4] )    
            self.context[id] = context   
            self.records[id] = []             

            # this wires together the vars 
        self.tree = self.buildSelfTree(rootID)

        self.modvars = modvars
        self.mtree = {}
        for id in dict:
            self.mtree[id] = self.getMODTree(id)
    
        x = 2

    def getVar(self, id):
        return self.context[id].var
     
    def getMODTree( self, id ):
        c = self.context[id]
        return c.getMODTree(self.modvars)

    def detectActiveContexts( self ):
        idvect = []
        for id in self.context:
            v = self.getVar(id)
            if v.found:
                idvect.append(id)
        return idvect

    def hasActiveMODS( self, id, tokens, rawtokens):
         mtree = self.mtree[id]
         segM = PrepareSegment( mtree, tokens, rawtokens)
         if mtree.foundInChildren:
             return True
         else:
             return False

         # TODO? This gets duplicate copies of self IDs, if parts have parts
    def detectSubActiveMods( self, id, tokens, rawtokens ):
        idvect = []
            # append active mods of 'self'
        if self.hasActiveMODS( id, tokens, rawtokens ):
            idvect.append(id)
             # append active mods of parts
        for part in self.context[id].PARTS:
            idvect.extend( self.detectSubActiveMods(part, tokens, rawtokens) )
        return idvect

    def getParentID(self, id):
        return self.context[id].ENV

        # this does not include the id 
    def getAllParents(self, id):
        context = self.context[id]

        idList = [] # [id] for now let us not include id as its own parent
        while context.ENV:
            context = self.context[ context.ENV ] # step back to the parent
            idList.append( context.ID )
        return idList
        
        # this does inculude the id1 and id2
    def getCommonParent(self, id1, id2 ):
        pid = self.getAllParents(id1)
        pid.reverse()
        pid.append(id1)
       
        qid = self.getAllParents(id2)
        qid.reverse()
        qid.append(id2)

        id = ''
        for j in range( 0, min(len(pid), len(qid)) ):
            if pid[j]!=qid[j]:
                break
            else:
                id = pid[j]
        return id

            
    def getActiveTail(self, id):
        R = self.records[id]
        if len(R)==0:
            R.append( ContextRecord(self.context[id], None) )                       
        tail = []
        for i in range(0,len(R)):
            if R[i].done:
                continue
            tail.append(i)
        return tail


    def getLast(self, id):
        R = self.records[id]
        if R:
            return R[ len(R)-1 ]
        else:
            return None

        # indented block of records for this id
    def strRecord(self, id, ntabs):
        pre = ''
        for i in range(0,ntabs):
            pre += "\t"

        out = ''
        for r in self.records[id]:
            out += pre + r.str() + "\n"

        return out

    def strSubRecords( self, id, ntabs ):
        out = self.strRecord( id, ntabs)
        for part in self.context[id].PARTS:
           out += " " + self.strSubRecords( part, ntabs+1 )
        return out
            
    def StrRecords(self):
        return self.strSubRecords( self.rootID, 0 )


    def read( self, text ):
        """ match text tokens to VARs in the context"""
        rawtokens = []
        tokens = prepareTokens(text, rawtokens) 
           
            # fill the self.tree with 'found' vars
        segment = PrepareSegment(self.tree, tokens, rawtokens)   
            
            # Active contexts
        idvect = self.detectActiveContexts()
            
                # MOVE THIS
            # Active modifiers
        mvect = []
        for id in idvect:
            mvect.extend(self.detectSubActiveMods(id, tokens, rawtokens) )

            # merge the trees
        T = KList("temp","").var()
        T.sub( self.tree)

        for id in mvect:
            T.sub( self.mtree[id] )

        segM = PrepareSegment(T, tokens, rawtokens)

        print( T.PrintSimple() + "\n")
        print( "SEG: " + printSEG( segM ) )

               
        for id in idvect:
            for mod in self.context[id].MODS:
                self.makeRecord( id, mod ) 
        x = 2
        
        s = self.StrRecords()

        self.FinalizeAllRecords()    


    def makeRecord( self, id, mod ):   
        # EVALUATE MOST RECENT RECORDS ------------        
        r = self.getLast(id)
        if not r or r.done:
            needNewIParents = True
        else:
            needNewIParents = False


        # CREATE A NEW RECORD -----------------------
        s = ContextRecord(self.context[id], [])
 
        # FILL IT HERE -------------------------------

        # MERGE OR SPAWN -----------------------------     
        # We are extending records, in the current context....           
        if not needNewIParents: 
            if r.isCompatible(s): 
                r.merge(s) 
            else:
                s.iparent = r.iparent
                self.records[id].append(s)
            return

        # ... or it is a first time we are here in a new context     
        commonID = self.getCommonParent(id, self.lastActiveID )
 
        # CONNECT THE PARENTS -------------------------
        """ If the commonID has changed we need to insert blank records. All
        the records between id and commonID should be blank, singular, and 
        wired together. 
        Confusing? parent is a node, iparent is an index of a record for 
        the node
        """      
        mID = id  
        pID = self.getParentID(mID) 
        if not pID:
            self.records[mID].append(s) 
            self.lastActiveID = id
            return

 
        while pID != commonID:
            s.iparent = self.getActiveTail(pID) # allocates a record, len(s.iparent)==1
            self.records[mID].append(s)

            if( len(s.iparent)) != 1:
               print("OOPS!")

            mID = pID
            pID = self.getParentID(mID)
                
        s.iparent = self.getActiveTail(commonID)
        self.records[mID].append(s) 
        
        # UPDATE --------------------------------
        self.lastActiveID = id

        # Phew! Now THAT is an algorithm



    def FinalizeAllRecords(self):
        for id in self.context:
            for r in self.records[id]:
                r.Done = True

 
