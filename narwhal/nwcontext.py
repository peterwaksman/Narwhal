""" 
nwcontext.py is for handling "context" - which is defined as past words implictly used
in current sentences. By my lights there are a very limited set of such things, excluding
various personal pronouns that can be assumed absent in a sales-bot application, or can
be brought in later. For now we have these categories of concept:

Positing and juxtpositing mechanisms bring ideas into mind. 
And the basic operations that apply
to one or several postited ideas are:
group       (for comparable nouns)
alternate   (for distinct values of an adjective category like color)
merge       (for adjective values from different categories that apply to the same nouns)
sequence    (for nouns in sequence)

The goal of nwcontext is to support these operations as CONTEXT_OP vars, as you will see.
The plan is: label parents with the above identifiers and look in the past context for
words that share the right sort of parent.
 
"""

from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwsegment import *


class SegmentBuffers:
    def __init__(self, N):
        self.N = N
        self.buffer = []
        for i in range(0,N):
            self.buffer.append( [NULL_VAR] )
        self.next = 0

    def clear(self):
        for i in range(0,self.N):
            self.buffer[i] = [NULL_VAR] 

    def addSegment(self, segment):
        self.buffer[ self.next ] = segment
        self.next = (self.next+1)%self.N

    def getAll( self ):
        a = []
        for i in range(0,self.N):
            s = self.buffer[(self.next + i)%self.N ]
            if s != [NULL_VAR]:
                a.extend( s )
        return a

""" Some basic methods, followed by increasingly abstract entitiees"""

# willforget context after this many vars have gone bye.
MAXCONTEXTMEM = 30


def isParent(node, var):
    for child in node.children :
        if child.equals(var):
            return True
    return False

# find the node of tree with isParent(var) True
def getParent(tree, var):

    if isParent(tree,var):
        return tree
     
    for node in tree.children:
        p = getParent(node,var)
        if  p == NULL_VAR:
            continue
        else:
            return p

    return NULL_VAR

##############################
def get2Alternatives(tree, segment ):
     revseg = segment[::-1] # reverse the list
     p = NULL_VAR
     q = NULL_VAR
     var0 = NULL_VAR
     numvars = 0
     for var in revseg:

         numvars += 1
         if numvars>MAXCONTEXTMEM:
             continue

         # find a parent that is "ALTERNATIV"E
         p = getParent(tree,var)
         if not p.contextType == ALTERNATIVE_CONTEXT:
             continue

         # if you already saw such a parent
         if not q==NULL_VAR:
             if q.equals(p): #and it is the same parent
                 return [ var, var0]
             else:
                return [NULL_VAR, NULL_VAR]
         q = p.copy()
         var0 = var
     return [NULL_VAR, NULL_VAR]
    
def getOneOfGroup(tree, segment):
     revseg = segment[::-1] # reverse the list
     p = NULL_VAR
     numvars = 0
     for var in revseg:
         numvars += 1
         if numvars>MAXCONTEXTMEM:
            continue

         # find a parent that is "ALTERNATIVE"
         p = getParent(tree,var)
         if not p.contextType == GROUP_CONTEXT:
            continue
         # returns first groupable var
         return [var]
     return [NULL_VAR]

def getManyOfGroup(tree, segment):
    revseg = segment[::-1] # reverse the list
    p = NULL_VAR
    h = []
    numvars = 0
    for var in revseg:
        numvars += 1
        if numvars>MAXCONTEXTMEM:
            continue

        # find a parent that is "ALTERNATIVE"
        p = getParent(tree,var)
        if not p.contextType == GROUP_CONTEXT:
            continue
        # returns first groupable var
        h.append(var)
    return h

    # look for two ints in context and get their associated last const
def get2Ints(tree, segment):
    revseg = segment[::-1] # reverse the list
    p = NULL_VAR
    h = []
    numints = 0
    for var in revseg:
        if var.isA("int"):
            numints += 1
            if numints<=2:
                h.append( var )
    h = h[::-1]
    return h

def getAll(tree, segment ):
    revseg = segment[::-1] # reverse the list
    p = NULL_VAR
    h = []
    for var in revseg:
        if var != NULL_VAR:
            h.append( var )
    h = h[::-1]
    return h

def getN(segment, N):
    revseg = segment[::-1] # reverse the list
    p = NULL_VAR
    h = []
    n = 0
    for var in revseg:
        if var != NULL_VAR:
            if n<N:
                h.append( var )
                n += 1
            if n==N:
                break
    h = h[::-1]

    if len(h)<N :
        h = []

    return h

def get2( segment ):
    return getN(segment,2)

def get1( segment ):
    getN(segment,1) 



######################################################
######################################################

 


kDIFF = "difference, compare "

#DIFF = KList("diff", kDIFF).var(get2Alternatives)
DIFF = KList("diff", kDIFF).var(get2)


kBOTH = "both, the pair , the two"
#BOTH = KList("both", kBOTH).var(get2Ints)
BOTH = KList("both", kBOTH).var(get2)