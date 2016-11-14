from nwtypes import * # brings in nwutils and nwfind
from nwutils import *
from nwcontrol import *

# The "vault" (NarVault below) is a repository for instances of a 
# narrative, encountered in the course of reading a text. 
# It consists of an array of NarRecords.

# The NarRecord reflects a collapsing of the data that has been kept 
# as separate count of numSlotsUsed() and ifound (the indices of found tokens) 
# during the reading process. These it gets scored and perhaps saved or "vaulted".
# There is a poetic analogy with how superposition of waves is
# additive until an event is observed. Events are not additive. In any case,
# the vaulting is an event. GOF means "goodness of fit" between narrative 
# and text

class NarRecord:
    def __init__(self, nar, ifound, tokens):
        self.nused = nar.numSlotsUsed()   # num slots used in nar, since nar.clear() erases this info.
        self.nslots = nar.numSlots()      # keep for convenience
        self.ifound = ifound[:]           # indices that have already been read  
        self.block = False
        self.GOF = self.gof(tokens)
        self.narpolarity = nar.polarity   # nar could change, so save its current polarity

    def block(self):
        self.block = True

        # "goodness of fit"
    def gof(self, tokens):  
        L = len(tokens)
        jfound = discountControls(tokens, self.ifound)
        jfound = cleanFound(jfound)
        r = histo( jfound, L )
        f = getFoundRange(jfound,L)

        u = self.nused # a snapshot of state when the NarRecord is created
        u = min(u, len(jfound) )
        n = self.nslots 


        if f==0 or n==0:
            G = 0
        else:
            G = (float(u)/float(n))*(float(r)/float(f))  # one  of several possibilities.
        return G


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
            # apply blocks
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