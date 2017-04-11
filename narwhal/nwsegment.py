"""
nwsegment.py implements utilities associated with a "segment" which is
just a plain lists of VARs, without any wrapping. The most important are
    PrepareSegement() -  to convert text-to-tokens-VARs 
    ReadSegment() - the "inner loop" which reads all the text, recursively
    per the hierarchy inside each nar.

The relation between indices in the original tokens of text and indices in
the new "segmented text" is an unhappy one. Various methods try to 
coordinate them: getHi(), getLo(), wordReadRange

"""
# nwsegment.py for handling text segmentation utilities.
# used by the NWSReader. Contains utilities and the inner loop read() methods
from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *


#################################
#################################

# convert text to a segment
def PrepareSegment(tree, tokens):
    tree.clear()
    GENERAL_OP.clear()
    seg = []
    itok = 0
    for itok in range(len(tokens)):
        if (itok in tree.ifound) or (itok in GENERAL_OP.ifound):
            continue
        vars = tree.findInText2(tokens, itok)
        # here we had a single returned var, and no loop in the following
        # now we can findInText2() can return a list of all vars matching here.
        if len(vars) > 0:
            for var in vars:
                var.ifound = cleanFound(var.ifound)
                newvar = var.copy()
                seg.append(newvar)
        else:
            vars = GENERAL_OP.findInText2(tokens, itok)
            if len(vars) > 0:
                for var in vars:
                    var.ifound = cleanFound(var.ifound)
                    newvar = var.copy()
                    seg.append(newvar)
            else:
                seg.append(NULL_VAR)
    return seg

    # a sort of inverse to findInText2()
    # you return with the first var whose ifound contains itok
    # or else return NULL_VAR


def findInSegment(segment, itok):
    for var in segment:
        if itok in var.ifound:
            return var
    return NULL_VAR

  ####################################################
    


def getLo(segment):
    lo = 10000
    for var in segment:
        if var == NULL_VAR:
            continue
        x = max(var.ifound)
        if lo > x:
            lo = x
    return lo


def getHi(segment):
    hi = -1
    for var in segment:
        if var == NULL_VAR:
            continue
        x = max(var.ifound)
        if hi < x:
            hi = x
    return hi


def isInLoHi(nar, lo, hi):
    ifound = nar.getIFound()
    for i in ifound:
        if lo <= i and i <= hi:
            return True
    return False
##################################


def varstring(var):
    if var == NULL_VAR:
        return "?"
    else:
        return var.string(0)


def showSEG(segment, text):
    tokens = prepareTokens(text)
    out = ""
    for itok in range(len(tokens)):
        out += tokens[itok].rjust(10) + " "
        var = findInSegment(segment, itok)
        out += varstring(var) + "\n"
        #out += " "
    return out


def printSEG(segment):
    out = ""
    for var in segment:
        out += varstring(var) + " "
    return out


def getWords(tokens, ifound):
    out = ""
    for i in ifound:
        out += tokens[i] + " "
    return out


def showSEG2(segment, text):
    tokens = prepareTokens(text)
    out = ""
    for var in segment:
        h = ""
        h = varstring(var).rjust(10) + " " + \
            getWords(tokens, var.ifound) + "\n"
        out += h
    return out

################################################
################### inner read loop ############


def ReadSegment(nar, seg):
    if ORDER(nar) == 0:
        return ReadSegment0(nar, seg)

    action = nar.action
    relation = nar.relation

    if relation != NULL_VAR:
        return ReadSegmentAsAttribute(nar, seg)

        # check encoded operator "events"
    if action == NAR_SO:
        return ReadSegmentAsCausal(nar, seg)

    elif action == NAR_THEN:
        return ReadSegmentAsSequential(nar, seg)

        # check user-defined events
    elif action != NULL_VAR:
        return ReadSegmentAsAction(nar, seg)

    return 0

# In this implementation the ifound's are stored with the vars in the segment
# This makes reading cleaner. The nar gets its ifound filled here.
def ReadSegment0(nar, seg):
    if not isinstance(nar, VAR):
        return 0
    if len(seg) == 0:
        return 0
    foundNow = False
    for var in seg:
        if var <= nar:
            nar.ifound.extend(var.ifound)
            nar.ifound = cleanFound(nar.ifound)
            nar.found = True
            nar.polarity = var.polarity
            foundNow = True
    if foundNow:
        return 1
    else:
        return 0


def ReadSegmentAsAttribute(nar, seg):
    t = ReadSegment(nar.thing, seg)
    v = ReadSegment(nar.value, seg)

    # read any client defined relations
    if nar.relation != NULL_NAR:
        r = ReadSegment(nar.relation, seg)
    else:
        r = ReadSegment0(ATTRIB_OP, seg)

    # a little algorithm to determine polarity of nar.
    T = nar.thing.polarity
    V = nar.value.polarity
    R = nar.relation.polarity
    if v > 0 and V == False:  # a "Bad" value is passed to the nar, regardless of R
        if R:
            nar.polarity = False
        else:
            nar.polarity = True
    elif R == False:  # a "Bad" relation is passed to nar, if that has a meaning
        nar.polarity = False
    elif v == 0 and T == False:  # handling for partial matches
        nar.polarity = False

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
    if a == 0:
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
    c = ReadSegment(SO_OP, seg)
    if c > 0:
        if SO_OP.polarity == True:
            
            doSecondPass = False
        else:
            doFirstPass = False
    # In the "first pass" we check for the syntax of cause followed by effect:"A so B"
    # In the "second pass" we check for syntax of effect preceeding cause: "B as A"
    # If a SO_OP token is there, it can save time, otherwise we check both syntaxes
    # in two (slow) passes.

    # maximizes the score over all possible subdivisions into tokensA,tokensB
    imax = 0
    maxab = 0
    m = nar.copy()  # to preserve the orginal
    firstPass = True
    if doFirstPass:
        for i in range(len(seg) + 1):
            segA = seg[:i]
            segB = seg[i:]
            m.thing.ifound = []
            m.value.ifound = []
            t = ReadSegment(m.thing, segA)
            v = ReadSegment(m.value, segB)
            c = ReadSegment(SO_OP, seg)

            # favors maximum balanced between the t and v
            if maxab <= (t + 1) * (v + 1):
                imax = i
                maxab = (t + 1) * (v + 1)

    # repeat search in reverse order
    if doSecondPass:
        for i in range(len(seg) + 1):
            segA = seg[:i]
            segB = seg[i:]
            m.value.ifound = []
            m.thing.ifound = []
            v = ReadSegment(m.value, segA)  # (thing and value are swapped)
            t = ReadSegment(m.thing, segB)
            c = ReadSegment(SO_OP, seg)

            # favors maximum balanced between the t and v
            if maxab <= (t + 1) * (v + 1):
                imax = i
                maxab = (t + 1) * (v + 1)
                firstPass = False

    # implement the maximization
    if firstPass:
        segA = seg[:imax]
        segB = seg[imax:]
        t = ReadSegment(nar.thing, segA)
        v = ReadSegment(nar.value, segB)
        c = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC
        T = nar.thing.polarity
        V = nar.value.polarity
#        if (T and V) or (not T and not V):
# Note, I removed the "not" on V
# I did this when a food("cheese,cilantro")
# went to being a food = good("cheese") | bad("cilantro")
# This is a connection too deep to explore for now.
        if (T and V) or (not T and V):
            nar.polarity = True
        elif v==0:
            nar.polarity = T
        else:
            nar.polarity = False
    else:
        segA = seg[:imax]
        segB = seg[imax:]
        v = ReadSegment(nar.value,  segA)
        t = ReadSegment(nar.thing, segB)
        c = ReadSegment(SO_OP, seg)

        # polarity algorithm. Unfortunately AD HOC
        T = nar.value.polarity
        V = nar.thing.polarity
        if (T and V) or (not T and V):
            nar.polarity = True
        elif t==0:
            nar.polarity = V
        else:
            nar.polarity = False

    x = nar.numSlotsUsed()
    return t + v + c


def ReadSegmentAsSequential(nar, seg):
    if nar.action != NAR_THEN:
        return 0

    imax = 0
    maxab = -1
    m = nar.copy()
    # maximizes the score over all possible subdivisions into tokensA,tokensB
    for i in range(len(seg) + 1):
        segA = seg[:i]
        segB = seg[i:]
        m.thing.ifound = []
        m.value.ifound = []
        t = ReadSegment(m.thing, segA)
        v = ReadSegment(m.value, segB)
        a = ReadSegment(AND_OP, seg)

        if maxab < (t + 1) * (v + 1):
            maxab = (t + 1) * (v + 1)
            imax = i
    # implement the max
    segA = seg[:imax]
    segB = seg[imax:]

    t = ReadSegment(nar.thing,  segA)
    v = ReadSegment(nar.value, segB)
    a = ReadSegment(AND_OP, seg)  # uses full segment

    # polarity algorithm. Unfortunately AD HOC
    if t > 0 and v == 0:
        nar.polarity = nar.thing.polarity
    elif v > 0 and t == 0:
        nar.polariy = nar.value.polarity
    # else nar.polarity remains at default

    return t + v + a

################################


def scanNextControl2(segment, istart):
    CD = ControlData()
    L = len(segment)
    if istart > L - 1:
        CD.set(END_CTRLTYPE, NULL_VAR, L)
        return CD
    for i in range(istart, L):
        var = segment[i]
        if var <= LOGIC_OP:
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

