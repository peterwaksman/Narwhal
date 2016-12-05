from nwtypes import * # brings in nwutils and nwfind
from nwutils import *
from nwcontrol import *

# The "vault" (NarVault below) is a repository for instances of a 
# narrative, encountered in the course of reading a text. 
# It consists of an array of NarRecords.

# for convenience, the nar record includes the relevant snippet of original text
def getSnippet(ifound, tokens):
     if len(ifound)<1:
         return ""
     imin = minITOK(ifound)
     imax = maxITOK(ifound)
     snippet = tokens[imin:imax+1]
     return snippet
 
# The NarRecord reflects a collapsing of the data that has been kept 
# as separate count of numSlotsUsed() and ifound (the indices of found tokens) 
# during the reading process. These get scored and perhaps saved or "vaulted".
# There is a poetic analogy with how superposition of waves is
# additive until an event is observed. Events are not additive. In any case,
# the creation of a record and vaulting are an event. GOF means "goodness of fit" 
# between narrative and text

class NarRecord:
    def __init__(self, nar, ifound, tokens, ictrl, subrange):
        self.snippet = getSnippet(ifound,tokens)
        self.nused = nar.numSlotsUsed()   # num slots used in nar, since nar.clear() erases this info.
        self.nslots = nar.numSlots()      # keep for convenience
        self.ifound = ifound[:]           # indices that have already been read  
        self.block = False
        self.GOF = self.gof(tokens, subrange)
        self.narpolarity = nar.polarity   # nar could change, so save its current polarity
        self.ictrl = ictrl

    def block(self):
        self.block = True

        # "goodness of fit"
        # the subrange is the length of the subtokens used for this ifound
        # Not same as tokens
    def gof(self, tokens, subrange):  
        L = len(tokens)
        jfound = discountControls(tokens, self.ifound)
        jfound = cleanFound(jfound)
        r = histo( jfound, L )
        f = getFoundRange(jfound,L)

        u = self.nused # a snapshot of state when the NarRecord is created
        n = self.nslots 

        if f==0 or n==0:
            G = 0
        else:
            a = float(u)/float(n)
            b = float(r)/float(f)
            c = float(r)/float( subrange )
            G = a*b*c
             
        return G

    def finalPolarity( self, calib):
        p = self.narpolarity
        if calib: # flip interpretation
            p = not p

        b = self.block
        if b==p:  # it works out as this
            return False
        else:
            return True             

# This is currently defined in terms of the above NarRecord. 
# Probably it could be more general.
class NarVault:
    def __init__(self):
        self._vault = []         
        self.pre   = 0
        self.nblocks = 0

# self.pre is or will be what is proposed for vaulting. 
# It is "previous" to vaulting.
# You can block self.pre before or after you encounter the nar
# that proposes data into it. This gives rise to awkward phrases like
# "pre-preblocking" and "post-preblocking". The point is that
# Pre can be blocked while still empty, eg when you see "although".

    def clear(self):
        self._vault = []
        self.pre   = 0
        self.nblocks = 0 
          
    def vault(self):
        if self.pre!=0 and self.pre.GOF>0.1:
            # Apply blocks. Although polarity of a nar need
            # not behave like a boolean, the blocks arising from 
            # controls perhaps DO behave like booleans
            if 1==self.nblocks%2: 
                self.pre.block = True 
            self._vault.append( self.pre )    
        self.pre = 0
        # resetting nblocks is someone else's job     
                                   
    def abandonPre(self):
        self.pre = 0
        
    def addBlock(self):
        self.nblocks = self.nblocks+1 
         
    def removeBlock(self):  
        if self.nblocks>0:
            self.nblocks = self.nblocks-1 

    def rollUp( self, record, Threshold, block=False):
        self.vault()

        if block:
            self.addBlock()

        if record!=None and record.GOF>Threshold:
            self.vault() # saves old pre, as needed
            self.pre = record
            return True
        else:
            return False

        # Retrieve a record with specified ictrl.
        # Given way vault is created, at most one is possible 
    def getRecordByCtrl( self, ictrl):
        for r in self._vault:
            if r.ictrl==ictrl:
                return r
        return None

### This is a class manages the nar and related "found" information
### after a read
### It relieves some of the complexity of the NarReader. 
### It is a nar plus ifound and Vault
class NarReadData:
    def __init__(self, treeroot, nar ):
        self.tree = treeroot.copy()
        self.nar = nar.copyUsing( self.tree )
        self.calib = False

        self.ifound = []
        self.V = NarVault()

    def clearIFound(self):
        self.nar.clearIFound()
        self.ifound = []

    def clear(self):
        self.clearIFound()
        self.nar.clear()

    def finalPolarity(self, r):
        p = r.narpolarity
        if self.calib: # flip interpretation
            p = not p

        b = r.block
        if b==p:  # it works out as this
            return False
        else:
            return True             