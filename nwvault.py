from nwtypes import * # brings in nwutils and nwfind
from nwutils import *
from nwcontrol import *

# The "vault" (NarVault below) is a repository for instances of a 
# narrative, encountered in the course of reading a text. 
# It consists of an array of NarRecords.

# The NarRecord reflects a collapsing of the data that has been kept 
# as separate count of numSlotsUsed() and ifound (the indices of found tokens) 
# during the reading process. Here it gets scored and perhaps saved or "vaulted".
# There is a poetic analogy with how superposition of waves is
# additive until an event is observed. Events are not additive. In any case,
# the vaulting is an event with GOF meaning "goodness of fit" between narrative and text

class NarRecord:
    def __init__(self, nar, ifound, tokens):
        self.nused = nar.numSlotsUsed()   # num slots used in nar, since nar.clear() erases this info.
        self.nslots = nar.numSlots()      # keep for convenience
        self.ifound = ifound[:]           # indices that have already been read  
        self.blocked = False
        self.GOF = self.gof(tokens)

    def block(self):
        self.blocked = True

        # "goodness of fit"
    def gof(self, tokens):  
        u = self.nused; # a snapshot of state when the NarRecord is created
        n = self.nslots 
        L = len(tokens)
        jfound = discountControls(tokens, self.ifound)
        jfound = cleanFound(jfound)
        r = histo( jfound, L )
        f = getFoundRange(jfound,L)
        if f==0 or n==0:
            print("error in NarRecord.gof()")
        else:
            G = (float(u)/float(n))*(float(r)/float(f))  # one  of several possibilities.
            return G


# This is currently defined in terms of the above NarRecord. 
# Probably it could be more general.
class NarVault:
    def __init__(self):
        self._vault = []         
        self.pre   = 0
        self.preblock = False

# self.pre is or will be what is proposed for vaulting. 
# It is "previous" to vaulting.
# You can block self.pre before or after you encounter the nar
# that proposes data into it. This gives rise to awkward phrases like
# "pre-preblocking" and "post-preblocking". The point is that
# Pre can be blocked while still empty, eg when you see "although".

    def clear(self):
        self._vault = []
        self.pre   = 0
        self.preblock = False 
          
    def vault(self):
        #if self.pre.GOF<=0.1:
        #    print( "Aborting vault for lack of fit" )
        if self.pre!=0 and self.pre.GOF>0.1:
            if self.preblock:
                self.pre.block() #apply any pre blockage
            self._vault.append( self.pre )    
            gofStr = str(self.pre.GOF)
        self.pre = 0
        self.preblock = False
                     
    def propose(self, nar, ifound,tokens, istart):
        if len(ifound)==0:
            return;       
        ifound = cleanFound(ifound) 

        # use readstart to adjust relative indices back to absolute ones 
        ifound = shiftFoundIndices(ifound, istart)

        self.pre = NarRecord(nar, ifound, tokens)
               
    def abandonPre(self):
        self.pre = 0
        
    def blockPre(self):
        self.preblock = True 
         
    def unblockPre(self):  
        self.preblock = False

    def rollUp( self, record, Threshold, block=False):
        if record.GOF>Threshold:
            self.vault()
            self.pre = record
            if block: # no double negatives
                self.pre.blocked = True
            return True
        else:
            return False