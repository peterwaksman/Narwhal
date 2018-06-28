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
        self.ID = id # should be unique
        self.ENV = env # None or another ID, could be dynamically assigned
        self.MODS = modifiers # list of enum vals
        self.PARTS = parts # list of IDs
        self.RELS = relations # tbd
            # language related
        self.var = var
        

    def getMODTree(self, modVARs):
        tree = KList(self.ID+'MODS', "").var()
        for mod in self.MODS:
            tree.sub( modVARs[mod] )
        return tree

   
"""
ContextRecords will be of the form
        [ID, val, val, val....] 
Where the ID is for the context being recorded and where val is 
None or a string filled by a handler
"""
class ContextRecord:
    def __init__(self, cf ):
        self.id = cf.id
        self.val = []
        for mod in cf.mods: 
            self.val = ''

class ContextManager :

    # go all levels in
    def buildSelfTree( self, id ):
        tree = self.getVar(id) 
        for part in self.context[id].PARTS:
            tree.sub( self.buildSelfTree( part ) )
        return tree       

    def  __init__(self, dict, modvars, baseID):
        self.context = {}
        
            # create frames, making self.context a dictionary
        for id in dict:
            x = dict[id]
            self.context[id] = ContextFrame(id, x[0], x[1], x[2], x[3], x[4] )                 

            # this wires together the vars 
        self.tree = self.buildSelfTree(baseID)

        self.modvars = modvars
        self.mtree = {}
        for id in dict:
            self.mtree[id] = self.getMODTree(id)
    

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


    def read( self, text ):
        """ match text tokens to VARs in the context"""
        rawtokens = []
        tokens = prepareTokens(text, rawtokens) 
           
            # fill the self.tree with 'found' vars
        segment = PrepareSegment(self.tree, tokens, rawtokens)   
            
            # Active contexts
        idvect = self.detectActiveContexts()
            
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
