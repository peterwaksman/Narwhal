from nwutils import *
from nwtypes import *
from nwcontrol import *
from nwvault import *

# works with indexing relative to subtoks
def PlainRead( nar, subtoks):
    jfound = []
    x = ReadText(nar, subtoks, jfound )
    jfound = cleanFound(jfound)  
    return jfound   

## ReadText() and its sub routines implement "plain" reading where
## a narrative is fit to an entire segment of text. This leaves it
## to a higher level to decide when something has been read (based
## on triggers such as all narrative slots being used, or the sentence
## ending, etc...). That is the job of the "higer level" NWReader ("NarReader").
##
## But the plain ReadText() function must be recursive, since NARs are.
## The difficulty is that a provisional concept of goodness of fit
## is needed in order for the two part narratives, sequence() and cause(),
## to be optimally fit to a single piece of text. So I used -basically- the 
## the number of used slots, which is additive and can be returned from subnarratives
## recursively and ALSO the list of ifound[] which also can be returned
## recursively and 'additively' (superposition of lists rather than 
## addition of slot counts). Then the final scoring is postponed to the 
## "higher level" in NWReader, as part of vaulting. See the comments in nwvault.py


######################### READ METHODS ###########
def ReadText(nar, tokens, ifound ):
    if ORDER(nar)==0:
        return ReadText0(nar, tokens, ifound)

    #thing    = nar.thing # used elsewhere
    action   = nar.action
    relation = nar.relation  
    #value    = nar.value # used elsewhere

    if relation!=NULL_VAR:
        return ReadTextAsAttribute(nar, tokens, ifound)

            # check encoded operator "events" 
    if action==NAR_SO:
        return ReadTextAsCausal(nar, tokens, ifound )
    
    elif action==NAR_THEN:
        x=ReadTextAsSequential(nar, tokens, ifound)
        return x
    
            # check user-defined events
    elif action!=NULL_VAR:
        return ReadTextAsAction(nar, tokens, ifound )

    return 0


def ReadText0( nar, tokens, ifound ):   
    if not isinstance(nar, VAR ):
        return 0    
    if len( tokens )==0:
        return 0 

    found = nar.findInText(tokens) # cummulative with nar.ifound set
    # Relay the ifound up the stack. Someone else is responsible
    # for calling nar.clear() - perhaps via the root of the tree
    if found :
        ifound.extend( nar.ifound )
        nar.found = True
        return 1
    return 0  

 

def ReadTextAsAttribute(nar, tokens, ifound ):
    jfound = []

    t = ReadText( nar.thing, tokens, jfound)
    v = ReadText( nar.value, tokens, jfound)

    # read any client defined relations
    if nar.relation != NULL_NAR:
        r = ReadText(nar.relation, tokens, jfound)
    else:    
        ATTRIB_OP.clearIFound()
        r = ReadText0( ATTRIB_OP, tokens, jfound)

    # a little algorithm to determine polarity of nar. [HAD: It ignores nar.thing]
    # and prioritizes the polarity of nar.value 
    V = nar.value.polarity
    R = nar.relation.polarity
    T = nar.thing.polarity
    if v>0 and V==False: # a "Bad" value is passed to the nar, regardless of R
        nar.polarity = False
    elif R==False: # a "Bad" relation is passed to nar, if that has a meaning
        nar.polarity = False
    elif v==0 and T==False: #handling for partial matches
        nar.polarity = False

    ifound.extend(jfound) 

    return t + v + r

def ReadTextAsAction(nar, tokens, ifound):
    jfound = []
  
    t = ReadText(nar.thing, tokens, jfound)
    a = ReadText(nar.action, tokens, jfound)
    v = ReadText(nar.value, tokens, jfound)

    # a little algorithm to determine polarity of nar.
    # It is the group multiplication on {-1,1}
    C = nar.action.polarity
    A = nar.value.polarity
    if not C and not A:
        nar.polarity = True
    else:
        nar.polarity = C and A
        
    ifound.extend(jfound) 
    
    # require that action be found??? AD HOC
    if a==0:
        return 0 
    else:
        return t + a + v
      
    
def ReadTextAsCausal(nar, tokens, ifound):
    if nar.action != NAR_SO: 
        return 0 
   
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    imax = 0
    maxab=0
    m = nar.copy() # to preserve the orginal
    for i in range(len(tokens)+1):
        kfound = []
        tokensA = tokens[:i]
        tokensB = tokens[i:]
        m.thing.clear()
        m.value.clear()
        t  = ReadText(m.thing,  tokensA, kfound)
        v  = ReadText(m.value, tokensB, kfound)
        c  = ReadText(SO_OP, tokens, kfound)
    
        # favors maximum balanced between the t and v
        if maxab<(t+1)*(v+1):
            imax = i
            maxab = (t+1)*(v+1)
            
    tokensA = tokens[:imax]
    tokensB = tokens[imax:]
    
    kfound = []
    nar.clearIFound()
    t  = ReadText(nar.thing,  tokensA, kfound)
    ifound.extend(kfound)

    kfound = []
    nar.clearIFound()
    v  = ReadText(nar.value, tokensB, kfound)
    for i in range(len(kfound)):
        kfound[i] = kfound[i]+imax
    ifound.extend(kfound)
    SO_OP.clear()
    c  = ReadText(SO_OP, tokens, kfound)
    ifound.extend(kfound)

    # polarity algorithm. Unfortunately AD HOC  
    T = nar.thing.polarity
    V = nar.value.polarity
    if (T and V) or (not T and not V):
        nar.polarity = True
    else:
        nar.polarity = False

    return t+v+c

def ReadTextAsSequential(nar, tokens, ifound):
    if nar.action != NAR_THEN: 
        return False
    
    imax = 0
    maxab = -1
    m = nar.copy()
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(tokens)+1):
        kfound = []
        tokensA = tokens[:i]
        tokensB = tokens[i:]
        m.thing.clear()
        m.value.clear()
        t  = ReadText(m.thing, tokensA, kfound)
        v  = ReadText(m.value, tokensB, kfound)
        a  = ReadText(AND_OP, tokens, kfound)
    
        if maxab<(t+1)*(v+1) :
            maxab = (t+1)*(v+1)
            imax = i

    tokensA = tokens[:imax]
    tokensB = tokens[imax:]
   
    kfound = []
    nar.clearIFound()
     
    t  = ReadText(nar.thing,  tokensA, kfound)
    ifound.extend(kfound)

    kfound = []
    nar.clearIFound()

    v  = ReadText(nar.value, tokensB, kfound) #token indices offset by imax
    for i in range(len(kfound)):
        kfound[i] = kfound[i]+imax      
    ifound.extend(kfound)
   
    kfound = []
    a  = ReadText(AND_OP, tokens, kfound) #uses all token indices
    ifound.extend(kfound)

    ifound = cleanFound(ifound)

    # polarity algorithm. Unfortunately AD HOC  
    if t>0 and v==0:
        nar.polarity = nar.thing.polarity
    elif v>0 and t==0:
        nar.polariy = nar.value.polarity
    #else nar.polarity remains at default    

    return t + v + a 



######################################################
################# ABReader ###########################
######################################################
class ABReader:
    def __init__(self, treeroot, nar):
        
          # get our own playground
        self.tree = treeroot.copy()
        self.tree.clear()
        self.nar  = nar.copyUsing( self.tree )
        self.nar.refreshImplicts( False )
        
        self.ifound = [] #indices found in text. A list of variable length
                         
        # during a readText() this keeps a fixed length 
        self.tokens = []
        self.V = NarVault()

    ## encode punctuations, tokenize, and use lower()
    def prepareTokens(self, text): 
        # encode punctuations  
        text = replacePunctuation(text)    
            
        self.ifound = []

         
         # creat lower case tokens 
        tokens = text.split(' ')
        self.tokens = []
        for tok in tokens: 
            if len(tok)>0:
                self.tokens.append(tok)

        for i in range( len(self.tokens)):
            tok = self.tokens[i].lower()
            self.tokens[i] = tok 
 
    def clear(self):
        # fixed, but clear the content
        self.tree.clear()
        self.nar.clear()
        
        # recreated during readText() 
        self.ifound = []   
        self.tokens = []
        # do not clear the vault
    
    def clearStart(self, CD):
        self.nar.clearIFound() 
        self.ifound = []
        # consider appending CD.ctrl.ifound to self.ifound

        # In any case if there was a keyword search it might have consumed
        # more than one token, so use len(CD.ctrl.ifound) to figuure this out.
        # If there was no keyword search, still the control was associated to a token
        # like _comma_ , so you need to advance beyond it also.
        skip =  max(1, len(CD.ctrl.ifound))
        return CD.ictrl + skip

    # Implement the "moving topic" by plain reading between controls
    def readText(self, text, freshStart=True):     
        self.clear()
        if freshStart:
            self.V.clear()  

        self.prepareTokens(text) 
        if len(self.tokens)==0:
            return   

        # for readability 
        nar    = self.nar
        ifound = self.ifound  
        tokens = self.tokens
         
         # look for control data.  
        istart = 0       
        CD  = scanNextControl(tokens, istart)

        while CD.type != END_CTRLTYPE :
              
            #### shift to LOCAL indexing in interval [istart, ictrl] 
            subtoks = tokens[istart : CD.ictrl]
            
            #### PLAIN READ.  
            jfound = PlainRead(nar, subtoks)
            # Shift back to global indices 
            jfound = shiftFoundIndices(jfound, istart )
            cleanFound(jfound)
            self.ifound.extend( jfound )

            #### negate forward or backward, propose and vault, as needed 
            #### and (ifound should be ignored before istart)
            istart = self.applyControl(CD, istart, len(subtoks) )

            #### next control 
            CD = scanNextControl(tokens, istart)
        
        # now CD should be of END_CTRLTYPE
        subtoks= tokens[istart : len(tokens)]
        jfound = PlainRead(nar, subtoks )
        jfound = shiftFoundIndices(jfound, istart )
        ifound.extend(jfound)
        self.ifound = ifound[:]
        self.applyControl( CD, istart, len(subtoks))


    ############################################
    ########### APPLY CONTROL ##################
    ############################################
    # return an updated istart
    def applyControl( self, CD, istart, subrange) :
        if CD.type==NO_CTRLTYPE :
            return istart

        nar = self.nar
        ifound = self.ifound
        tokens = self.tokens
        V = self.V

        if len(ifound)>0:
            record = NarRecord( nar, ifound, tokens, CD.ictrl, subrange )
        else: 
            record = None # I'm told this is "pythonic"
   
        if CD.type==END_CTRLTYPE:
            V.rollUp(record, 0.1) # a more tolerant threshold
            V.vault()
            return len(tokens)


        ########### process the control

        CTRL = CD.ctrl
     
        # this is current "and" processing. It is closely tied to
        # to how "AND" is declared, as a SKIP, or LOGIC OPerator.
        # Take this code out if you want it to SKIP
        # Also consider changing the 0.5 to tune sub-vaulting
        if CTRL.isA("AND"):
            V.rollUp(record, 0.5)
            # no clearing of nar
            istart = self.clearStart(CD)
            return istart

        # other controls:
        if CTRL.isA("NEG") or CTRL.isA("HEDGE"):
            # block backward
            BLOCK = True
            rOK = V.rollUp(record, 0.5, BLOCK) # Indicates pre should be blocked
            if rOK:
                V.vault()
            else:
                V.abandonPre()
            istart = self.clearStart(CD) 
            self.ifound = [] # fresh start

        elif CTRL.isA("FNEG") or CTRL.isA("FHEDGE") :
            rOK = V.rollUp(record, 0.5)
            V.vault()
            istart = self.clearStart(CD)
            # block forward
            V.addBlock()
       
        elif CTRL.isA("COMMA") or CTRL.isA("SEMICOLON"):    
            rOK = V.rollUp( record, 0.5)
            if rOK:
                V.vault()
                #nar.clear() #AD HOC (AND WRONG)
            istart = self.clearStart(CD)
            V.nblocks = 0 
            nar.clearPolarity()

        elif CTRL.isA("PERIOD"):
            rOK = V.rollUp(record, 0.1)
            if rOK:
                V.vault()
            istart = self.clearStart(CD)
            V.nblocks = 0
            nar.clear()

        else :
            print( "did not apply contol: "+ CTRL.knames[0] )

        return istart         

#########################################################
##################### NWReader ##########################
#########################################################    
# The following code, although not identical with the ABReader,
# is supposed to be the same, together with looping over an array
# of nars, each with their own ifound, and vault (i.e. "NarReadData")
# rather than having one nar and managing the ifound and vault in 
# the reader.  
        
######################################################
# The syntax is R = NWReader( tree, nars[] )
#               R.readText( text )
# If you want to reverse polarity of a nar use R.setCalibration()
class NWReader:
    def __init__(self, tree, nars):
        self.tokens = []                              
        self.RD =[] #(R)ead (D)ata
        for nar in nars:
            self.RD.append( NarReadData(tree, nar) )

    def setCalibration(self, calibs):
        for i in range( min( len(self.RD), len(calibs) ) ):
            self.RD[i].calib = calibs[i]
    
    ##### PRIVATELY USED ########### 
    def prepareTokens(self, text): 
            # encode punctuations  
        text = replacePunctuation(text)    
            
             # lower case tokens 
        tokens = text.split(' ')
        self.tokens = []
        for tok in tokens: 
            if len(tok)>0:
                self.tokens.append(tok)

        for i in range( len(self.tokens)):
            tok = self.tokens[i].lower()
            self.tokens[i] = tok 
             
    # how far to skip to restart reading                  
    def newStart(self, CD):
        # If there was a keyword search it might have consumed
        # more than one token, so use len(CD.ctrl.ifound) to figuure this out.
        # If there was no keyword search, still the control was associated to
        # a token like _comma_ , so you need to advance beyond it also.
        skip =  max(1, len(CD.ctrl.ifound))
        return CD.ictrl + skip

    def clearMany( self ):
        for rd in self.RD :
            rd.clear()

    def clearIFoundMany( self ):
        for rd in self.RD :
            rd.clearIFound()
            
    def clearVaults( self ):
         for rd in self.RD :
            rd.V.clear()
                    
    def clearAll(self):
        self.clearMany()
        self.clearIFoundMany()
        self.clearVaults()

    def readMany(self, subtoks, istart):
        for rd in self.RD :
            nar = rd.nar                         
            jfound = PlainRead(nar, subtoks)
            jfound = shiftFoundIndices(jfound, istart )
            cleanFound(jfound)
            rd.ifound.extend( jfound )
            
    def recordMany( self, tokens, ictrl, subrange):
        records = []
        for rd in self.RD:
            if len(rd.ifound)>0:
                record = NarRecord( rd.nar, rd.ifound, tokens, ictrl, subrange)
            else:
                record = None
            records.append( record )
        return records

    # each "rollUp" method works slightly differently. I did not see
    # a better way to generalize ABReader, although maybe...
    def rollUpMany( self, records, Threshold, block=False):
        for i in range( len(self.RD) ):
            RD = self.RD[i]
            RD.V.rollUp( records[i], Threshold, block)

    def rollUpAndVaultMany( self, records, Threshold, block=False):
        for i in range( len(self.RD) ):
            RD = self.RD[i]
            RD.V.rollUp( records[i], Threshold, block)
            self.RD[i].V.vault()
            
    def rollUpCanVaultMany(self, records, Threshold, block=False):
        for i in range( len(self.RD) ):
            rd = self.RD[i]
            rOK = rd.V.rollUp( records[i], Threshold, block)
            if rOK:
                rd.V.vault()
            
    def rollUpCanVaultOrAbandonMany( self, records, Threshold, block=False):
        for i in range( len(self.RD) ):
            rd = self.RD[i]
            rOK = rd.V.rollUp( records[i], Threshold, block)
            if rOK:
                rd.V.vault()
            else:
                rd.V.abandonPre()
            
    def addBlockMany(self):
       for rd in self.RD:
            rd.V.addBlock()            

    def removeAllBlocksMany(self):
        for rd in self.RD:
            rd.V.nblocks = 0
            rd.nar.clearPolarity()

     

        ################################################
        ################## READ  #######################
        ################################################
        # Implement the "moving topic" by plain reading between controls
    def readText(self, text, freshStart=True):     
        if freshStart:
            self.clearAll()

        self.prepareTokens(text) 
        if len(self.tokens)==0:
            return   

        tokens = self.tokens 
         
         # look for control data.  
        istart = 0       
        CD  = scanNextControl(tokens, istart)

        while CD.type != END_CTRLTYPE :              
            subtoks = tokens[istart : CD.ictrl]  

            self.readMany( subtoks, istart )

            istart = self.applyControl(CD, istart, len(subtoks) )

            CD = scanNextControl(tokens, istart)
        
        # now CD should be of END_CTRLTYPE
        subtoks= tokens[istart : len(tokens)]
        self.readMany(subtoks, istart )
        self.applyControl( CD, istart, len(subtoks))


        ################################################# 
        ########### APPLY CONTROL ####################### 
        ################################################# 
        # return an updated istart
    def applyControl( self, CD, istart, subrange) :
        if CD.type==NO_CTRLTYPE :
            return istart

        tokens = self.tokens

            # prepare records for all nars
        records = self.recordMany(tokens, CD.ictrl, subrange)
        if records==None or len(records)==0:
            return istart
   
        if CD.type==END_CTRLTYPE:
            self.rollUpAndVaultMany(records, 0.1)
            return len(tokens)


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

        elif CTRL.isA("PERIOD"):
            self.rollUpCanVaultMany(records, 0.1)
            self.removeAllBlocksMany()      
               
            self.clearMany() # a clean start

        else :
            print( "did not apply contol: "+ CTRL.knames[0] )


        self.clearIFoundMany()
            
        istart = self.newStart(CD)
            
        return istart         

    def report(self):
        out = ""
        for i in range(len(self.tokens)+1):
            if i< len(self.tokens):
                out += self.tokens[i].rjust(10) + " "
            else: 
                out += "END".rjust(10) + " "
            for rd in self.RD:
                r = rd.V.getRecordByCtrl(i)
                if r==None:
                    out += " "
                else:
                    P = r.finalPolarity(rd.calib)
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

