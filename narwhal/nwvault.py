"""
nwvault.py implents the NarRecord and the NarVault for storing them.

A key aspect of this is scoring the goodness-of-fit between a nar and
a segement of text. This is the gof() function.   
"""

from narwhal.nwtypes import *  # brings in nwutils and nwfind
from narwhal.nwutils import *
from narwhal.nwsegment import *
from narwhal.nwcontrol import *

def gof(segment, nar, ifound, imin, imax):
    """
    goodness of fit between nar and segment. Uses the indexing
    of tokens from original text, and the imin and imax index in the
    segment.
    """
    u = nar.numSlotsUsed()
    n = nar.numSlots()  # temp, just to examine in debugger
    av = nar.numSlotsActive()
    r = wordReadCount(segment, ifound, imin, imax)
    f = wordReadRange(segment, ifound, imin, imax)
    ifound = cleanFound(ifound)
    n = av         # deploy the 'implicits'
    n = max(n, 2)   # AD HOC? avoid over weighting of single word narratives

    f = max(f,av)   # AD HOC? Now for segments I want this

    if f == 0:
        G = 0
    else:
        # de-emphasize 1-word matches, for one slot narratives
        a = float(u) / float(n)
        b = float(r) / float(f)
        G = a * b
    return G


def getSnippet3(tokens, ifound):
    L = len(tokens)
    if L == 0:
        return ""
    A = min(ifound)
    B = max(ifound)
    out = ""
    for i in range(A,B+1):
        out += tokens[i] + " "

    return out

####################################################################

class NarSRecord:
    """
     The NarSRecord reflects a collapsing of the data that has been kept
     as separate count of numSlotsUsed() and ifound (the indices of found tokens)
     during the reading process. These get scored and perhaps saved or "vaulted".
     There is a poetic analogy with how superposition of waves is
     additive until an event is observed. Events are not additive. In this case,
     the creation of a record and vaulting are an event. GOF means "goodness of fit"
     between narrative and text
    """
    def __init__(self, nar, segment, imin, imax, tokens):
        # imin and imax are segment indices and need translating for use
        # in accessing the tokens array, which is here for informational
        # purposes
        s = nar.getIFound()
        ifound = []
        for i in nar.getIFound():
            if imin <= i and i <= imax:
                ifound.append(i)
        self.ifound = ifound[:]
        self.snippet = getSnippet3(tokens, self.ifound)

        self.nar = nar.copy()
        self.imin = imin
        self.imax = imax
        self.block = False
        self.ictrl = imax
        self.GOF = gof(segment, nar, self.ifound, imin, imax)
        self.ifound = cleanFound(self.ifound)
        self.narpolarity = nar.polarity
        self.lastConst = nar.lastConst

    def block(self):
        self.block = True

    def finalPolarity(self, calib):
        p = self.narpolarity
        if calib:  # flip interpretation
            p = not p

        b = self.block
        if b == p:  # it works out as this
            return False
        else:
            return True

#####################################################

class NarVault:
    """
    The "vault" (NarVault below) is a repository for records of a
    narrative, encountered in the course of reading a text.
    It consists of an array of finalized NarRecords. It also contains
    a preliminary NarRecord called "pre". The "pre" NarRecord is regarded
    as a staging area. This record can still be modified (eg negated) or
    abandoned. At some point, triggered by the client of this code, a 
    "vaulting" event may occur, taking the "pre" and putting into a finalized 
    array where it can no longer be modified.
    
    To "roll up" the vault means to push something new (perhaps a NULL_VAR) 
    into the "pre" staging area, while also pushing what was already in
    the "pre" into the final repository (unless it is NULL_VAR).


    For convenience, the nar record includes the relevant snippet of
    original text. So later the vault can be evaluated by the client.  
    """

    def __init__(self):
        self._vault = []
        self.pre = 0
        self.nblocks = 0

# self.pre is or will be what is proposed for vaulting.
# It is "previous" to vaulting.
# You can block self.pre before or after you encounter the nar
# that proposes data into it. This gives rise to awkward phrases like
# "pre-preblocking" and "post-preblocking". The point is that
# Pre can be blocked while still empty, eg when you see "although".

    def clear(self):
        self._vault = []
        self.pre = 0
        self.nblocks = 0

    def vault(self, Threshold):
        if self.pre != 0 and self.pre.GOF > Threshold:
            # Apply blocks. Although polarity of a nar need
            # not behave like a boolean, the blocks arising from
            # controls perhaps DO behave like booleans
            if 1 == self.nblocks % 2:
                self.pre.block = True
                self.nblocks = 0
            self._vault.append(self.pre)
        elif self.pre!=0:
            self._vault.append(self.pre)
        self.pre = 0
        # resetting nblocks is someone else's job

    def abandonPre(self):
        self.pre = 0
        self.nblocks = 0

    def addBlock(self):
        self.nblocks = self.nblocks + 1

    def removeBlock(self):
        if self.nblocks > 0:
            self.nblocks = self.nblocks - 1

    def rollUp(self, record, Threshold, block=False):
        self.vault(Threshold)

        if record != None:
            if self.nblocks>0:
                block = not block
                self.nblocks = self.nblocks-1

            record.block = block
            self.pre = record
            return True
        else:
            if block:
                self.addBlock()
            return False


        # Retrieve a record with specified ictrl.
        # Given way vault is created, at most one is possible
    def getRecordByCtrl(self, ictrl):
        for r in self._vault:
            if r.ictrl == ictrl:
                return r
        return None

    def getRecordByCtrl2(self, itok):
        for r in self._vault:
            if len(r.ifound) > 0 and max(r.ifound) == itok:
                return r
        return None

    def maxGOF( self ):
        max = 0.0
        for r in self._vault:
            if max < r.GOF :
                max = r.GOF
        return max

    def lastConst( self ):
        maxlen = 0
        ret = ""
        for r in self._vault:
            if maxlen < len(r.lastConst):
                maxlen = len(r.lastConst)
                ret = r.lastConst
        return ret
# This class manages nar and related "found" information after a read
# It is a nar plus ifound plus Vault
# It relieves some of the complexity of the NarReader.


    def tabulate(self, numTokens, cal):
        x = []
        for i in range(numTokens):
            x.append('.')
        for r in self._vault:
            if r.finalPolarity(cal):
                sign = "+"
            else:
                sign = "-"
            i = lastIFound( r.ifound )
            if 0 <= i and i < numTokens:
                #x[i] =  "{0:.4g}".format(r.GOF) + sign
                x[i] =  sign + "{0:.4g}".format(r.GOF) 
                #x[i] +=  " " + r.lastConst
        return x



    ##############################################################
    # recordSlotEvents() is a substitute for vaulting. A step towards
    # the "golden" algorithm but lacking polarity and lacking higher order nar support
    ###############################################################

def delBelow(ifound,istart):
    newfound = []
    for i in ifound:
        if i>=istart:
            newfound.append(i)
    newfound = cleanFound(newfound)
    return newfound
           
def recordSlotEvents0( nar, segment):
    if not isinstance(nar, VAR):
        return None
    r = []
    for var in segment:
        if var<=nar: 
            nar.ifound.extend(var.ifound)
            nar.ifound = cleanFound(nar.ifound)
            nar.found = True
            nar.polarity = var.polarity
            nar.lastConst = var.knames[0]
            r.append( nar.lastConst )
    return r

def recordSlotEvents1(nar, segment):
    r = []
    if ORDER(nar)!=1:
        return r

    nar.clear()
    i = 0
    istart = 0
    T = nar.thing
    A = nar.action
    R = nar.relation
    V = nar.value
    prevConst = nar.lastConst  
    #event = False
    ifound = []
    for var in segment:
        event = False
        if var==NULL_VAR:
            i = i+1
            continue            
          
        if T != NULL_VAR and var<=T:
            event = True
            T.ifound.extend(var.ifound)
            T.ifound = cleanFound(T.ifound)
            T.found = True
            if var.knames[0]=='int':
                T.lastConst = var.lastConst
            else:
                T.lastConst = var.knames[0]
 
        if A != NULL_VAR and var<=A:
            event = True
            A.ifound.extend(var.ifound)
            A.ifound = cleanFound(A.ifound)
            A.Found = True
            if var.knames[0]=='int':
                A.lastConst = var.lastConst
            else:
                A.lastConst = var.knames[0]
 
        if R != NULL_VAR and R != NULL_NAR and var<=R:
            event = True
            R.ifound.extend(var.ifound)
            R.ifound = cleanFound(R.ifound)
            R.found = True
            if var.knames[0]=='int':
                R.lastConst = var.lastConst
            else:
                R.lastConst = var.knames[0]
 
        if V != NULL_VAR and var<=V:
            event = True
            V.ifound.extend(var.ifound)
            V.ifound = cleanFound(V.ifound)
            V.found = True
            if var.knames[0]=='int':
                V.lastConst = var.lastConst
            else:
                V.lastConst = var.knames[0]
      
 
        ifound.extend( T.ifound )
        ifound.extend( A.ifound )
        if R!=NULL_NAR:
            ifound.extend( R.ifound )
        ifound.extend( V.ifound )
        ifound = delBelow( ifound, istart)
 
        ######## SLOT EVENT #########
        if event:
            nar.generateLastConst() 

        if event and prevConst != nar.lastConst: #(for now require a change) 
            prevConst = nar.lastConst      
            u = nar.numSlotsUsed()
            a = nar.numSlotsActive()    
            GOF = gof(segment, nar, ifound, istart, i)
            if u == a :   # here, could test GOF vs a threshold    
                r.append( [ GOF, nar.lastConst] )

                nar.clear()  
                ifound = []
                istart = i         

        # here put AND and COMMA processing
                               
        i += 1
    return r       

# I am going to try to write this so it works when nar is of order 1
def recordSlotEvents(nar,segment):

    r = [] # record to be created
    if nar.order==0 or isinstance( nar, VAR ):
        return recordSlotEvents0(nar,segment)

    elif nar.order==1:
        return recordSlotEvents1(nar,segment)
    
    else:
        print "UNDER CONSTRUCTION"
        # here can compose a slot event for subnar into a single event
        # for higher order.

