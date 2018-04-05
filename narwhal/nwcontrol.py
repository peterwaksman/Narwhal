""" 
nwcontrol.py implements the GENERAL_OP tree and the ControlData class.
The VARs in this tree are called "contols". The ones under LOGIC_OP
are called "operators". 

Since special operators and controls are handled specially during text parsing, 
The prepareTokens() method is implemented here and calls replaceSpecialChars().
It also puts every token in lower case. If you ever want to go to rawtokens and 
only use lowercase tokens in findInText(), then prepareTokens() is the code to 
modify along the way.

It is important to note that the GENERAL_OP tree is re-used frequently 
and volatile member variables of its node's (which are VARs) get overwritten 
frequently. So they are not reliable.

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

####################### Tree of LOGIC VARs ##################
BLOCK_OP.subs([GENNEGATION_OP, GENHEDGE_OP])
FWDBLOCK_OP.subs([FWDNEGATION_OP, FWDHEDGE_OP])
PRECONJ_OP.subs([IF_OP, NOTONLY_OP, IFNOT_OP])
LOGIC_OP.subs([AND_OP, BLOCK_OP, FWDBLOCK_OP, PRECONJ_OP])
SKIP_OP.subs([SO_OP, ATTRIB_OP, DESIGNATOR_OP])

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
DASH_OP = kDASH.var()  # defined here but not included in PUNCTUATION

PUNCTUATION_OP = KList("PUNCTUATION", "").var()
PUNCTUATION_OP.subs([PERIOD_OP, COMMA_OP, SEMI_OP, QUERY_OP, EXCLM_OP, OPAREN_OP, CPAREN_OP ])


########## GENERAL OPERATOR TREE #########################
GENERAL_OP = KList("GENERAL", " GEN ").var()
GENERAL_OP.subs([LOGIC_OP, DULL_OP, SKIP_OP, PUNCTUATION_OP])


######################################################
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


def getControlIFound(segment, imin, imax):
    dullI = OpIFound(segment, DULL_OP, imin, imax)
    logicI = OpIFound(segment, LOGIC_OP, imin, imax)
    skipI = OpIFound(segment, SKIP_OP, imin, imax)

    ifound = []
    ifound.extend(dullI)
    ifound.extend(logicI)
    ifound.extend(skipI)
    cleanFound(ifound)
    return ifound


def opCount(segment, op, imin, imax):
    ifound = OpIFound(segment, op, imin, imax)
    return len(ifound)


def wordReadCount(segment, ifound, imin, imax):
    #ifound = nar.getIFound()
    foundMin = max(imin, minITOK(ifound))
    foundMax = min(imax, maxITOK(ifound))

    # get all the words read
    cfound = getControlIFound(segment, foundMin, foundMax)
    ifound.extend(cfound)
    ifound = cleanFound(ifound)
    # limit between imin and imax
    jfound = ifound
    ifound = []
    for j in jfound:
        if foundMin <= j and j <= foundMax:
            ifound.append(j)

    pcount = opCount(segment, PUNCTUATION_OP, foundMin, foundMax)

    # remove any punctuations
    final = len(ifound) - pcount

#    ifound = cleanIFound(ifound)

    return max(0, final)


def wordReadRange(segment, ifound, imin, imax):
    #ifound = nar.getIFound()
    foundMin = max(imin, minITOK(ifound))
    foundMax = min(imax, maxITOK(ifound))
    pcount = opCount(segment, PUNCTUATION_OP, foundMin, foundMax)
    final = (foundMax - foundMin + 1) - pcount
    # remove any punctuations
    return max(0, final)

#######################################################
    """
    An important method. This is the opportunity for "pre-processing".
     For now my excuse for putting it in nwcontrol is the use of 
     replaceSpecialChars() which is tightly related to _OP processing above.
    """

def prepareTokens(text, rawtokens):
    if len(text)==0:
        return ''

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
            rawtokens.append(tok)

    for i in range(len(newtokens)):
        tok = newtokens[i].lower()
        newtokens[i] = tok

    newtokens = ensureFloatBeforeMM(newtokens)
    rawtokens = ensureFloatBeforeMM(rawtokens)

    return newtokens


def scanNextControl2(segment, istart):
    CD = ControlData()
    L = len(segment)
    if istart > L - 1:
        CD.set(END_CTRLTYPE, NULL_VAR, L)
        return CD
    for i in range(istart, L):
        var = segment[i]
        if var <= LOGIC_OP and not var<=DULL_OP:
            CD.set(OPERATOR_CTRLTYPE, var, i)
            return CD
        elif var <= PUNCTUATION_OP:
            CD.set(PUNCTUATION_CTRLTYPE, var, i)
            return CD
    CD.set(END_CTRLTYPE, NULL_VAR, L)
    return CD


def OpIFound(segment, op, imin, imax):
    ifound = []
    for var in segment:
        if var <= op:
            ifound.extend(var.ifound)

    # only keep those in [imin,imax]
    jfound = []
    for j in ifound:
        if imin <= j and j <= imax:
            jfound.append(j)
    cleanFound(jfound)
    return jfound
