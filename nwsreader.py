## nwsegment.py for handling text semgentation
#from nwtypes import *  
#from nwutils import *
#from nwcontrol import *
from nwvault import *
from nwsegment import *

def gof2( segment, nar, ifound, imin, imax):
    u = nar.numSlotsUsed()
    n = nar.numSlots()# temp, just to examine in debugger
    av = nar.numSlotsActive()
    r = wordReadCount(segment, ifound, imin, imax)
    f = wordReadRange(segment, ifound, imin, imax)
    ifound = cleanFound(ifound)
    n = av         # deploy the 'implicits'
    n = max(n,2)   # AD HOC? avoid over weighting of single word narratives

    f = max(f,av)   # AD HOC? Now for segments I want this

    if f==0:
        G = 0
    else:
        a = float(u)/float(n) # de-emphasize 1-word matches, for one slot narratives
        b = float(r)/float(f)         
        G = a*b 
    return G

def getSnippet3(tokens, ifound):
    L = len(tokens)
    if L==0 :
        return ""
    ilo = 0
    ihi = 0
    for i in ifound:
        if ilo>i and i<L:
            ilo = i
        if ihi<i and i<L:
            ihi = i
    out = ""  
    for i in range(ilo, ihi+1):
       out += tokens[i] + " "
    
    return out        

####################################################################       
## compatible with NarRecord. Either type can be stored in the vault
class NarSRecord:
    def __init__(self, nar, segment, imin, imax, tokens):
        # imin and imax are segment indices and need translating for use
        # in accessing the tokens array, which is here for informational purposes
        s = nar.getIFound()
        ifound = []
        for i in nar.getIFound():
            if imin<=i and i<=imax:
                ifound.append(i)
        self.ifound = ifound 
#        self.ifound = nar.getIFound()[imin:imax]
        self.snippet = getSnippet3(tokens, self.ifound)

        self.nar = nar.copy()
        self.imin = imin 
        self.imax = imax
        self.block = False    
        self.ictrl = imax 
        #self.GOF = gof( segment, nar, imin, imax)
        self.GOF = gof2(segment, nar, self.ifound, imin, imax)
        self.ifound = cleanFound(self.ifound)
        self.narpolarity = nar.polarity
 
    def block(self):
        self.block = True

    def finalPolarity( self, calib):
        p = self.narpolarity
        if calib: # flip interpretation
            p = not p

        b = self.block
        if b==p:  # it works out as this
            return False
        else:
            return True   
           
  

###################################################################################
#  "NWS" = (N)ar(W)hal (S)egment reader
###################################################################################
class NWSReader:
    # assume the nars are defined using treeroot 
    # The will retains their individual explicit/implicit settings
    def __init__(self,treeroot, nars):
        self.tree = treeroot.copy()
        self.tree.clear()
        self.tree.clearImplicits()
    
        self.nars = nars #[:]

        nar = nars[0]

        self.calibs = []
        self.setCalibration([]) # later you can call set calibs with some 'True' entries

        # for vaulting NarSRecords
        self.vaults = []
        for nar in self.nars:
            self.vaults.append( NarVault() )

        # for recording what is found  
        self.tokens = []
          
    def setCalibration(self, newcalibs):
        self.calibs = []
        for nar in self.nars:        
                self.calibs.append(False)

        for i in range( min( len(self.nars), len(newcalibs) ) ):
            self.calib[i] = newcalibs[i]

    def clearAll(self):
        self.tree.clear()
        GENERAL_OP.clear()
        i = 0
        for nar in self.nars:     
            nar.clear()  
            self.vaults[i].clear() 
        self.tokens = []
             
    def readMany(self, segment):
        for nar in self.nars:
            ReadSegment(nar, segment)
            x = 2
    
    def recordMany( self, segment, imin, imax):
        records = []
        for nar in self.nars:
            s = nar.getIFound()
            g = segment[imin:imax+1]
            lo = getLo(g)
            hi = getHi(g)
            if isInLoHi(nar, lo, hi):
                record = NarSRecord( nar, segment, lo, hi, self.tokens)
            else:
                record = None
            records.append( record )
        return records

    # each "rollUp" method works slightly differently. I did not see
    # a better way to generalize 
    def rollUpMany( self, records, Threshold, block=False):
        for i in range( len(self.nars) ):
            V = self.vaults[i]
            V.rollUp( records[i], Threshold, block)

    def rollUpAndVaultMany( self, records, Threshold, block=False):
        for i in range( len(self.nars) ):
            V = self.vaults[i]
            V.rollUp( records[i], Threshold, block)
            V.vault(Threshold)

    def rollUpCanVaultMany(self, records, Threshold, block=False):
        for i in range( len(self.nars) ):  
            V = self.vaults[i]
            rOK = V.rollUp( records[i], Threshold, block)
            if rOK:
                V.vault(Threshold)
    
    def rollUpCanVaultOrAbandonMany( self, records, Threshold, block=False):
        for i in range( len(self.nars) ):
            V = self.vaults[i]
            rOK = V.rollUp( records[i], Threshold, block)
            if rOK:
                V.vault(Threshold)
            else:
                V.abandonPre()
                nar[i].clearPolarity()
    
    def addBlockMany(self):
       for V in self.vaults:
           V.addBlock()            

    def removeAllBlocksMany(self):
        for i in range (len(self.nars) ): 
            self.vaults[i].nblocks = 0
            self.nars[i].clearPolarity() # comment out AD HOC?
   
    def clearIFoundMany( self ):
        for nar in self.nars :
            nar.clearIFound()

    def clearMany(self):
        for nar in self.nars :
            nar.clear()

    def newStart(self, CD, istart):
        # a control occupies only one index in the segment
        return CD.ictrl + 1
 
    #####################################################
    ##################### outer read loop ###############
    def readText( self, text ):   
        self.clearAll()
        self.tokens = prepareTokens(text)

        segment = prepareSegment( self.tree, self.tokens)
       
        if len(segment)==0:
            return 
     
        istart = 0 # i will be the index of a VAR in the whole segment
        CD = scanNextControl2(segment, istart)

        N = self.nars
        while CD.type != END_CTRLTYPE :
            subseg = segment[istart : CD.ictrl]
            self.readMany(subseg)
            istart = self.applyControl(CD, istart, segment)

            CD = scanNextControl2(segment, istart)
        
        subseg= segment[istart : len(segment)]
        self.readMany(subseg )
        self.applyControl( CD, istart, segment)

    ############################################
    def applyControl(self, CD, istart, segment):
        if CD.type==NO_CTRLTYPE :
            return istart 

            # prepare records for all nars (some can be  "None")
        records = self.recordMany(segment, istart, CD.ictrl)
        if records==None or len(records)==0:
            return istart
   
        if CD.type==END_CTRLTYPE:
            self.rollUpAndVaultMany(records, 0.1)
            return len(segment)


        CTRL = CD.ctrl
    
            # this is current "and" processing. It is closely tied to
            # to how "AND" is declared, as a SKIP, or LOGIC OPerator.
            # Take this code out if you want it to SKIP
            # Also consider changing the 0.5 to tune sub-vaulting
        if CTRL.isA("AND"):
            self.rollUpMany( records, 0.5)
            #self.clearIFoundMany()

        elif CTRL.isA("NEG") or CTRL.isA("HEDGE"):                   
            BLOCK = True  # block backward
            self.rollUpCanVaultOrAbandonMany(records, 0.5, BLOCK)
            #self.clearIFoundMany()

        elif CTRL.isA("FNEG") or CTRL.isA("FHEDGE") :
            self.rollUpAndVaultMany( records, 0.5)
            #self.clearIFoundMany()
            self.addBlockMany()# block forward
       
        elif CTRL.isA("COMMA") or CTRL.isA("SEMICOLON"):
            self.rollUpCanVaultMany( records, 0.5)
            self.removeAllBlocksMany()
            #self.clearIFoundMany()

        # note: no "OPENPAREN" processing yet
        elif CTRL.isA("CLOSEPAREN"):
            self.rollUpCanVaultMany( records, 0.5)
            self.removeAllBlocksMany()
     
        elif CTRL.isA("OPENPAREN"):
            self.rollUpCanVaultMany( records, 0.5)
            self.removeAllBlocksMany()

        elif CTRL.isA("PERIOD") or CTRL.isA("EXCLAIM") or CTRL.isA("DASH"):
            self.rollUpCanVaultMany(records, 0.1)
            self.removeAllBlocksMany()      
               
            self.clearMany() # a clean start

        else :
            print( "did not apply contol: "+ CTRL.knames[0] )
            self.clearIFoundMany()
            self.clearIFoundMany()
            return istart+ max(1, len(CD.ctrl.ifound))

        #self.clearIFoundMany()
            
        istart = self.newStart(CD, istart)
            
        return istart         

  
    def report(self, text):
        tokens = prepareTokens(text)
        out = ""
        L = len(tokens)
        for i in range(len(tokens)+1):
            if i< len(tokens):
                out += tokens[i].rjust(10) + " "
            else: 
                out += "END".rjust(10) + " "
            
            for j in range(len(self.nars)):
                V = self.vaults[j]     # j not i!
                cal = self.calibs[j]
                 
                r = V.getRecordByCtrl2(i) # i not j!
                if r==None:
                    out += " "
                else:
                    P = r.finalPolarity(cal)
                    if P:
                        val = "+"
                    else:
                        val = "-"                  
                    out += val
                if r==None:
                    out += ".      " 
                else:
                    out += ("{0:.4g}".format(r.GOF)).ljust(6) + " "
            out += "\n" 
        out += "\n"
        return out 