"""
nwsegment.py implements utilities associated with a "segment" which is
just a plain lists of VARs, without any wrapping. The most important are
    PrepareSegment() -  to convert text-to-tokens-VARs 
    ReadSegment() - the "inner loop" which reads all the text, recursively
    per the hierarchy inside each nar.
The relation between indices in the original tokens of text and indices in
the new "segmented text" is an unhappy one. Various methods try to 
coordinate them: getHi(), getLo(), wordReadRange
"""
# nwsegment.py for handling text segmentation utilities.
# used by the NWNReader. Contains utilities and the inner loop read() methods
from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *



#################################
#################################
""" 
The heart of Narwhal in some ways, yet this code is wrong.
In fact, PrepareSegment() should loop through all the VARS in the 
tree [it does now]. The current code may fail to set the ifound for VARs in the
tree ocurring later than ones found first. See the "criminal" line
of code below.
"""


# convert text to a segment
def PrepareSegment(tree, tokens, rawtokens):
    tree.clear()
    GENERAL_OP.clear()
    seg = []
    itok = 0
    for itok in range(len(tokens)):
        # LEAVE IN OR TAKE OUT? After all, it is WRONG
        # here is the "criminal" line:

        #if (itok in tree.ifound) or (itok in GENERAL_OP.ifound):
        #    seg.append(NULL_VAR)
        #    continue

        var = None
        vars = tree.findInText2(tokens, rawtokens, itok)
        # findInText2() can return a list of all vars matching here.
        if len(vars) > 0:
            for var in vars:
                var.ifound = cleanFound(var.ifound)
                newvar = var.copy()
                seg.append(newvar)
        else:
            vars = GENERAL_OP.findInText2(tokens, rawtokens, itok)
            if len(vars) > 0:
                for var in vars:
                    var.ifound = cleanFound(var.ifound)
                    newvar = var.copy()
                    seg.append(newvar)
            else:
                seg.append(NULL_VAR)
    return seg


    # a sort of inverse to findInText2()
    # you return with the first var whose ifound contains itok
    # or else return NULL_VAR
def findInSegment(segment, itok):
    for var in segment:
        if itok in var.ifound:
            return var
    return NULL_VAR

  ####################################################
    


def getLo(segment):
    lo = 10000
    for var in segment:
        if var == NULL_VAR or len(var.ifound)==0:
            continue
        x = max(var.ifound)
        if lo > x:
            lo = x
    return lo


def getHi(segment):
    hi = -1
    for var in segment:
        if var == NULL_VAR or len(var.ifound)==0:
            continue
        x = max(var.ifound)
        if hi < x:
            hi = x
    return hi


def isInLoHi(nar, lo, hi):
    ifound = nar.getIFound()
    for i in ifound:
        if lo <= i and i <= hi:
            return True
    return False
##################################


def varstring(var):
    if var == NULL_VAR:
        return "?"
    else:
        return var.string(0)

def showList(ifound):
    out = '['
    for i in ifound:
        out += str(i) + ','
    out += ']'
    return out
        

def showSEG(segment, text):
    rawtokens = []
    tokens = prepareTokens(text, rawtokens)
    out = ""
    for itok in range(len(tokens)):
        out += tokens[itok].rjust(10) + " "
        var = findInSegment(segment, itok)
        out += varstring(var) 
        out += "\n"
    return out


def printSEG(segment):
    out = ""
    for var in segment:
        out += varstring(var) + " "
    return out


def getWords(tokens, ifound):
    out = ""
    for i in ifound:
        out += tokens[i] + " "
    return out


def showSEG2(segment, text):
    rawtokens = []
    tokens = prepareTokens(text, rawtokens)
    out = ""
    for var in segment:
        h = ""
        h = varstring(var).rjust(10) + " " + \
            getWords(tokens, var.ifound) + " " + \
            showList(var.ifound) + "\n"
        out += h
    return out

def tabulateSEG(segment, tokens):
    numTokens = len(tokens)
    x = []
    for i in range(numTokens):
        x.append('.')
    for var in segment:
        # saves the *last* var in segment with this i
        i = var.lastIFound()
        if 0 <= i and i < numTokens:
            x[i] = var.knames[0]
            if var.polarity==True:
                x[i] += '+'
            else:
                x[i] += '-'
    return x

def tabulateSEG2( segment, tokens):  
    numTokens = len(tokens)
    x = tabulateSEG(segment,tokens)
    out = ""
    for i in range(numTokens):
        out += tokens[i].rjust(8) + " " + x[i].rjust(8) + "\n"
    print( out )
    return out


def isNullSegment(seg):
    for var in seg:
        if var != NULL_VAR:
            return False
    return True
            
################################################
################### inner read loop ############
def ReadSegment(nar, seg):
    nar.lastConst = "" # may get set in a sub ReadXXX
                       # redundant in the current code
    
    if ORDER(nar) == 0:
        if isinstance(nar,NAR):
            return ReadSegment0(nar.thing, seg)
        else:
            return ReadSegment0(nar,seg)
        #if isinstance(nar,VAR):
        #    return ReadSegment0(nar, seg)
        #else:
        #    return ReadSegment0(nar.thing, seg)

    action = nar.action
    relation = nar.relation
    target = nar.thing
    value = nar.value

    if target != NULL_VAR and action != NULL_VAR \
      and relation != NULL_VAR and value != NULL_VAR:
        return ReadSegmentAsRelation(nar, seg)

    if relation != NULL_VAR:
        return ReadSegmentAsAttribute(nar, seg)

        # check encoded operator "events"
    if action == VAR_SO:
        return ReadSegmentAsCausal(nar, seg)

    elif action == VAR_THEN:
        return ReadSegmentAsSequential(nar, seg)

        # check user-defined events
    elif action != NULL_VAR:
        return ReadSegmentAsAction(nar, seg)

    return 0

# In this implementation the ifound's are stored with the vars in the segment
# This makes reading cleaner. The nar gets its ifound filled here.
def ReadSegment0(nar, seg):
    t = isinstance(nar, VAR)
    if not isinstance(nar, VAR):
        return 0

    if len(seg) == 0:
        return 0
    foundNow = False
    for var in seg:
        if var <= nar:
            nar.ifound.extend(var.ifound)
            nar.ifound = cleanFound(nar.ifound)
            nar.found = True
            nar.polarity = var.polarity
            foundNow = True

            if var.isUnknown():#knames[0]=='int' or var.knames[0]=='float':
                nar.lastConst = var.lastConst
            else: # !!!!!!!! THE SEGMENTS IS BUILT WITH VARs not with lastConst's
                nar.lastConst = var.knames[0]  
                
    if foundNow:
        return 1
    else:
        return 0


def ReadSegmentAsAttribute(nar, seg):
    t = ReadSegment(nar.thing, seg)
    v = ReadSegment(nar.value, seg)

    # read any client defined relations
    if nar.relation != NULL_VAR:
        r = ReadSegment(nar.relation, seg)
    else:
        r = ReadSegment0(ATTRIB_OP, seg)

    # a little algorithm to determine polarity of nar.
    T = nar.thing.polarity
    V = nar.value.polarity
    R = nar.relation.polarity
    if v > 0 and V == False:  # a "Bad" value is passed to the nar, regardless of R
        if R:
            nar.polarity = False
        else:
            nar.polarity = True
    elif R == False:  # a "Bad" relation is passed to nar, if that has a meaning
        nar.polarity = False
    elif (v == 0 or v==1) and T == False:  # handling for partial matches
        nar.polarity = False

    nar.generateLastConst()

    return t + v + r


def ReadSegmentAsAction(nar, seg):
    t = ReadSegment(nar.thing, seg)
    a = ReadSegment(nar.action, seg)
    v = ReadSegment(nar.value, seg)

    # a little algorithm to determine polarity of nar.
    # It is the group multiplication on {-1,1}
    C = nar.action.polarity
    A = nar.value.polarity
    if not C and not A:
        nar.polarity = True
    else:
        nar.polarity = C and A

    nar.generateLastConst()

    # require that action be found??? AD HOC
    if a == 0:
        return 0
    else:
        return t + a + v

     # maximizes the "inner" score over all possible subdivisions into tokensA,tokensB
     # Unfortunately you have to do it in both directions


def ReadSegmentAsCausal(nar, seg):
    if nar.action != VAR_SO:
        return 0

    # check for directionality of the SO_OP token
    doFirstPass = True
    doSecondPass = True
    kfound = []
    c = ReadSegment(SO_OP, seg)
    if c > 0:
        if SO_OP.polarity == True:        
            doSecondPass = False
        else:
            doFirstPass = False
    # In the "first pass" we check for the syntax of cause followed by effect:"A so B"
    # In the "second pass" we check for syntax of effect preceeding cause: "B as A"
    # If a SO_OP token is there, it can save time, otherwise we check both syntaxes
    # in two (slow) passes.

    # maximizes the score over all possible subdivisions into tokensA,tokensB
    imax = 0
    maxab = 0
    m = nar.copy()  # to preserve the orginal
    firstPass = True
    if doFirstPass:
        for i in range(len(seg) + 1):
            segA = seg[:i]
            segB = seg[i:]
            m.thing.ifound = []
            m.value.ifound = []
            t = ReadSegment(m.thing, segA)
            v = ReadSegment(m.value, segB)
            c = ReadSegment(SO_OP, seg)

            # favors maximum balanced between the t and v
            if maxab <= (t + 1) * (v + 1):
                imax = i
                maxab = (t + 1) * (v + 1)

    # repeat search in reverse order
    if doSecondPass:
        for i in range(len(seg) + 1):
            segA = seg[:i]
            segB = seg[i:]
            m.value.ifound = []
            m.thing.ifound = []
            v = ReadSegment(m.value, segA)  # (thing and value are swapped)
            t = ReadSegment(m.thing, segB)
            c = ReadSegment(SO_OP, seg)

            # favors maximum balanced between the t and v
            if maxab <= (t + 1) * (v + 1):
                imax = i
                maxab = (t + 1) * (v + 1)
                firstPass = False

    # implement the maximization
    if firstPass:
        segA = seg[:imax]
        segB = seg[imax:]
        t = ReadSegment(nar.thing, segA)
        v = ReadSegment(nar.value, segB)
        c = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC
        T = nar.thing.polarity
        V = nar.value.polarity
#        if (T and V) or (not T and not V):
# Note, I removed the "not" on V
# I did this when a food("cheese,cilantro")
# went to being a food = good("cheese") | bad("cilantro")
# This is a connection too deep to explore for now.
        if v==0 and t>0 :
            nar.polarity = T
        elif t==0 and v>0:
            nar.polarity = V
        elif (T and V) or (not T and V):
            nar.polarity = True
        else:
            nar.polarity = False
    else:
        segA = seg[:imax]
        segB = seg[imax:]
        v = ReadSegment(nar.value,  segA)
        t = ReadSegment(nar.thing, segB)
        c = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC
        V = nar.value.polarity
        T = nar.thing.polarity
        if v==0 and t>0 :
            nar.polarity = T
        elif t==0 and v>0:
            nar.polarity = V
        elif (T and V) or (not T and V):
            nar.polarity = True
        else:
            nar.polarity = False

    nar.generateLastConst()

    x = nar.numSlotsUsed()
    return t + v + c


def ReadSegmentAsSequential(nar, seg):
    if nar.action != VAR_THEN:
        return 0

    imax = 0
    maxab = -1
    m = nar.copy()
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(seg) + 1):
        segA = seg[:i]
        segB = seg[i:]
        m.thing.ifound = []
        m.value.ifound = []
        t = ReadSegment(m.thing, segA)
        v = ReadSegment(m.value, segB)
        a = ReadSegment(AND_OP, seg)

        if maxab < (t + 1) * (v + 1):
            maxab = (t + 1) * (v + 1)
            imax = i
    # implement the max - split the segment optimally
    segA = seg[:imax]
    segB = seg[imax:]

    t = ReadSegment(nar.thing,  segA)
    v = ReadSegment(nar.value, segB)
    a = ReadSegment(AND_OP, seg)  # uses full segment

    # polarity algorithm. Unfortunately AD HOC
    if t > 0 and v == 0:
        nar.polarity = nar.thing.polarity
    elif v > 0 and t == 0:
        nar.polariy = nar.value.polarity
    # else nar.polarity remains at default

    nar.generateLastConst()

    return t + v + a

################################
def ReadSegmentAsRelation(nar, seg):
    t = ReadSegment(nar.thing, seg)
    v = ReadSegment(nar.value, seg)
    r = ReadSegment(nar.relation, seg)
    m = ReadSegment(nar.action, seg) # this is the 'modifier'

    # a little algorithm to determine polarity of nar.
    # NOTE: this is the same as the attribute() algorithm
    # With modifier polarity tacked on at the end
    T = nar.thing.polarity
    V = nar.value.polarity
    R = nar.relation.polarity
    M = nar.action.polarity

    if v > 0 and V == False:  # a "Bad" value is passed to the nar, regardless of R
        if R:
            nar.polarity = False
        else:
            nar.polarity = True
    elif R == False:  # a "Bad" relation is passed to nar, if that has a meaning
        nar.polarity = False
    elif (v == 0 or v==1) and T == False:  # handling for partial matches
        nar.polarity = False

        # the polarity of the modifer is applied externally
    if m>0 and M==False:
        nar.polarity = not nar.polarity


    nar.generateLastConst()

    return t + v + r + m
 
################################
""" 
[This is an earlier version of conversational context that addresses short term context, so
the use of words like "it" and "both" and "difference".]

About SegmentBuffers that used to be implemented in nwcontext.py.
It is for handling "context" - which is defined as past words implictly used
in current sentences. By my lights there are a very limited set of such things, excluding
various personal pronouns that can be assumed absent in a sales-bot application, or can
be brought in later. For now we have these categories of concept:

Positing and juxtpositing mechanisms bring ideas into mind
----------------------------------------------------------
And the basic operations that apply to one or several postited ideas are:
group       (for comparable nouns)
alternate   (for distinct values of an adjective category like color)
merge       (for adjective values from different categories that apply to the same nouns)
sequence    (for nouns in sequence)

The goal of nwcontext [sic] is to support these operations as CONTEXT_OP vars, as you will see.
The plan is: label parents with the above identifiers and look in the past context for
words that share the right sort of parent. For examples, see DIFF usage.
 
"""



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
        newseg = []
        for var in segment:
            if var!= NULL_VAR:
                h = var.copy() 
                h.ifound = [] # protect against bogus indexing
                newseg.append(h)
        self.buffer[ self.next ] = newseg 
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
    return getN(segment,1) 



#######################################################
#######################################################