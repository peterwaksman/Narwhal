""" 
nwcontrol.py implements the GENERAL_OP tree and the ControlData class.
The VARs in this tree are called "contols". The ones under LOGIC_OP
are called "operators".

It is important to note that the GENERAL_OP tree is re-used frequently 
and volatile member variables of its node's (which are VARs) get overwritten 
frequently.

Logical operators, punctuations, dull words to ignore - all are 
considered types of "controls" that affect reading and are in the 
GENERAL_OP tree. This is Narwhal's version of the boolean operators,
plus other things. It is also Narwhal's version of syntax-n-grammar 
"elements". See nwreader.NWSReader.applyControl() for how the logic is 
interpreted. 
 

Although not up to date, the tree is something like this:

 GENERAL_OP()
     LOGIC_OP()
        AND_OP( andD )
        SO_OP( soD )
        ATTRIB_OP( attribD )
        BLOCK_OP()
             GENNEGATION_OP( gennegD )
             GENHEDGE_OP( genhedgeD )
        FWDBLOCK_OP
             FWDNEGATION_OP( fornegD )
             FWDHEDGE_OP( forhedgeD )
        PRECONJ_OP()
            IF_OP( ifD )
            NOTONLY_OP(onlyD )
    PUNCTUATION_OP()
    SKIP_OP()
        DULL_OP()


 I complain about how logicians co-opted natural language terms for their own uses.
 But Narwhal needs to co-opt the same terms because the terms do, in fact, play a
 basic role in parsing out separate statements and whether the "value" they
 impart is to be blocked or unblocked. Also they help determine when a
 new statement begins - which is never easy to decide.

"""

from narwhal.nwtypes import *
from narwhal.nwutils import *



# Note: the more thoroughly we list "dull" words to ignore, the more effective
# the word counting. I had "it" listed but choose to put it in the hotel
# word list.
kDULL = " a , the , an , did "
dullD = KList("DU", kDULL)
DULL_OP = dullD.var()


# these are separators of sequence
# '-' and '.' may need to be pre-cleaned in the text. YEP
kCONJUNCTIONS = " and , also , then , but also ,but more "


kNEGATIONS = "isn't,wasn't,barely,hardly,unfounded, is not,isnt,don't, do not, doesn't, does not,"
kNEGATIONS += "avoid,rather than,not so,not true,false,nothing # too|being|was|but,"
kNEGATIONS += " minimum,minimal,neither,forget it,not at all"
kNEGATIONS += "low # volume|floor,or $ less,difficult to be,poor"

# Unfortunately "not" appears in too many places
kFORWARDNEGATIONS = "not to have had to,didn't # need, no ,"
kFORWARDNEGATIONS += "impossible to,should be,should have,doesn't,doesnt,does not,couldn't # have|believe,"
kFORWARDNEGATIONS += "bad for,n't # a|need|have|an,"
kFORWARDNEGATIONS += "not # only|be|have|necessarily|hesitate|so|only|quite|yet|central|available,n&#39;t,didn&#39,didn&#39;t,"
kFORWARDNEGATIONS += "cannot,could do wit,could do with,werent,wont,dont,no way,"
kFORWARDNEGATIONS += "lack, difficult to, never ,rarely # find|found,could have,"
kFORWARDNEGATIONS += "out of # the|their|there|her|his,"
kFORWARDNEGATIONS += "no # one|matter|fuss|language|charge|problem|issues|problems|time|further,"  # ???
kFORWARDNEGATIONS += "without # being|a|hesitation|issue|issues|problems"  # ????

# these need to be sorted into ones that hedge the previous versus ones
# hedging the folling
kHEDGES = "but # more|also,other than,except,except for,however, yet "
kFORWARDHEDGES = "although, even if,despite,for being,instead of,even though,even when,"

kATTRIBUTORS = " with , of , had , hav, has , was, is # not , are , which , were, is , from the "

# not used yet
kDESIGNATORS = " that , it "
kAMPLIFIERS = " very "

kCAUSES = " so , therefore, therefor , because, hence ,room $ for, due to, dueto, as ,keep the, kept us"

kCAUSESFWD = " so , therefore, therefor , because, hence ,keep the, kept us, makes me , made me "
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
ifD = KList("IF", kIF)
IF_OP = ifD.var()

notonlyD = KList("NOTJUST", kNOTONLY)
NOTONLY_OP = notonlyD.var()

ifNotD = KList("IFNOT", kUNLESS)
IFNOT_OP = ifNotD.var()

# artificial, inficaed the begining of content that
# is in conjunction with other content - before or after
preconjD = KList("PRECONJ", "")
PRECONJ_OP = preconjD.var()

andD = KList("AND", kCONJUNCTIONS)
AND_OP = andD.var()

#soD = KList("SO", kCAUSES)
#SO_OP = soD.var()
fwdCauseD = KList("so", kCAUSESFWD)
bkdCauseD = KList("as", kCAUSESBKD)
SO_OP = fwdCauseD.var() | bkdCauseD.var()


attribD = KList("HAS", kATTRIBUTORS)
ATTRIB_OP = attribD.var()

designatorD = KList("IT", kDESIGNATORS)
DESIGNATOR_OP = designatorD.var()


gennegD = KList("NEG", kNEGATIONS)
GENNEGATION_OP = gennegD.var()

hedgeD = KList("HEDGE", kHEDGES)
GENHEDGE_OP = hedgeD.var()

fornegD = KList("FNEG", kFORWARDNEGATIONS)
FWDNEGATION_OP = fornegD.var()

forhedgeD = KList("FHEDGE", kFORWARDHEDGES)
FWDHEDGE_OP = forhedgeD.var()

blockD = KList("BLOCK", "")
BLOCK_OP = blockD.var()

fblockD = KList("FBLOCK", "")
FWDBLOCK_OP = fblockD.var()
kLOGIC = ""
logicD = KList("LOGIC", kLOGIC)
LOGIC_OP = logicD.var()

skipD = KList("SKIP", "")
SKIP_OP = skipD.var()

####################### Tree of VARs ##################
#
BLOCK_OP.sub(GENNEGATION_OP)
BLOCK_OP.sub(GENHEDGE_OP)
#
FWDBLOCK_OP.sub(FWDNEGATION_OP)
FWDBLOCK_OP.sub(FWDHEDGE_OP)
#
#PRECONJ_OP = VAR()
PRECONJ_OP.sub(IF_OP)
PRECONJ_OP.sub(NOTONLY_OP)
PRECONJ_OP.sub(IFNOT_OP)
########################
LOGIC_OP.sub(AND_OP)
# LOGIC_OP.sub(SO_OP)
# LOGIC_OP.sub(ATTRIB_OP)
LOGIC_OP.sub(BLOCK_OP)
LOGIC_OP.sub(FWDBLOCK_OP)
LOGIC_OP.sub(PRECONJ_OP)


#######################################################
# SKIP_OP.sub(AND_OP)
SKIP_OP.sub(SO_OP)
SKIP_OP.sub(ATTRIB_OP)
SKIP_OP.sub(DESIGNATOR_OP)


#######################################################
# PUNCTUATION (and other)
# pre process the text, replacing punctuations with unique text "encodings"
# Later these encodings are matched as tokens using the PUNCTUATION var tree
# (or other)

def replaceSpecialChars(text):
    newtext = ""
    for i in range(len(text)):
        # preserve periods with numbers after them.
        # see connection to asFloat()
        if text[i] == '.':
            if i < len(text)-1 and text[i+1].isdigit():
                newtext += '.'
            else:
                newtext += " _period_ "
        elif text[i] == ',':
            newtext += " _comma_ "
        elif text[i] == ';':
            newtext += " _semi_ "
        elif text[i] == '?':
            newtext += " _query_ "
        elif text[i] == "!":
            newtext += " _hey_ "
        elif text[i] == "(":
            newtext += " _(_ "
        elif text[i] == ")":
            newtext += " _)_ "
        elif text[i] == "-":
            if i<len(text)-1 and text[i+1].isdigit():
                newtext += "-" # leave it alone
            else:
                newtext += " - "  # for now
        elif text[i] == "#":
            newtext += " _hash_ " #(not a punctuation)
        else:
            newtext += text[i]
    return newtext



kPERIOD = KList("PERIOD", "_period_")
kCOMMA = KList("COMMA", "_comma_")
kSEMI = KList("SEMICOLON", "_semi_")
kQUERY = KList("QUERY", "_query_")
kEXCLM = KList("EXCLAIM", "_hey_")
kOPENPAREN = KList("OPENPAREN", "_(_")
kCLOSEPAREN = KList("CLOSEPAREN", "_)_")
kDASH = KList("DASH", " - ")

PERIOD_OP = kPERIOD.var()
COMMA_OP = kCOMMA.var()
SEMI_OP = kSEMI.var()
QUERY_OP = kQUERY.var()
EXCLM_OP = kEXCLM.var()
OPAREN_OP = kOPENPAREN.var()
CPAREN_OP = kCLOSEPAREN.var()
DASH_OP = kDASH.var()

kPUNCT = KList("PUNCTUATION", "")
PUNCTUATION_OP = kPUNCT.var()
PUNCTUATION_OP.sub(PERIOD_OP)
PUNCTUATION_OP.sub(COMMA_OP)
PUNCTUATION_OP.sub(SEMI_OP)
PUNCTUATION_OP.sub(QUERY_OP)
PUNCTUATION_OP.sub(EXCLM_OP)
PUNCTUATION_OP.sub(OPAREN_OP)
PUNCTUATION_OP.sub(CPAREN_OP)
#PUNCTUATION_OP.sub(DASH_OP )





#######################################################
# put it together

kGENERAL = KList("GENERAL", " GEN ")

GENERAL_OP = kGENERAL.var()
GENERAL_OP.sub(LOGIC_OP)
GENERAL_OP.sub(DULL_OP)
GENERAL_OP.sub(SKIP_OP)
GENERAL_OP.sub(PUNCTUATION_OP)


#######################################################
# Control types.
NO_CTRLTYPE = 0
PUNCTUATION_CTRLTYPE = 1
OPERATOR_CTRLTYPE = 2
END_CTRLTYPE = 3
SKIP_CTRLTYPE = 4


class ControlData:
    """
    The ControlData class keeps track of the relation between token indices
    and the operators during reading.
    """
    def __init__(self):
        self.type = NO_CTRLTYPE
        self.ctrl = NULL_VAR
        self.ictrl = -1

    def set(self, type, ctrl, ictrl):
        self.type = type
        self.ctrl = ctrl
        self.ictrl = ictrl

def separateMM(text):
    h = len(text)
    if h < 3:
        return text
    
    newtext = ""
    c = text[0]
    newtext += c
    for i in range(1, len(text)-1):
        if text[i]=='m' and text[i+1]=='m' and c.isdigit():
            newtext += " "   
        c = text[i]
        newtext += c
    newtext += text[len(text)-1]

    # TODO: check for decimal point preceeding an "mm", and insert one if needed
    # helps disambiguate ints that are intended as floats

    return newtext       


def cleanDecimals(text):
    if len(text)==0:
        return
    newtext = ""
    for i in range(0, len(text)-1):
        if text[i]=='.' and text[i+1].isdigit():
            if i==0 or not text[i-1].isdigit():
                newtext += '0'  
        newtext += text[i]
    newtext += text[len(text)-1]
    return newtext    

####################################################
def isInteger(tok):
    if len(tok)==0:
        return False
    if tok[0]=='+' or tok[0]=='-':
        tmp = tok[1:]
    else:
        tmp = tok
    for c in tmp:
        if not c.isdigit():
            return False
    return True
def ensureFloatBeforeMM(tokens):
    for i in range(1, len(tokens)):
        tok = tokens[i]
        prev = tokens[i-1]
        if tok=='mm' and isInteger(prev):
            tokens[i-1] = prev + ".0"
    return tokens



#######################################################
def prepareTokens(text):
    if len(text)==0:
        return ''
    """
    An important method. It is "hiding" here in nwcontrol.py. This is
    the opportunity for "pre-processing".
    """

        # encode special chars
    text = replaceSpecialChars(text)

    # one of several future cleanups
    text = cleanAMPM(text)

    # put space before an "mm"
    text = separateMM(text)

    # insert 0 before decimal
    text = cleanDecimals(text)

    # make lower case tokens
    tokens = text.split(' ')
    newtokens = []
    for tok in tokens:
        if len(tok) > 0:
            newtokens.append(tok)  

    for i in range(len(newtokens)):
        tok = newtokens[i].lower()
        newtokens[i] = tok

    newtokens = ensureFloatBeforeMM(newtokens)

    return newtokens

