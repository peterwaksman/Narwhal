
from nwutils import *
from nwtypes import *
from nwcontrol import *
from nwvault import *

# works with indexing relative to subtoks
def PlainRead( nar, subtoks):
    jfound = []
    ReadText(nar, subtoks, jfound )
    cleanFound(jfound)  
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

    # a little algorithm to determine polarity of nar. It ignores nar.thing
    # and prioritizes the polarity of nar.value 
    V = nar.value.polarity
    R = nar.relation.polarity
    if V==False: # a "Bad" value is passed to the nar, regardless of R
        nar.polarity = False
    elif R==False: # a "Bad" relation is passed to nar, if that has a meaning
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
    
    return t + a + v
      
    
def ReadTextAsCausal(nar, tokens, ifound):
    if nar.action != NAR_SO: 
        return 0 

    imax = 0
    maxab=0
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(tokens)):
        kfound = []
        tokensA = tokens[:i]
        tokensB = tokens[i:]
        nar.thing.clear()
        nar.value.clear()
        t  = ReadText(nar.thing,  tokensA, kfound)
        v  = ReadText(nar.value, tokensB, kfound)
        c  = ReadText(SO_OP, tokens, kfound)
    
        # favors maximum balanced between the t and v
        if maxab<t*v :
            imax = i
            maxab = t*v
            
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

    return t+v+c

def ReadTextAsSequential(nar, tokens, ifound):
    if nar.action != NAR_THEN: 
        return False
    
    imax = 0
    maxab = -1
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(tokens)):
        kfound = []
        tokensA = tokens[:i]
        tokensB = tokens[i:]
        nar.thing.clear()
        nar.value.clear()
        t  = ReadText(nar.thing, tokensA, kfound)
        v  = ReadText(nar.value, tokensB, kfound)
        a  = ReadText(AND_OP, tokens, kfound)
    
        if maxab<t*v :
            maxab = t*v
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
    return t + v + a 


############# TRIGGERS are events that follow from reading ONE token.
# Typically a trigger is a "control" - a logical operator or a punctuation 
# For example ',' and 'and' have much in common. I don't like the idea because 
# it reminds me that code implementation is sequential but reality is more parallel


# Define trigger types.
NO_TRIGGER = -1      # use to check if type>=0
FORGET_TRIGGER = 0   # means enough words have gone to cut our losses and start again
COMPLETE_TRIGGER = 1 # when numSlotsUsed()==numSlots()
CONTROL_TRIGGER = 2  # when a control word is encountered
PUNCTUATION_TRIGGER = 3 # when punctuation is encountered

def getTrigger(nar, tokens, itok, forget ):

    x = isLogicControl(tokens,itok)
    if x!=NULL_VAR:
        return CONTROL_TRIGGER

    p = isPunctuationControl(tokens,itok)
    if p!=NULL_VAR:
        return PUNCTUATION_TRIGGER

    u = nar.numSlotsUsed()
    n = nar.numSlots()
    if u==n:
        return COMPLETE_TRIGGER

    if u<n: # is this case needed?
        nar.find(tokens[itok])    
        if nar.numSlotsUsed()==n: # means the findInText() found the last slot
            return COMPLETE_TRIGGER

    if forget > 3:
        return FORGET_TRIGGER
    return NO_TRIGGER



######################################################
################# NWReader ###########################
######################################################

class NWReader:
    def __init__(self, treeroot, nar):
        
          # get our own playground
        self.tree = treeroot.copy()
        self.nar  = nar.copyUsing( self.tree )
        
        self.ifound = [] #indices found in text. A list of variable length
                         
        # during a readText() this keeps a fixed length 
        self.tokens = []
        self.V = NarVault()
         
    def clear(self):
        # fixed, but clear the content
        self.tree.clear()
        self.nar.clear()
        
        # recreated during readText() 
        self.ifound = []   
        self.tokens = []
       
    def readText(self, text, restart=True):
        
        # prepare to read
        self.clear()
        if restart:
            self.V.clear() #?? or continue from before.

        text = replacePunctuation(text)     
           
        # lower case:
        readstart = 0 # advances when we complete a vaulting

        self.tokens = text.split(' ')
        # go to lower case
        for i in range( len(self.tokens)):
            tok = self.tokens[i].lower()
            self.tokens[i] = tok 
 
        if len(self.tokens)==0:
            return
            
        nar    = self.nar
        ifound =  self.ifound 
        
        tokens = self.tokens

        eventStr = ""
        oldpol = nar.polarity # to test for changes
        forget = 0            # increments until you get bored and start again
        
        # Implements the "moving topic" by plain reading
        # each initial segment of tokens and observing triggering events  
        for itok in range(len(tokens)):

            # prepare event report
            eventStr += tokens[itok].rjust(10)     
            pol = nar.polarity
            if pol != oldpol :
                oldpol = pol
                eventStr += "-"
            else:
                eventStr += " "

            subtoks = tokens[readstart:itok+1]
     
            # do a full, plain, read of the subtoks
            oldL = len(ifound)
            ReadText(nar, subtoks, ifound )
            ifound = cleanFound(ifound)
            if len(ifound)>oldL:
                forget = 0
                eventStr += "f"
            else:
                forget = forget + 1
                eventStr += " "

            i = itok-readstart #the current index in subtoks          
            
            trigger = getTrigger(nar, subtoks, i, forget)
            
            pre = self.V.pre
            if pre==0:
                preIsComplete = False
                GOF = 0
            else:
                preIsComplete = (pre.nused==nar.numSlots())
                GOF = pre.GOF

            if trigger==NO_TRIGGER:
                if itok==len(tokens)-1 : 
                    if preIsComplete:
                        self.V.vault()
                        eventStr += " V("+str(GOF)+")"
                    self.V.propose(nar, ifound,tokens, readstart)  
                    eventStr += " V("+str(GOF)+")P"
                eventStr += "\n"
                continue
            
            elif trigger==FORGET_TRIGGER :
                eventStr += " frgt"
                if preIsComplete or GOF>0.5:
                    self.V.vault()
                    eventStr += " V("+str(GOF)+")"
                    self.V.propose(nar, ifound,tokens, readstart)
                    eventStr += "P"
                ifound = []   
                nar.clear()    
                forget = 0                              

            elif trigger==COMPLETE_TRIGGER :
                eventStr += " DONE"
                if preIsComplete:
                    self.V.vault()
                    eventStr += " V("+str(GOF)+")"
                # overlays nar on pre if pre is not complete               
                self.V.propose(nar, ifound,tokens, readstart) 
                eventStr += " V("+str(GOF)+")P"
                preIsComplete = True
                ifound = []
                readstart = itok
                nar.clear()
                forget = 0
            
            elif trigger==CONTROL_TRIGGER :
                eventStr += " ctrl"
                x = isLogicControl(subtoks, itok) # can assume not NULL_VAR
                if x.isA("AND"):
                    if preIsComplete or GOF>0.5:
                        self.V.vault()
                        eventStr += " V("+str(GOF)+")"
                        #putting this under an "if" is different from 
                        # BUT/HEDGE and critical
                        ifound = []
                        readstart = itok
                        nar.clearIFound()
                elif x.isA("NEG") or x.isA("HEDGE"):
                    if GOF<=0.5 :
                        self.V.abandonPre()
                    else:
                        self.V.blockPre()
                   
                    if preIsComplete or GOF>0.5:
                        self.V.vault()
                        eventStr += " V("+str(GOF)+")"
                    ifound = []
                    readstart = itok
                    nar.clearIFound()
                    forget = 0

                elif x.isA("FNEG") or x.isA("FHEDGE"):      
                    if GOF<=0.5 :
                        self.V.abandonPre()
                    else:
                        self.V.vault()
                        eventStr += " V("+g+")"
                        V.blockPre() # in anticipation of pre being filled
                else:
                   print("UNHANDLED CONTROL="+x.knames[0]+ " at itok="+str(itok))

            elif trigger==PUNCTUATION_TRIGGER :
                eventStr += " punct"
                p = isPunctuationControl(subtoks, itok)
                if p.isA("COMMA") or p.isA("PERIOD") or p.isA("SEMICOLOMN"):  
                    # for now, everyone uses "AND" processing                              
                    if preIsComplete or GOF>0.5:
                        self.V.vault()
                        eventStr += " V("+str(GOF)+")"
                        # also under an "if" for now
                        ifound = []
                        readstart = itok
                        nar.clearIFound()
                else: # p.isA("SEMICOLON") or p.isA("EXCLAIM"):
                    print("unhandled punctuation")

            # last token processing. For now, borrows from COMPLETE_TRIGGER
            if itok==len(tokens)-1 : 
                if preIsComplete:
                    self.V.vault()
                    eventStr += " V("+str(GOF)+")"
                self.V.propose(nar, ifound,tokens, readstart)  
                eventStr += " V("+str(GOF)+")P"
                #GOF = pre.gof(nar,subtoks)      
                #ifound = []
                #readstart = itok
                #nar.clear()
            eventStr += "\n"

        self.V.vault()
        print(eventStr)
        
        print("Vault has " +  str(len(self.V._vault)) + "entries" )
        for v in self.V._vault:
            G = v.gof(tokens)
            print("GOF=" + str(G))
            
######################################################
################# ABReader ###########################
######################################################
class ABReader:
    def __init__(self, treeroot, nar):
        
          # get our own playground
        self.tree = treeroot.copy()
        self.nar  = nar.copyUsing( self.tree )
        
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
        self.tokens = text.split(' ')
       
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
       
    
    # Implement the "moving topic" by plain reading between controls
    def readText(self, text, freshStart=True):     
        self.clear()
        if freshStart:
            self.V.clear()  

        self.prepareTokens(text) 
        if len(tokens)==0:
            return   

        # for readability 
        nar    = self.nar
        ifound = self.ifound  
        tokens = self.tokens
         
        istart = 0  
        # look for control data.  
        CD  = scanNextControl(tokens, istart)
        
        while CD.type != END_CTRLTYPE :
            
            #### shift to LOCAL indexing in interval [istart, ictrl] 
            subtoks = tokens[istart : CD.ictrl]
            
            #### PLAIN READ. Then shift back to global indices 
            jfound = PlainRead(nar, subtoks)
            shiftFoundIndices(jound, istart )
            ifound.append(jfound)

            #### negate forward or backward, propose and vault, as needed 
            #### and (ifound should be ignored before istart)
            istart = applyControl(CD, nar, ifound, tokens, istart, self.V )

            #### next control 
            CD = scanNextControl(tokens, istart)
        
        # now CD should be of END_CTRLTYPE
        subtoks= tokens[istart : len(tokens)]
        jfound = PlainRead(nar, subtoks )
        shiftFoundIndices(jound, istart )
        ifound.append(jfound)
        applyControl( CD, nar, ifound, tokens, istart, self.V )


def rollUp( block, vault, record, Threshold ):
    if record.GOF>Threshold:
        V.vault()
        V.pre = record
        if block: # no double negatives
            V.pre.blocked = True
def clearStart(CD, nar, ifound):
    nar.iclear()
    ifound = []
    return CD.ictrl

# return an updated "istart"
def applyControl( CD, nar, ifound, tokens, istart, V) :

    block = False
    record = NarRecord( nar, ifound, tokens )

    rOK = record.GOF>0.5

    if CD.type==NO_CTRLTYPE :
        return istart

    elif CD.type==END_CTRLTYPE:
        rollUp(block, V, record, 0.1) # a more tolerant saving
        V.vault()
        return len(tokens)

    if CD.type==OPERATOR_CTRLTYPE:       
        op = CD.ctrl        
        if op.isA("NEG") or op.isA("HEDGE"):
            # block backward
            block = True
            rollUp(block, V, record, 0.5)
            if rOK:
                V.vault()
            else:
                V.abandonPre()

            istart = clearStart(CD, nar, ifound) 

        elif op.isA("FNEG") or op.isA("FHEDGE") :
            rollUp(block, V, record, 0.5)
            if rOK:
                V.vault()
            else:
                V.abandonPre()

            istart = clearStart(CD,nar,ifound)

            # block forward
            V.blockPre()

        elif op.isA("AND"):
            rollUp(block, V, record, 0.5)
            if rOK:
                V.vault()
                istart = clearStart(CD,nar,ifound)

    elif CD.type==PUNCTUATION_CTRLTYPE:       
        punct = CD.ctrl
        
        if punct.isA("COMMA") or punct.isA("SEMICOLON"):    
            rollUp(block, V, record, 0.5)
            if rOK:
                V.vault()
                istart = clearStart(CD,nar,ifound)
        elif punct.isA("PERIOD"):
            rollUp(block, V, record, 0.5)
            if rOK:
                V.vault()
                istart = clearStart(CD,nar,ifound)
            if rOK and record.nused==record.nslots:
                nar.clear()

    else :
        print( "unhandled control in applyControl()" )
        return istart

