from nwtypes import * # brings in nwutils and nwfind
from nwutils import *
from nwcontrol import *
from math import sqrt

# The "vault" (NarVault below) is a repository for instances of a 
# narrative, encountered in the course of reading a text. 
# It consists of an array of NarRecords.

# for convenience, the nar record includes the relevant snippet of original text
def getSnippet(istart, ictrl, tokens):
     if ictrl<=istart:
         return ""
     snippet = tokens[istart:ictrl]
     return snippet
 
 # for convenience, the nar record includes the relevant snippet of original text
 # plus some embelishments
def getSnippet2(istart, ictrl, ifound, tokens):
     if ictrl<=istart:
         return ""

     newtokens = tokens[:]
     for j in range( len(ifound)):
         i = ifound[j]
         newtokens[i] = newtokens[i]+"*"

     snippet = ""
     for i in range(istart,ictrl):
         snippet += newtokens[i]+" "

     return snippet


# The NarRecord reflects a collapsing of the data that has been kept 
# as separate count of numSlotsUsed() and ifound (the indices of found tokens) 
# during the reading process. These get scored and perhaps saved or "vaulted".
# There is a poetic analogy with how superposition of waves is
# additive until an event is observed. Events are not additive. In any case,
# the creation of a record and vaulting are an event. GOF means "goodness of fit" 
# between narrative and text

class NarRecord:
    def __init__(self, nar, ifound, tokens, ictrl, istart):
        self.snippet = getSnippet2(istart,ictrl,ifound, tokens)
        self.nused = nar.numSlotsUsed()   # num slots used in nar, since nar.clear() erases this info.
        self.nslots = nar.numSlots()      # keep for convenience
        self.nactive = nar.numSlotsActive()
        self.ifound = ifound[:]           # indices that have already been read  
        self.block = False
        self.ictrl = ictrl
        self.GOF = self.gof(tokens, istart)
        self.narpolarity = nar.polarity   # nar could change, so save its current polarity

    def block(self):
        self.block = True

        # "goodness of fit"
        # the subrange is the length of the subtokens used for this ifound
        # Not same as tokens
    def gof(self, tokens, istart): 
        L = len(tokens)
        jfound = discountControls(tokens, self.ifound)
        jfound = cleanFound(jfound)
        # (this r counts words and controls in read word range)
        r = histo( jfound, L )
        f = getFoundRange(jfound,L) # same as len(snippet)

        u = self.nused # a snapshot of state when the NarRecord is created
        n = self.nslots
        av = self.nactive
        n = av         # deploy the 'implicits'
        n = max(n,2)   # but de-emphasize single-VAR narratives

        if f==0 or n==0:
            G = 0
        else:
            a = float(u)/float(max(n,2)) # de-emphasize 1-word matches, for one slot narratives
            b = float(r)/float(f)         
            G = a*b 
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
          
    def vault(self,Threshold):
        if self.pre!=0 and self.pre.GOF>Threshold:
            # Apply blocks. Although polarity of a nar need
            # not behave like a boolean, the blocks arising from 
            # controls perhaps DO behave like booleans
            if 1==self.nblocks%2: 
                self.pre.block = True 
                self.nblocks = 0
            self._vault.append( self.pre )    
        self.pre = 0
        # resetting nblocks is someone else's job     
                                   
    def abandonPre(self):
        self.pre = 0
        self.nblocks = 0

    def addBlock(self):
        self.nblocks = self.nblocks+1 
         
    def removeBlock(self):  
        if self.nblocks>0:
            self.nblocks = self.nblocks-1 

    def rollUp( self, record, Threshold, block=False):
        self.vault(Threshold)

        if block:
            self.addBlock()

        if record!=None:
            self.vault(Threshold) # saves old pre, as needed
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
   
    def getRecordByCtrl2( self, itok):
        for r in self._vault:
            if len(r.ifound)>0 and max(r.ifound)==itok:
                return r
        return None
### This is a class manages nar and related "found" information after a read
### It is a nar plus ifound plus Vault
### It relieves some of the complexity of the NarReader. 
class NarReadData:
    def __init__(self, treeroot, nar ):
        self.tree = treeroot.copy()
        self.tree.clear()
        self.tree.clearImplicits()
        self.nar = nar.copyUsing( self.tree )
        #self.nar.refreshImplicits(False) they are refreshed inadvertenly while copyUsing()
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