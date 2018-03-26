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

