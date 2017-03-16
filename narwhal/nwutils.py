##from nwtypes import *
##from NoiseTree import *


import sys

def PythonMajorVersion():
    return int( sys.version[0] )


# Thanks to Gringo Suave:
# to call a function of one variable and redirect ouput
def sendToFileA( printFn, a):
    orig_stdout = sys.stdout
    f = file('out.txt', 'w')
    sys.stdout = f

    printFn(a)

    sys.stdout = orig_stdout
    f.close()

# to call a function of two variables
def sendToFileAB( printFn, a, b):
    orig_stdout = sys.stdout
    f = file('out.txt', 'w')
    sys.stdout = f

    printFn(a,b)

    sys.stdout = orig_stdout
    f.close()



def TOKS( text ):
    tokens = text.split(' ')
    return tokens


    # T = numTokens. It is assume ifound is list of indices from
    # in [0, T)
def compressFound( T , ifound ):
    tmp = []
    for i in range( T ):
        tmp.append(False)
    for j in range( len(ifound) ):
        if ifound[j]< T:
            tmp[ ifound[j] ] = True
    return tmp

def expandFound( T, tmp):
    ifound = []
    for i in range(T):
        if tmp[ i ]:
            ifound.append( i )
    return ifound

def countFound0(T, ifound ):
    count = 0
    tmp = compressFound( T, ifound)
    for i in range(T):
        if tmp[i] :
            count += 1
    return count

def countFound(ifound ):
    max = -1
    for i in ifound:
        if max<i:
            max = i
    if max==-1:
        return 0

    count = 0
    tmp = compressFound( max+1, ifound)
    for i in range(max+1):
        if tmp[i] :
            count += 1
    return count

# assumes a cleanFound(), otherwise it changes you data
def histo(ifound,i):
    if len(ifound)<1:
        return 0
    ifound = cleanFound(ifound)
    count = 0
    for j in range(len(ifound)):
        if ifound[j]<=i:
            count += 1
    return count


def cleanFound( ifound ):
    max = -1
    for i in ifound:
        if max<i:
            max = i
    if max==-1:
        return []
    tmp = compressFound( max+1, ifound )
    ifound = expandFound(max+1, tmp )
    return ifound

def getMinMax(ifound, thresh, mlo, mhi ):
    mlo = 3
    mhi = 4

def minITOK(ifound):
    if len(ifound)==0:
        return -1
    imin = 1000000
    for i in ifound:
        if imin>i:
            imin = i
    return imin

def maxITOK(ifound):
    if len(ifound)==0:
        return -1
    imax = 0
    for i in ifound:
        if imax<i:
            imax = i
    return imax

def getFoundRange(ifound, ithresh):
    if len(ifound)==0 :
        return 0
    imin = 3000
    imax = -1
    for j in range( len(ifound) ):
        i = ifound[j]
        if i>ithresh:
            continue
        if imax<i :
            imax = i
        if imin>i :
            imin = i
    return imax - imin + 1

def dullCount(ifound, dull, ithresh):
    # same as in getFoundRange()
    if len(ifound)==0 :
        return 0
    imin = 3000
    imax = -1
    for j in range( len(ifound) ):
        i = ifound[j]
        if i>ithresh:
            continue
        if imax<i :
            imax = i
        if imin>i :
            imin = i
    count = 0   # this could be more efficient and more error prone
    for i in range(len(dull)):
        if dull[i] and imin<=i and i<= imax:
            count += 1
    return count

def countBool(array):
    count = 0
    for i in range(len(array)):
        if array[i]:
            count += 1
    return count

def showFound( tokens, ifound ):
    T = len(tokens)
    t = []
    total = []
    tmp = compressFound( T, ifound)
    for i in range(T):
        t = tokens[i]
        if tmp[i] :
            t += "* "
        else:
            t += " "
        #print( t ),
        total.append(t)
    s = ''.join(total)
 #   print( s )
    return s


def filterFile( filename, var ):
    infile = open(filename,"r")
    for line in infile:
        outstring = ""
        sentences = line.split('.' )
        if len(line)>0:
            print("\n\noriginal:"+ line)
        for sentence in sentences:
            tokens = sentence.split(' ')
            var.clear()
            F = var.findInText(tokens)
            if F:
                #print("FOUND" + showFound(tokens, var.ifound))
                outstring += " " + showFound(tokens, var.ifound)

        if len(outstring)>0:
            print("FOUND:"+outstring)

    infile.close()


def readFile( fineame, nar):
    infile = open(filename,"r")
    for line in infile:
        outstring = ""
        sentences = line.split('.' )
        if len(line)>0:
            print("\n\noriginal:"+ line)
        for sentence in sentences:
            tokens = sentence.split(' ')
            ifound = []
            E.clear()
            F = var.findInText(tokens)
            if F:
                #print("FOUND"+ showFound(tokens, var.ifound))
                outstring += " " + showFound(tokens, var.ifound)
        if len(outstring)>0:
            print("FOUND:" + outstring)

    infile.close()


def shiftFoundIndices(ifound, shift):
    for itok in range(len(ifound)):
       ifound[itok] = ifound[itok] + shift
    cleanFound(ifound)
    return ifound

def cleanAMPM(text):
    L = len(text)
    newtext = ""
    i = 0
    while i < L:
        c = text[i]
        if c=='I' and i<L-3 and text[i+1]==' ' and text[i+2]=='a' and text[i+3]=='m': # test for "I am"
            newtext += "I_am"
            i += 4
        elif c.isdigit() and i<L-2:
            d = text[i+1]
            e = text[i+2]

            if d.lower()=='a' and e.lower()=='m':
                newtext += c + ' ' + 'a' + 'm'
                i += 3
            elif  d.lower()=='p' and e.lower()=='m':
                newtext += c + ' ' + 'p' + 'm'
                i += 3
            else:
                newtext += c
                i +=1
        else:
            newtext += c
            i +=1

    return newtext



# I was not able to use a recursive definition inside the VAR.__le__()
def recursiveLE(self,other):
        if self.knames==other.knames:
            return True
        for child in other.children:
            if recursiveLE(self,child):
                return True
        return False
