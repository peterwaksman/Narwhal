import collections

from narwhal.nwtypes import *
from narwhal.nwcontrol import *
from narwhal.nwsegment import *

from narwhal.nwcontextrecord import *


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

    def newRecord(self, id):
        return ContextRecord(id, self.context[id].MODS)

              # need error checking that dict and modvars are already OrderedDict type.
              # modhandlers does not need to be ordered
    def  __init__(self, dict, modvars, modhandlers, rootID):
        self.context = collections.OrderedDict()           
        
        self.rootID = rootID 
 
            # create frames, making self.context an OrderedDict
        for id in dict:
            x = dict[id]
            context = ContextFrame(id, x[0], x[1], x[2], x[3], x[4] )    
            self.context[id] = context   
             
            # because of this initialization, there must 
            # either be null, generic, or mod-specific handlers. 
            # See MARGIN_DEPTH
            context.RELS = {}
            for mod in x[1]:
                context.RELS[mod] = modhandlers[mod] 
 
            # this wires together the vars 
        self.tree = self.buildSelfTree(rootID)

        self.modvars = modvars
        self.mtree = {}
        for id in dict:
            self.mtree[id] = self.getMODTree(id)
    
        self.ledger = self.newRecord(rootID)
        self.activeRecordIDs = [rootID]
      

        # when 'id' is in a segment, it may not be an id of this tree
    def isID(self, id):
        if self.context.get(id):
            return True
        else:
            return False

    def getVar(self, id):
        if self.isID(id):
            return self.context[id].var
        else:
            return None
 
    def getMODTree( self, id ):
        c = self.context[id]
        return c.getMODTree(self.modvars)

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


    def isActive(self, id):
        for jd in self.activeRecordIDs:
            if jd==id:
                return True
        return False

    def getParent(self, id):
        return self.context[id].ENV

    def getLastChild(self, id):
        if self.children:
            return self.children[ len(c.children)-1 ]
             
        # returns None if id is not active
    def getRecentRecord(self, id):
        if id==self.rootID:
            return self.ledger

        c = self.ledger
        while c.children:
            c = c.children[ len(c.children)-1 ]
            if c.id==id:
                return c

    def copyLastAll(self ):
        L = {}
        #L[self.rootID] = self.ledger

        for id in self.activeRecordIDs:
            if id==self.rootID:
                continue
            rec = self.getRecentRecord(id)
            newrec = rec.copy(True) # make a "soft" copy
            L[id] = newrec

        prevrec = self.ledger
        for id in self.activeRecordIDs:
            if id==self.rootID:
                continue
            prevrec.children.append( L[id] )
            prevrec = L[id]
        x = 2

    def resetActiveIDs(self):
        self.activeRecordIDs = []
        c = self.ledger      
        while c:
            self.activeRecordIDs.append( c.id )
            if c.children:
                c = c.children[ len(c.children)-1 ]
            else:
                break
 
            # when id is not active, need different chain of ids
    def appendChain(self, id, rec):
        arec = rec
        pid = self.getParent(id)
        while not self.isActive( pid ):
            k = self.newRecord(pid)
            k.children.append( arec )
            arec = k
            pid = self.getParent( pid )

        # now pid is "common ancestor" above id but also "active"
        k = self.getRecentRecord(pid)
        k.children.append( arec )




    ##############################################
    ##############################################

    def read( self, text ):
        """ match text tokens to VARs in the context"""
        rawtokens = []
        tokens = prepareTokens(text, rawtokens) 
           
            # fill the self.tree with 'found' vars
        segment = PrepareSegment(self.tree, tokens, rawtokens)   
 
            # sadly, this is needed to coordinate the internal Narhwal 'and'
            # with this external stepping through of IDs
        idcount = {}
        for var in segment:       
            id = var.knames[0] 
            idcount[id] = 0         

        for var in segment:       
            id = var.knames[0]          

            if self.isID(id):
                MODS = self.context[id].MODS

                for mod in MODS :
                    R = self.fillRecord(id, mod, tokens, rawtokens)
                    if not R:
                        continue

                    j = 0
                    for rec in R:
                        if j==idcount[id]:
                            self.writeDetail(id, rec)
                        j = j+1

                        x = 2

            idcount[id] = idcount[id]+1
                 
        s = self.ledger.str()
        print("***********\n")
        print(s)

        #self.ledger.harden()
        #self.activeRecordIDs = [self.rootID]
                
 
        """  
          The MERGE, SPLIT, or APPEND algorithm
         'mod' is an un-seen argument.  It can be changing
          behind the scenes, modifying different parts of the record  """
    def writeDetail(self, id, rec):

        if self.isActive(id):
            parentID = self.getParent(id)

            s = self.ledger.str()

               # ---- MERGE ----                   
            if not parentID:  # special case of id==rootID             
                self.ledger.merge(rec)  # (ignore return value)
                self.activeRecordIDs = [self.rootID]
                return
                        
            else:             # In these cases, no change to "activeRecordsIDs"     
                prevRec     = self.getRecentRecord( id )
                if prevRec.merge(rec):   
                    return

                # ---- SPLIT ----
                else:         
                    self.copyLastAll() # makes soft copy of recent sequence of records
                    prevRec = self.getRecentRecord( id ) # which becomes "previous"
                    ok = prevRec.merge(rec, rec.block)
                    if not ok: # the soft copy should be writable
                        print("OOPS in SPLIT!")
                    return
              

            # ---- APPEND ----
        else: # this id is not in the current active chain
            self.appendChain(id, rec )
            self.resetActiveIDs()
            return

    def fillRecord(self, id, mod, tokens, rawtokens):    
        proc = self.context[id].RELS[mod]
        if proc == nullRel:
            return []

                # get temp tree+modtree
        tree = self.tree.copy()
        for mod2 in self.context[id].MODS:
            mtree = self.modvars[mod2]
            tree.sub( mtree )

        print( tree.PrintSimple() )

        segM = PrepareSegment(tree, tokens, rawtokens)
        
        print( printSEG(segM) )

        
        R = proc(segM, tree, tokens, id, mod, self.context[id].MODS ) 
        return R
  
