from nwtypes import *
from nwutils import *

# LOGICAL OPERATORS AND PUNCTUATION ARE CONSIDERED "CONTROLS" THAT AFFECT READING

## I complain about how logicians co-opted natural language terms for their own uses. 
## But Narwhal needs to co-opt the same terms because the terms do, in fact, play a
## basic role in parsing out separate statements and whether the "value" they 
## impart is to be blocked or unblocked. Also help determine when a new statement begins.

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
dullD = KList("DULL",kDULL )
DULL_OP = dullD.var()



# these are separators of sequence
# '-' and '.' may need to be pre-cleaned in the text. YEP
kCONJUNCTIONS= " and , also , then , but also ,but more "



kNEGATIONS = "isn't,wasn't,barely,hardly,unfounded, is not,"
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
kFORWARDHEDGES = "although, even if,despite,instead of,even though,even when,"

kATTRIBUTORS = " with , of , had , hav, has , was, is # not , which , were, is "

kCAUSES = " so , therefore, therefor , because, hence ,room $ for, due to, dueto, as "

# pre conjunctions
kIF = "as $ if "
kNOTONLY = "not only, not just"
#kONLY = "only, just"
kUNLESS = "unless"

# ??? Not sure. The idea was to pre clean the text by removing these keywords.
# It is something you can try to use to control ambiguity
kSKIP = "should not,a little,to hear,working order,screams that,why not,"
"without a problem,without problems"




##################### KList VARs ##################
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

soD = KList("SO", kCAUSES)
SO_OP = soD.var()


attribD = KList( "HAS", kATTRIBUTORS )
ATTRIB_OP = attribD.var()



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
LOGIC_OP.sub(SO_OP)
LOGIC_OP.sub(ATTRIB_OP)
LOGIC_OP.sub(BLOCK_OP)
LOGIC_OP.sub(FWDBLOCK_OP)
LOGIC_OP.sub(PRECONJ_OP)

########################## 
 

def findControl(self, tokens, itok):
    for kname in self.knames:
        klist = KList.instances[ kname ]
        found = klist.findInText(tokens, itok, self.ifound)
        if found:
            #print "really found at ",kname
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
            newtext += " _dot_ "
        elif text[i]==',' :
            newtext += " _comma_ "
        elif text[i]==';' :
            newtext += " _semi_ "
        elif text[i]=='?':
            newtext += " _query_ "
        elif text[i]=="!" :
            newtext += " _hey_ "
        else:
            newtext += text[i]
    return newtext
    

PERIOD_KLIST = KList("PERIOD" , "_dot_")
COMMA_KLIST = KList("COMMA"     , "_comma_")
SEMI_KLIST = KList("SEMICOLON"  , "_semi_")
QUERY_KLIST = KList("QUERY"     , "_query_")
EXCLM_KLIST = KList("EXCLAIM"   , "_hey_")

PERIOD_OP = PERIOD_KLIST.var()
COMMA_OP  = COMMA_KLIST.var()
SEMI_OP   = SEMI_KLIST.var()
QUERY_OP  = QUERY_KLIST.var()
EXCLM_OP  = EXCLM_KLIST.var()

PUNCT_KLIST = KList("PUNCTUATION", "")
PUNCTUATION_OP = PUNCT_KLIST.var()
PUNCTUATION_OP.sub(PERIOD_OP )
PUNCTUATION_OP.sub(COMMA_OP )
PUNCTUATION_OP.sub(SEMI_OP )
PUNCTUATION_OP.sub(QUERY_OP)
PUNCTUATION_OP.sub(EXCLM_OP )

def findPunctuation(self, tokens, itok):
    for kname in self.knames:
        klist = KList.instances[ kname ]
        found = klist.findInText(tokens, itok, self.ifound)
        if found:
            #print "really found at ",kname
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
        LOGIC_OP.clear()
        PUNCTUATION_OP.clear()
 
        if DULL_OP.find(tokens[i]):
            jfound.append(i)

        elif LOGIC_OP.find(tokens[i]):
            jfound.append(i)   

        elif PUNCTUATION_OP.findInText(tokens[i]):
            # do NOT append to jfound. So the punctuation token
            # will not be counted in the numerator of (r/f) in the gof() formula 
            asd  = 1 #remove "compiler warning" squiggles 
    cleanFound(jfound)
    ifound.extend(jfound)
    return ifound
