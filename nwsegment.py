## nwsegment.py for handling text semgentation
from nwtypes import *  
from nwutils import *
from nwcontrol import *
from nwread import *



##################################
#################################


                # Finds VAR matching at itok. Only visit
                # children if no direct match is found
def findInText2( self, tokens, itok):  
    ikname = 0 
    wasFound = False
    for kname in self.knames: # for each name in self's klist         
        klist = KList.instances[ kname ]                
        found = klist.findInText(tokens, itok, self.ifound) 
        if found:
            self.found = True # could have been true already
            # this can switch frequently and reflects the last found token
            if self.exclusive and ikname>0:
                self.polarity = False
            else:
                self.polarity = True   
                                     
            wasFound = True   
                         
        ikname += 1           
     
    # If nothing was found, search iteratively inside the children
    for child in self.children:
        foundC = findInText2( child, tokens , itok)
        if foundC!=NULL_VAR :
            self.foundInChildren = True
            self.ifound.extend( child.ifound )
            self.ifound = cleanFound(self.ifound)
            if not wasFound:
                self.polarity = child.polarity

            return foundC

    if wasFound:
        return self
    else:
        return NULL_VAR



        # convert text to a segment
def prepareSegment( tree, text):
    tree.clear()
    seg = []
    tokens = prepareTokens(text)
    for itok in range( len(tokens) ):
        var = findInText2( tree, tokens, itok) 
        if var!=NULL_VAR:
            newvar = var.copy()
            seg.append(newvar)
        else:
            var = findInText2( GENERAL_OP, tokens, itok)
            if var != NULL_VAR:
                newvar = var.copy()
                seg.append(newvar)
            else:
                seg.append(NULL_VAR) 
                #pads the segment with empty VARs and flags un-recognized words

    return seg

################################################
################### inner read loop ############
def ReadSegment( nar, seg ):
    if ORDER(nar)==0:
        return ReadSegment0(nar, seg)
    
    action   = nar.action
    relation = nar.relation  

    if relation!=NULL_VAR:
        return ReadSegmentAsAttribute(nar, seg)

            # check encoded operator "events" 
    if action==NAR_SO:
        return ReadSegmentAsCausal(nar, seg)
    
    elif action==NAR_THEN:
        return ReadSegmentAsSequential(nar, seg)
    
            # check user-defined events
    elif action!=NULL_VAR:
        return ReadSegmentAsAction(nar, seg)

    return 0

# In this implementation the ifound's are stored with the vars in the segment
# This makes reading cleaner. The nar gets its ifound filled here.
def ReadSegment0( nar, seg ):   
    if not isinstance(nar, VAR ):
        return 0    
    if len( seg )==0:
        return 0 

    foundNow = False

    for var in seg:
        if var<=nar:
            nar.ifound.extend( var.ifound )
            nar.ifound = cleanFound( nar.ifound )
            nar.found = True
            foundNow = True
   
    if foundNow:
        return 1
    else:
        return 0

def ReadSegmentAsAttribute(nar, seg ):
    t = ReadSegment( nar.thing, seg)
    v = ReadSegment( nar.value, seg)

    # read any client defined relations
    if nar.relation != NULL_NAR:
        r = ReadSegment(nar.relation, seg)
    else:    
        r = ReadSegment0( ATTRIB_OP, seg)

    # a little algorithm to determine polarity of nar. 
    T = nar.thing.polarity
    V = nar.value.polarity
    R = nar.relation.polarity
    if v>0 and V==False: # a "Bad" value is passed to the nar, regardless of R
        if R:
            nar.polarity = False
        else:
            nar.polarity = True
    elif R==False: # a "Bad" relation is passed to nar, if that has a meaning
        nar.polarity = False
    elif v==0 and T==False: #handling for partial matches
        nar.polarity = False

    # accumulate the ifounds of children
    #nar.ifound.extend(nar.thing.ifound)
    #nar.ifound.extend(nar.value.ifound)    
    #nar.ifound.extend(nar.relation.ifound)
    #nar.ifound.cleanFound( nar.ifound)  

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
    
    # require that action be found??? AD HOC
    if a==0:
        return 0 
    else:
        return t + a + v

      
     # maximizes the "inner" score over all possible subdivisions into tokensA,tokensB
     # Unfortunately you have to do it in both directions
def ReadSegmentAsCausal(nar, seg):
    if nar.action != NAR_SO: 
        return 0 
   
    # check for directionality of the SO_OP token
    doFirstPass = True
    doSecondPass = True
    kfound = []
    c  = ReadSegment(SO_OP, seg)
    if c>0:
        if SO_OP.polarity==True:
            doSecondPass = False
        else:
            doFirstPass = False
    # In the "first pass" we check for the syntax of cause followed by effect:"A so B"
    # In the "second pass" we check for syntax of effect preceeding cause: "B as A"
    # If a SO_OP token is there, it can save time, otherwise we check both syntaxes
    # in two (slow) passes.
 
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    imax = 0
    maxab=0
    m = nar.copy() # to preserve the orginal
    firstPass = True
    if doFirstPass:
        for i in range(len(seg)+1):
            segA = seg[:i]
            segB = seg[i:]
            m.thing.ifound = []
            m.value.ifound = []
            t  = ReadSegment(m.thing, segA)
            v  = ReadSegment(m.value, segB)
            c  = ReadSegment(SO_OP, seg)
    
            # favors maximum balanced between the t and v
            if maxab<=(t+1)*(v+1):
                imax = i
                maxab = (t+1)*(v+1)

    # repeat search in reverse order
    if doSecondPass:
        for i in range(len(seg)+1):            
            segA = seg[:i]
            segB = seg[i:]
            m.value.ifound = []
            m.thing.ifound = []
            v  = ReadSegment(m.value, segA) #(thing and value are swapped)
            t  = ReadSegment(m.thing, segB)
            c  = ReadSegment(SO_OP, seg)
    
            # favors maximum balanced between the t and v
            if maxab<=(t+1)*(v+1):
                imax = i
                maxab = (t+1)*(v+1)   
                firstPass = False    

    # implement the maximization        
    if firstPass:          
        segA = seg[:imax]
        segB = seg[imax:]
        t  = ReadSegment(nar.thing, segA)
        v  = ReadSegment(nar.value, segB)
        c  = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC  
        T = nar.thing.polarity
        V = nar.value.polarity
        if (T and V) or (not T and not V):
            nar.polarity = True
        else:
            nar.polarity = False
    else:
        segA = seg[:imax]
        segB = seg[imax:]  
        v  = ReadSegment(nar.value,  segA)
        t  = ReadSegment(nar.thing, segB)
        c  = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC  
        T = nar.value.polarity
        V = nar.thing.polarity
        if (T and V) or (not T and not V):
            nar.polarity = True
        else:
            nar.polarity = False

    return t+v+c


def ReadSegmentAsSequential(nar, seg):
    if nar.action != NAR_THEN: 
        return 0
   
    imax = 0
    maxab = -1
    m = nar.copy()
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(seg)+1):
        segA = seg[:i]
        segB = seg[i:]
        m.thing.ifound = []
        m.value.ifound = []
        t  = ReadSegment(m.thing, segA)
        v  = ReadSegment(m.value, segB)
        a  = ReadSegment(AND_OP, seg)
    
        if maxab<(t+1)*(v+1) :
            maxab = (t+1)*(v+1)
            imax = i
    # implement the max
    segA = seg[:imax]
    segB = seg[imax:]
     
    t  = ReadSegment(nar.thing,  segA)
    v  = ReadSegment(nar.value, segB)  
    a  = ReadSegment(AND_OP, seg) #uses full segment

    # polarity algorithm. Unfortunately AD HOC  
    if t>0 and v==0:
        nar.polarity = nar.thing.polarity
    elif v>0 and t==0:
        nar.polariy = nar.value.polarity
    #else nar.polarity remains at default    

    return t + v + a 

################################
def scanNextControl2(segment, istart):
    CD = ControlData()
    L = len(segment);
    if istart>L-1:
        CD.set(END_CTRLTYPE, NULL_VAR, L)
        return CD
    for i in range(istart,L):
        var = segment[i]
        if var<=LOGIC_OP:
            CD.set(OPERATOR_CTRLTYPE, var, i)
            return CD
        elif var<=PUNCTUATION_OP:
            CD.set(PUNCTUATION_CTRLTYPE, var, i)
            return CD
    CD.set(END_CTRLTYPE, NULL_VAR, L)
    return CD 


def OpIFound( segment, op, imin, imax):
    ifound = []
    for var in segment:
        if var <= op:
            ifound.extend( var.ifound )

    # only keep those in [imin,imax]
    jfound = []
    for j in ifound:
        if imin<=j and j<=imax:
            jfound.append(j)
    cleanFound(jfound)
    return jfound

def getControlIFound( segment, imin, imax):
    dullI  = OpIFound(segment, DULL_OP, imin, imax)
    logicI = OpIFound(segment, LOGIC_OP, imin, imax)
    skipI  = OpIFound(segment, SKIP_OP, imin, imax)

    ifound = []
    ifound.extend( dullI )
    ifound.extend( logicI )
    ifound.extend( skipI ) 
    cleanFound( ifound )
    return ifound       

def opCount(segment, op, imin, imax ):
    ifound = OpIFound(segment, op, imin, imax)   
    return len( ifound )

def wordReadCount(segment, nar, imin, imax):
    ifound = nar.getIFound()
    foundMin = max( imin, minITOK(ifound ) )  
    foundMax = min( imax, maxITOK(ifound ) )

    # get all the words read  
    ifound.extend( getControlIFound(segment, foundMin, foundMax ) )
    ifound = cleanFound(ifound)

    pcount = opCount(segment, PUNCTUATION_OP, foundMin, foundMax ) 

    #remove any punctuations
    final = len(ifound) - pcount

    return max(0, final)

def wordReadRange(segment, nar, imin, imax):
    ifound = nar.getIFound()
    foundMin = max( imin, minITOK(ifound ) )  
    foundMax = min( imax, maxITOK( ifound ) )
    pcount = opCount(segment, PUNCTUATION_OP, foundMin, foundMax ) 
    final = (foundMax - foundMin + 1) - pcount
    #remove any punctuations
    return max(0,final)

def gof( segment, nar, imin, imax):
    u = nar.numSlotsUsed()
    n = nar.numSlots()# temp, just to examine in debugger
    av = nar.numSlotsActive()
    r = wordReadCount(segment, nar, imin, imax)
    f = wordReadRange(segment, nar, imin, imax)
    
    n = av         # deploy the 'implicits'
    n = max(n,2)   # AD HOC? avoid over weighting of single word narratives

    if f==0:
        G = 0
    else:
        a = float(u)/float(n) # de-emphasize 1-word matches, for one slot narratives
        b = float(r)/float(f)         
        G = a*b 
    return G


def showSEG( segment ):
    out =  ""
    for var in segment:
        if var==NULL_VAR:
            out += "?"
        else:
            out += var.string(0)
        out += " "
    return out


##############################################
#  "NWS" = NarWhalSegment

class NWSReader:
    # assume the nars are defined using treeroot 
    # The will retains their individual explicit/implicit settings
    def __init__(self,treeroot, nars):
        self.tree = treeroot.copy()
        self.tree.clear()
        self.tree.clearImplicits()
    
        self.nars = nars

        self.calibs = []
        self.setCalibration([]) # later you can call set calibs with some 'True' entries

        # for vaulting NarSRecords
        self.vaults = []
        for nar in self.nars:
            self.vaults.append( NarVault() )

           
    def setCalibration(self, newcalibs):
        self.calibs = []
        for nar in self.nars:        
                self.calibs.append(False)

        for i in range( min( len(self.nars), len(newcalibs) ) ):
            self.calib[i] = newcalibs[i]

    def clearAll(self):
        self.tree.clear()
        i = 0
        for nar in self.nars:     
            nar.clear()  
            self.vaults[i].clear() 
             
    def readMany(self, segment):
        for nar in self.nars:
            ReadSegment(nar, segment)
    
    def recordMany( self, segment, imin, imax):
        records = []
        for nar in self.nars:
            ifound = nar.getIFound()[imin:imax]
            if len(ifound)>0:
                record = NarSRecord( nar, segment, imin, imax)
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
            V.vault()

    def rollUpCanVaultMany(self, records, Threshold, block=False):
        for i in range( len(self.nars) ):  
            V = self.vaults[i]
            rOK = V.rollUp( records[i], Threshold, block)
            if rOK:
                V.vault()
    
    def rollUpCanVaultOrAbandonMany( self, records, Threshold, block=False):
        for i in range( len(self.nars) ):
            V = self.vaults[i]
            rOK = V.rollUp( records[i], Threshold, block)
            if rOK:
                V.vault()
            else:
                V.abandonPre()
                nar[i].clearPolarity()
    
    def addBlockMany(self):
       for V in self.vaults:
           V.addBlock()            

    def removeAllBlocksMany(self):
        for i in range (len(self.nars) ): 
            self.vaults[i].nblocks = 0
            self.nars[i].clearPolarity()
   
    def clearIFoundMany( self ):
        for nar in self.nars :
            nar.clearIFound()

    def newStart(self, CD, istart):
        # a control occupies only one index in the segment
        return CD.ictrl + 1
 
    #####################################################
    ##################### outer read loop ###############
    def readText( self, text ):   
        self.clearAll()
        segment = prepareSegment( self.tree, text)
        if len(segment)==0:
            return 
     
        istart = 0 # i will be the index of a VAR in the whole segment
        CD = scanNextControl2(segment, istart)
        
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

        elif CTRL.isA("NEG") or CTRL.isA("HEDGE"):                   
            BLOCK = True  # block backward
            self.rollUpCanVaultOrAbandonMany(records, 0.5, BLOCK)

        elif CTRL.isA("FNEG") or CTRL.isA("FHEDGE") :
            self.rollUpAndVaultMany( records, 0.5)
            self.addBlockMany()# block forward
       
        elif CTRL.isA("COMMA") or CTRL.isA("SEMICOLON"):
            self.rollUpCanVaultMany( records, 0.5)
            self.removeAllBlocksMany()

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
            return istart+ max(1, len(CD.ctrl.ifound))

        self.clearIFoundMany()
            
        istart = self.newStart(CD, istart)
            
        return istart         

    
## compatible with NarRecord. Either type can be stored in the vault
class NarSRecord:
    def __init__(self, nar, segment, imin, imax):
        #self.snippet = getSnippet2(istart,ictrl,ifound, tokens)
        self.nar = nar.copy()
        self.imin = imin 
        self.imax = imax
        self.GOF = gof( segment, nar, imin, imax)
        self.block = False    

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