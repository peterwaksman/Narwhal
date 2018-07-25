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
        self.lastActiveRecord = self.ledger
        x=2

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


        # this does NOT include the self id 
        # and list is returned bottom-to-top
    def getAllParents(self, id, stopID=None):
        context = self.context[id]

        idList = [] # [id] for now let us not include id as its own parent
        while context.ENV:
            context = self.context[ context.ENV ] # step back to the parent
            idList.append( context.ID )
            if context.ID==stopID:
                break;
        return idList
        
        # this *does* include the id1 and id2 as possible results
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

  
    def getLastParent(self):
        p = self.ledger
        s = p
        while p != self.lastActiveRecord:
            s = p
            if p.children:
                p = p.children[ len(p.children)-1 ]
        return s
    


    ##############################################
    ##############################################

    def read( self, text ):
        """ match text tokens to VARs in the context"""
        rawtokens = []
        tokens = prepareTokens(text, rawtokens) 
           
            # fill the self.tree with 'found' vars
        segment = PrepareSegment(self.tree, tokens, rawtokens)   
 
        for var in segment:
            id = var.knames[0]
            if id!='nullK':
                mods = self.context[id].MODS

                for mod in mods:
                    r = self.fillRecord(id, mod, tokens, rawtokens)
                    s = self.ledger.str()
                    self.writeDetail(id, mod, r, self.tree, tokens, rawtokens)
                    s = self.ledger.str()
                    x = 2
                x = 2   

        s = self.ledger.str()
        print("***********\n")
        print(s)

        #self.ledger.harden()

        #      # Active contexts
        #idvect = self.detectActiveContexts()
            
        #        # MOVE THIS
        #    # Active modifiers
        #mvect = []
        #for id in idvect:
        #    mvect.extend(self.detectSubActiveMods(id, tokens, rawtokens) )

        #    # merge the trees
        #T = KList("temp","").var()
        #T.sub( self.tree)

        #for id in mvect:
        #    T.sub( self.mtree[id] )

        #segM = PrepareSegment(T, tokens, rawtokens)

        #print( T.PrintSimple() + "\n")
        #print( "SEG: " + printSEG( segM ) )

 


    def writeDetail(self, id, mod, s, tree, tokens, rawtokens):
        last = self.lastActiveRecord

        if last.id == id :
            keepSameFocus = True
        else:
            keepSameFocus = False

     
        # WRITE OUT (using last or a copy)------------
        #  write out record in existing "last" or its copy
        if keepSameFocus:
            if last.details[mod][1] != HARDDETAIL:
                last.merge(s)
                self.lastActiveRecord = last
            elif s.details[mod][1]==HARDDETAIL:
                p = self.getLastParent()
                p.children.append(s)
                self.lastActiveRecord = s
            else: # ????
                last = last.copy()
                last.merge(s)
                self.lastActiveRecord = last
                p = self.getLastParent()
                p.children.append(last)
            return

        # or else we have some parent above 'id'
        commonID = self.getCommonParent(id, last.id )

        """ for rootID, allow merge but not append"""
        # OK here? was moved from below
        if id==commonID and commonID==self.rootID:
            self.ledger.merge(s)
            self.lastActiveRecord = self.ledger
            return


        # WRITE OUT TO A NEWLY FOCUSED RECORD 'r' -----
        # the "head" of r is re-used
        r = self.ledger
        while( r.id != commonID ):
            r = r.children[  len( r.children)-1 ]
                # r is a record that now stops at commonID

        # then new records are created between r and s
        plist = self.getAllParents(id, commonID )  
        plist.reverse()  
        for pid in plist:
            if pid==commonID:
                continue
            c = self.newRecord(pid)
            r.children.append(c)
            r = c

        # now r is nested to the correct depth (I hope!)
        r.children.append( s )

        self.lastActiveRecord = s


    def fillRecord(self, id, mod, tokens, rawtokens):
        s = self.newRecord( id )

        proc = self.context[id].RELS[mod]
        if proc == nullRel:
            return s

                # get temp tree+modtree
        tree = self.tree.copy()
        mtree = self.modvars[mod]
        tree.sub( mtree )

        print( tree.PrintSimple() )

        segM = PrepareSegment(tree, tokens, rawtokens)
        
        print( printSEG(segM) )

 
        proc( segM, tree, tokens, s, mod) 
        return s
  
                    
