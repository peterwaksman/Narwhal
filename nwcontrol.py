from nwtypes import *
from nwutils import *

# LOGICAL OPERATORS AND PUNCTUATION ARE CONSIDERED "CONTROLS" THAT AFFECT READING

## I complain about how logicians co-opted natural language terms for their own uses. 
## But Narwhal needs to co-opt the same terms because the terms do, in fact, play a
## basic role in parsing out separate statements and whether the "value" they 
## impart is to be blocked or unblocked. Also they help determine when a new statement begins.

################################## Logic Term Tree

##  At the moment this is a tree whose groupings are more for convenience
## than necessity
## 
##LOGIC_OP()
##    AND_OP( andD )
##    SO_OP( soD )
##    ATTRIB_OP( attribD )
##    BLOCK_OP()
##         GENNEGATION_OP( gennegD )
##         GENHEDGE_OP( genhedgeD )   
##    FWDBLOCK_OP
##         FWDNEGATION_OP( fornegD )
##         FWDHEDGE_OP( forhedgeD )
##    PRECONJ_OP()
##        IF_OP( ifD )
##        NOTONLY_OP(onlyD )
##

# the more thoroughly we list "dull" words to ignore, the more effective
# the word counting, I had "it" listed but choose to put it in the hotel word list.
kDULL = " a , the , an , did "  
dullD = KList("DU",kDULL )
DULL_OP = dullD.var()



# these are separators of sequence
# '-' and '.' may need to be pre-cleaned in the text. YEP
kCONJUNCTIONS= " and , also , then , but also ,but more "



kNEGATIONS = "isn't,wasn't,barely,hardly,unfounded, is not,isnt,"
kNEGATIONS += "avoid,rather than,not so,not true,false,nothing # too|being|was|but,"
kNEGATIONS += " minimum,minimal,neither,forget it,not at all"
kNEGATIONS += "low # volume|floor,or $ less,difficult to be,poor"

# Unfortunately "not" appears in too many places
kFORWARDNEGATIONS = "not to have had to,didn't # need, no ,"
kFORWARDNEGATIONS+= "impossible to,should be,should have,doesn't,doesnt,does not,couldn't # have|believe,"
kFORWARDNEGATIONS+= "bad for,n't # a|need|have|an,"
kFORWARDNEGATIONS+= "not # only|be|have|necessarily|hesitate|so|only|quite|yet|central|available,n&#39;t,didn&#39,didn&#39;t,"
kFORWARDNEGATIONS+= "cannot,could do wit,could do with,werent,wont,dont,no way,"
kFORWARDNEGATIONS+= "lack, difficult to, never ,rarely # find|found,could have,"
kFORWARDNEGATIONS+= "out of # the|their|there|her|his,"
kFORWARDNEGATIONS+= "no # one|matter|fuss|language|charge|problem|issues|problems|time|further," #???
kFORWARDNEGATIONS+= "without # being|a|hesitation|issue|issues|problems" #????

# these need to be sorted into ones that hedge the previous versus ones hedging the folling
kHEDGES = "but # more|also,other than,except,except for,however, yet "
kFORWARDHEDGES = "although, even if,despite,for being,instead of,even though,even when,"

kATTRIBUTORS = " with , of , had , hav, has , was, is # not , are , which , were, is , from the "

# not used yet
kDESIGNATORS = " that , it "
kAMPLIFIERS  = " very "

kCAUSES = " so , therefore, therefor , because, hence ,room $ for, due to, dueto, as ,keep the, kept us"

kCAUSESFWD = " so , therefore, therefor , because, hence ,keep the, kept us"
kCAUSESBKD = "room $ for, due to, dueto, as "


# pre conjunctions
kIF = "as $ if "
kNOTONLY = "not only, not just"
#kONLY = "only, just"
kUNLESS = "unless"

# ??? Not sure. The idea was to pre clean the text by removing these keywords.
# It is something you can try to use to control ambiguity
kSkipThese = "should not,a little,to hear,working order,screams that,why not,"
"without a problem,without problems"




##################### KList VARs ##################
# less common controls that are not currently supported
ifD = KList("IF", kIF )
IF_OP = ifD.var()

notonlyD = KList("NOTJUST",kNOTONLY)
NOTONLY_OP = notonlyD.var()

ifNotD = KList("IFNOT", kUNLESS)
IFNOT_OP = ifNotD.var()

# artificial, inficaed the begining of content that
# is in conjunction with other content - before or after
preconjD = KList("PRECONJ", "" )
PRECONJ_OP = preconjD.var()

andD = KList("AND", kCONJUNCTIONS )
AND_OP = andD.var( )

#soD = KList("SO", kCAUSES)
#SO_OP = soD.var()
fwdCauseD = KList("so", kCAUSESFWD)
bkdCauseD = KList("as", kCAUSESBKD)
SO_OP = fwdCauseD.var() | bkdCauseD.var()
 

attribD = KList( "HAS", kATTRIBUTORS )
ATTRIB_OP = attribD.var()

designatorD = KList( "IT", kDESIGNATORS )
DESIGNATOR_OP = designatorD.var()


gennegD = KList("NEG", kNEGATIONS)
GENNEGATION_OP = gennegD.var()

hedgeD = KList( "HEDGE", kHEDGES )
GENHEDGE_OP = hedgeD.var()

fornegD = KList("FNEG", kFORWARDNEGATIONS)
FWDNEGATION_OP = fornegD.var()

forhedgeD = KList("FHEDGE", kFORWARDHEDGES)
FWDHEDGE_OP = forhedgeD.var()

blockD = KList("BLOCK","")
BLOCK_OP = blockD.var()

fblockD = KList("FBLOCK","")
FWDBLOCK_OP = fblockD.var()
kLOGIC = ""
logicD = KList("LOGIC", kLOGIC)
LOGIC_OP = logicD.var()

skipD = KList("SKIP","")
SKIP_OP = skipD.var()
####################### Tree of VARs ################
#
BLOCK_OP.sub( GENNEGATION_OP )
BLOCK_OP.sub( GENHEDGE_OP )
#
FWDBLOCK_OP.sub( FWDNEGATION_OP )
FWDBLOCK_OP.sub( FWDHEDGE_OP )
#
#PRECONJ_OP = VAR()
PRECONJ_OP.sub( IF_OP )
PRECONJ_OP.sub( NOTONLY_OP)
PRECONJ_OP.sub( IFNOT_OP )
########################
LOGIC_OP.sub(AND_OP)
#LOGIC_OP.sub(SO_OP)
#LOGIC_OP.sub(ATTRIB_OP)
LOGIC_OP.sub(BLOCK_OP)
LOGIC_OP.sub(FWDBLOCK_OP)
LOGIC_OP.sub(PRECONJ_OP)

########################## 
#SKIP_OP.sub(AND_OP)
SKIP_OP.sub(SO_OP)
SKIP_OP.sub(ATTRIB_OP)
SKIP_OP.sub(DESIGNATOR_OP) 


def findControl(self, tokens, itok):
    self.ifound = []
    for kname in self.knames:
        klist = KList.instances[ kname ]
        self.ifound = []
        found = klist.findInText(tokens, itok, self.ifound)
        if found:
            #print( "really found at "+kname)
            self.found = True
            return self
    
    for child in self.children:
        c = findControl(child, tokens, itok)
        if c != NULL_VAR:
           return c

    return NULL_VAR          
  
    
def isLogicControl(tokens, itok):
    return findControl( LOGIC_OP, tokens, itok)

def isDull(tokens, itok):
    DULL_OP.clear()
    tmp = []
    tmp.append(tokens[itok])
    if DULL_OP.findInText(tmp):
        return True
    else:
        return False

######################################################
# PUNCTUATION
# pre process the text, replacing punctuations with unique text "encodings"
# Later these encodings are matched as tokens using the PUNCTUATION var tree
def replacePunctuation( text ):
    begin = 0
    newtext = ""
    for i in range(len(text)):
        if text[i]=='.' :
            newtext += " _period_ "
            noEnd = False
        elif text[i]==',' :
            newtext += " _comma_ "
        elif text[i]==';' :
            newtext += " _semi_ "
        elif text[i]=='?':
            newtext += " _query_ "
        elif text[i]=="!" :
            newtext += " _hey_ "
        elif text[i]=="(":
            newtext += " _(_ "
        elif text[i]==")":
            newtext += " _)_ "
        elif text[i]=="-":
            newtext += " - " # for now
        else:
            newtext += text[i]
    return newtext
    

kPERIOD = KList("PERIOD" , "_period_")
kCOMMA = KList("COMMA"     , "_comma_")
kSEMI = KList("SEMICOLON"  , "_semi_")
kQUERY = KList("QUERY"     , "_query_")
kEXCLM = KList("EXCLAIM"   , "_hey_")
kOPENPAREN = KList("OPENPAREN", "_(_")
kCLOSEPAREN = KList("CLOSEPAREN", "_)_")
kDASH = KList("DASH"," - ")

PERIOD_OP = kPERIOD.var()
COMMA_OP  = kCOMMA.var()
SEMI_OP   = kSEMI.var()
QUERY_OP  = kQUERY.var()
EXCLM_OP  = kEXCLM.var()
OPAREN_OP = kOPENPAREN.var()
CPAREN_OP =  kCLOSEPAREN.var()
DASH_OP = kDASH.var()

kPUNCT = KList("PUNCTUATION", "")
PUNCTUATION_OP = kPUNCT.var()
PUNCTUATION_OP.sub(PERIOD_OP )
PUNCTUATION_OP.sub(COMMA_OP )
PUNCTUATION_OP.sub(SEMI_OP )
PUNCTUATION_OP.sub(QUERY_OP)
PUNCTUATION_OP.sub(EXCLM_OP )
PUNCTUATION_OP.sub(OPAREN_OP )
PUNCTUATION_OP.sub(CPAREN_OP )
#PUNCTUATION_OP.sub(DASH_OP )


def findPunctuation(self, tokens, itok):
    self.ifound = []
    for kname in self.knames:
        klist = KList.instances[ kname ]
        found = klist.findInText(tokens, itok, self.ifound)
        if found:
            #print( "really found at "+kname)
            self.found = True
            return self
    
    for child in self.children:
        c = findControl(child, tokens, itok)
        if c != NULL_VAR:
           return c

    return NULL_VAR          
  
    
def isPunctuationControl(tokens, itok):
    return findControl( PUNCTUATION_OP, tokens, itok)



############################
# The ifound is a list of found token indices. The following serves to insert additional 
# indices into the list whenever there is a dull or contol token BETWEEN indices of ifound
# this sort of adds noise to the signal. Punctuations don't .
def discountControls(tokens, ifound):
    jfound = []
    imin = minITOK(ifound)
    imax = maxITOK(ifound)
    for i in range(imin, imax+1):
        DULL_OP.clear()
        SKIP_OP.clear()
        LOGIC_OP.clear()
        PUNCTUATION_OP.clear()
 
        if DULL_OP.find(tokens[i]):
            jfound.append(i)

        elif LOGIC_OP.find(tokens[i]):
            jfound.append(i)   
        
        elif SKIP_OP.find(tokens[i]):
            jfound.append(i)   

        elif PUNCTUATION_OP.findInText(tokens[i]):
            # do NOT append to jfound. So the punctuation token
            # will not be counted in the numerator of (r/f) in the gof() formula 
            asd  = 1 #remove "compiler warning" squiggles 
    jfound = cleanFound(jfound)
    ifound.extend(jfound)
    return ifound

# Counts controls in the full range of subtoks, excluding ones  
# in the range where words have been found, which are already discounted.
def countUnreadControls(tokens, ifound, ictrl, istart):
    count = 0
    imin = minITOK(ifound)
    imax = maxITOK(ifound)
    for i in range(istart, ictrl): 
        if imin<= i and i<=imax:
            continue
        DULL_OP.clear()
        SKIP_OP.clear()
        LOGIC_OP.clear()
        PUNCTUATION_OP.clear()
 
        if DULL_OP.find(tokens[i]):
            count += 1

        elif LOGIC_OP.find(tokens[i]):
            count += 1
        
        elif SKIP_OP.find(tokens[i]):
            count += 1  

        elif PUNCTUATION_OP.findInText(tokens[i]):
            count += 1

    return count
 

################## prepareTokens() ###################
################## an important method "hiding" here in nwcontrol.py
##################
def prepareTokens( text): 
        # encode punctuations  
    text = replacePunctuation(text)    

        # one of several future cleanups
    text = cleanAMPM(text)
            
            # lower case tokens 
    tokens = text.split(' ')
    newtokens = []
    for tok in tokens: 
        if len(tok)>0:
            newtokens.append(tok)

    for i in range( len(newtokens)):
        tok = newtokens[i].lower()
        newtokens[i] = tok 

    return newtokens

#######################################################    
#######################################################    
### ControlData 
#######################################################    
#######################################################    

# Control types.
NO_CTRLTYPE          = 0       
PUNCTUATION_CTRLTYPE = 1 
OPERATOR_CTRLTYPE    = 2   
END_CTRLTYPE         = 3
SKIP_CTRLTYPE         = 4

class ControlData:
    def __init__(self):
        self.type = NO_CTRLTYPE
        self.ctrl = NULL_VAR
        self.ictrl = -1

    def set(self, type, ctrl, ictrl):
        self.type = type
        self.ctrl = ctrl
        self.ictrl = ictrl
  

# return with ictrl either the index of the control or
# L=len(tokens). Generally read up to <ictrl
def scanNextControl0(tokens, istart):
    CD = ControlData()
    L = len(tokens);
    if istart>L-1:
        CD.set(END_CTRLTYPE, NULL_VAR, L)
        return CD
   
    for itok in range(istart, L):
        ctrl = isLogicControl(tokens,itok)
        if ctrl!=NULL_VAR:
            CD.set(OPERATOR_CTRLTYPE, ctrl, itok)
            return CD
        ctrl = isPunctuationControl(tokens, itok)
        if ctrl!=NULL_VAR:
            CD.set(PUNCTUATION_CTRLTYPE, ctrl, itok)
            return CD

    CD.set(END_CTRLTYPE, NULL_VAR, L)
    return CD

def scanNextControl(vtopic, tokens, istart):
    CD = scanNextControl0(tokens,istart)
    if CD.type==END_CTRLTYPE :
        return CD
    vtopic.clear()
    if not vtopic.detectInText(tokens):
        CD.type = SKIP_CTRLTYPE

    return CD

#################### put it together
kGENERAL = KList("GENERAL"," GEN ")

GENERAL_OP = kGENERAL.var()
GENERAL_OP.sub(LOGIC_OP)
GENERAL_OP.sub(DULL_OP)
GENERAL_OP.sub(SKIP_OP)
GENERAL_OP.sub(PUNCTUATION_OP)

#kCONTROL = KList("CONTROL", " CTRL ")
#CONTROL_OP = kCONTROL.var()
#CONTROL_OP.sub(LOGIC_OP)
#CONTROL_OP.sub(DULL_OP)
#CONTROL_OP.sub(SKIP_OP)




