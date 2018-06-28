import sys


def PythonMajorVersion():
    return int(sys.version[0])



# Thanks to Gringo Suave:
# to call a function of one variable and redirect ouput
def sendToFileA(printFn, a):
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f

    printFn(a)

    sys.stdout = orig_stdout
    f.close()

# to call a function of two variables


def sendToFileAB(printFn, a, b):
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f

    printFn(a, b)

    sys.stdout = orig_stdout
    f.close()



def bool32( ):
    array = []
    for i in range(33):
        array.append(False)
    return array

def str32():
    array = []
    for i in range(33):
        array.append('')
    return array



def countBool(array):
    return sum(1 for i in array if i)

def countStr(array):
    ret = 0
    for val in array:
        if len(val)>0:
            ret +=1
    return ret 


################### IFOUND RELATED ################
"""
When a VAR is compared to each "itok" position in a list of tokens, the tokens
involved in the match may include other indices. All are stored in VAR.ifound
which is cleared before hand and then progressively updated as itok is incremented
across the range of token indices. These utilities are used in various places.
"""

def compressFound(T, ifound):
    tmp = [False for _ in range(T)]
    for ifval in ifound:
        if ifval < T:
            tmp[ifval] = True
    return tmp


def expandFound(T, tmp):
    ifound = [i for i in range(T) if tmp[i]]
    return ifound


def countFound0(T, ifound):
    tmp = compressFound(T, ifound)
    count = sum(1 for i in range(T) if tmp[i])
    return count


def countFound(ifound):
    if not ifound:
        return 0
    imax = max(i for i in ifound)

    tmp = compressFound(imax + 1, ifound)
    count = sum(1 for i in range(imax + 1) if tmp[i])
    return count

# assumes a cleanFound(), otherwise it changes you data


def histo(ifound, i):
    if len(ifound) < 1:
        return 0
    ifound = cleanFound(ifound)
    count = sum(1 for j, ifval in enumerate(ifound) if ifval <= i)
    return count


def cleanFound(ifound):
    if len(ifound) < 1:
        return []
    imax = max(i for i in ifound)
    tmp = compressFound(imax + 1, ifound)
    ifound = expandFound(imax + 1, tmp)
    return ifound

def lastIFound(ifound):
    max = -1
    for i in ifound: 
        if max<i :
            max = i
    return max

def minITOK(ifound):
    if not ifound:
        return -1
    return min(i for i in ifound)


def maxITOK(ifound):
    if not ifound:
        return -1
    return max(i for i in ifound)


def getFoundRange(ifound, ithresh):
    if not ifound:
        return 0
    imin = min(i for i in ifound if i <= ithresh)
    imax = max(i for i in ifound if i <= ithresh)
    return imax - imin + 1


def dullCount(ifound, dull, ithresh):
    # same as in getFoundRange()
    if not ifound:
        return 0
    imin = min(i for i in ifound if i <= ithresh)
    imax = max(i for i in ifound if i <= ithresh)

    count = sum(1 for i, d in enumerate(dull) if d and imin <= i <= imax)
    return count



def showFound(tokens, ifound):
    T = len(tokens)
    t = []
    total = []
    tmp = compressFound(T, ifound)
    for i in range(T):
        t = tokens[i]
        if tmp[i]:
            t += "* "
        else:
            t += " "
        total.append(t)
    s = ''.join(total)
    return s



def shiftFoundIndices(ifound, shift):
    for itok in range(len(ifound)):
        ifound[itok] += shift
    cleanFound(ifound)
    return ifound



######################################################
############## PARSING TEXT #####################
######################################################
######################################################
 

def separateMM(text):
    h = len(text)
    if h < 3:
        return text
    
    newtext = ""
    c = text[0]
    newtext += c
    for i in range(1, len(text)-1):
        if ((text[i]=='m' and text[i+1]=='m') or (text[i]=='M' and text[i+1]=='M')) and c.isdigit():
            newtext += " "   
        c = text[i]
        newtext += c
    newtext += text[len(text)-1]

    # TODO: check for decimal point preceeding an "mm", and insert one if needed
    # helps disambiguate ints that are intended as floats

    return newtext       


def cleanAMPM(text):
    L = len(text)
    newtext = ""
    i = 0
    while i < L:
        c = text[i]
        # test for "I am"
        if c == 'I' and i < L - 3 and text[i + 1] == ' ' and text[i + 2] == 'a' and text[i + 3] == 'm':
            newtext += "I_am"
            i += 4
        elif c.isdigit() and i < L - 2:
            d = text[i + 1]
            e = text[i + 2]

            if d.lower() == 'a' and e.lower() == 'm':
                newtext += c + ' ' + 'a' + 'm'
                i += 3
            elif d.lower() == 'p' and e.lower() == 'm':
                newtext += c + ' ' + 'p' + 'm'
                i += 3
            else:
                newtext += c
                i += 1
        else:
            newtext += c
            i += 1

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
        if (tok=='mm' or tok=='MM') and isInteger(prev):
            tokens[i-1] = prev + ".0"
    return tokens



################ Thing(),Action(),Relation(), and Value() ##############
# used to decompose and analyze contents of a NAR, where the lastConst is 
# from its most recent read. One assumes the string is of the form x:y:z:w
# where x, y, z, w could be paren containing something else of the same 4-part
# form.
def separateTARV( str ):
    L = len(str)
    pcount = 0
    splits = []
    if str[0]=='(' and str[L-1]==')':
        tmp = str[1 : L-1]
    else:
        tmp = str
    for i in range( len(tmp) ):
        c = tmp[i]
        if c=='(':
            pcount += 1
        elif c==')':
            pcount -= 1

        # at the separator
        if c == ':' and pcount==0: 
            splits.append( i )

    temp = []
    if len(splits)==3 : # it resolved correctly into 4 pieces
        temp.append( tmp[ 0 : splits[0]] )
        temp.append( tmp[ splits[0]+1 : splits[1]] )
        temp.append( tmp[ splits[1]+1 : splits[2]] )
        temp.append( tmp[ splits[2]+1 : ] )
    return temp

def hasSeparator( lastC ):
        if lastC.find(':') > -1 :
            return True
        else:
            return False

def Thing(lastConst):
    if lastConst=='':
        return ''
    temp = separateTARV(lastConst)
    if len(temp)<4 :
        return ''
    else: 
        return temp[0]

def Action(lastConst):
    if lastConst=='':
        return ''
    temp = separateTARV(lastConst)
    if len(temp)<4 :
        return ''
    return temp[1]

def Relation(lastConst):
    if lastConst=='':
        return ''
    temp = separateTARV(lastConst)
    if len(temp)<4 :
        return ''
    return temp[2]

def Value(lastConst):
    if lastConst=='':
        return ''
    temp = separateTARV(lastConst)
    if len(temp)<4 :
        return ''
    return temp[3]

