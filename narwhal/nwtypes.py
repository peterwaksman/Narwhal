"""
nwtypes.py defines the basic data types involved in "narrative" entities
KList, VAR, and NAR. 
The KList is a list of keywords with text matching capabilities
The VAR is like a "concept" that wraps the KList. VARs are tree nodes
The NAR is a four part narrative with actor, action, relation, and target
"""

from narwhal import nwfind
from narwhal import nwutils


class KList:
    """ 
    KList - a wrapper around a list of keywords, with some regular expression-like 
    matching behavior defined by KList.findInText(). Note the way KList instances
    are tracked inside the KList class. This allows retrieving a KList by name.

    K(ey word)Lists are initialized with comma-separated strings thanks to Stack 
    Exchange for idea of making it into a factory and repository
    They have no "state".
    """
    instances = {}

    def __init__(self, name, inString):
        self.name = name
        self.list = inString.split(',')
        KList.instances[name] = self  # syntax: klist = KList.instances[ name ]


    def var(self):  # turn a KList into a VAR. Known as a "KList VAR"
        Z = VAR()
        Z.knames.append(self.name)
        return Z


        # the KList does not keep track of its last search result
        # it is the responsibility to the client to pass in ifound
        # This method returns True or False
        # It returns the token that was matched or with ''
    def findInText(self, tokens, itok, ifound):
        return nwfind.findInText(self, tokens, itok, ifound)


NULL_KLIST = KList("nullK", "")

# design pattern is a bit strange: relatively concrete containers are used
# to generate more abstract ones that wrap them.

# VARS are lists of keyword lists (actually just the names of keyword lists)
# with an attribute of "exclusive" if an input word can match just one
# of the KLists. If not "exclusive", an input word can match any KList


class VAR:
    """
    VAR - a tree node wrapping a single KList with constant attributes:
    exclusive - means the VAR represents a binary choice [ternary is possible]
    By definition, the first alternative means good and second means bad. 
    (You can change this with calibrations later.)

    explicit   - refers to when the VAR can be missing from a narrative
    parent, and children. (The VAR tree is fundamental to the app)

    Various volatile sctachpads and summaries used during reading:
    found - whether this VAR was found in the input text
    polarity - whether this is a good thing or a bad thing (per "exclusive" above)
    ifound[] - a list of token indices where VAR matched
    (Note that with the regular expression-like behavior of the KList,
    the act of "matching" is done as a sliding window over the tokens,
    centered on an itok index, searching forward AND backward from itok.)

    foundInChildren - means a child of the VAR node found a match
    """
    def __init__(self):

        # ---these are constant in the VAR
        self.knames = []  # a VAR can always have its own KList

        # true means VAR represents a binary choice (I did not implement
        # ternary...)
        self.exclusive = False

        self.parent = 0  # makes a VAR into a tree node, but tree info is lost by operators
        self.children = []
        self.explicit = True  # When False, this allows nars to be multi purpose. Slots that
        # are neither filled nor explicit are "inactive" and do not enter
        # into the GOF formula. Non-explicit VARs are called 'implicit'
        # If an implicit is not 'found' then, functionally, the nar just
        # becomes shorter

        # FOR READING:
        self.found = False
        # to store indices of tokens in text, with matches words of self's
        # KLists.
        self.ifound = []
        # to record what happened in the children
        self.foundInChildren = False
        # becomes false if kname after 1st is used
        self.polarity = True

        #become set to last read var<=this
        self.lastConst = "" 

      
    def __le__(self, other):
        """ typically a "var<=nar" means the var is a child or itself"""
        return nwutils.recursiveLE(self, other)


    # All children become implicit when their parent does
    def makeImplicit(self):
        if self == NULL_VAR:
            return
        self.explicit = False
        for child in self.children:
            child.makeImplicit()


    def makeExplicit(self):
        if self == NULL_VAR:
            return
        self.explicit = True
        for child in self.children:
            child.makeExplicit()


    def clearImplicits(self):
        self.explicit = True
        for child in self.children:
            child.clearImplicits()


    def clear(self):
        self.found = False
        self.ifound = []
        self.foundInChildren = False
        self.polarity = True

        self.lastConst = ""

        for child in self.children:
            child.clear()

            # this allows re-use of the VAR in search functions
            # but leaves the self.found unchanged
    def clearIFound(self):
        self.ifound = []
        for child in self.children:
            child.clearIFound()


    def numIFound(self):
        self.ifound = nwutils.cleanFound(self.ifound)
        return len(self.ifound)


    def getIFound(self):
        return self.ifound


    def clearPolarity(self):
        self.polarity = True


    def lastIFound(self):
        max = -1
        for i in self.ifound: 
            if max<i :
                max = i
        return max


    # call this once, usually on the root node of the tree
    def copy(self):
        if self==NULL_VAR:
            return NULL_VAR
        v = VAR()
        v.knames = self.knames
        v.exclusive = self.exclusive
        if self.parent == 0:
            v.parent = 0

        v.found = self.found
        v.ifound = self.ifound[:]
        v.foundInChildren = self.foundInChildren
        v.polarity = self.polarity

        v.lastConst = self.lastConst 

        for child in self.children:
            newchild = child.copy()
            v.children.append(newchild)

        v.explicit = self.explicit

        return v


    def copyUsing(self, tree):
        if self==NULL_VAR:
            return self
        name = self.knames[0]
        #print(name+ "\n")
        if not isinstance(tree, VAR):
            print("OOPS in copyUsing()")
            print(name)
            return
        else:
            x = tree.lookup(name)  # find VAR with same name, in this tree
        if x != NULL_VAR:
            x.explicit = self.explicit
            return x  # x.copy().
        else:
            return NULL_VAR


    # returns self, if kname in knames
    # or child with this name, else NULL_VAR
    def lookup(self, name):
        for kname in self.knames:
            if name == kname:
                return self

        for child in self.children:
            x = child.lookup(name)
            if x != NULL_VAR:
                return x
        return NULL_VAR

    def isUnknown(self):
        if self.knames[0]=='int' or self.knames[0]=='float':
            return True
        else:
            return False

        # Finds VAR matching at itok. Only visit
        # children if no direct match is found
    def findInText2(self, tokens, itok):
        self.lastConst = ""

        ikname = 0
        alreadyFound = False
        j=0
        f =''# the returned token that was matched
        for kname in self.knames:  # for each name in self's klist
            j+=1
            klist = KList.instances[kname]
                                    # get last matched token
            f = klist.findInText(tokens, itok, self.ifound)
            if len(f)>0:
                self.found = True  
                # this can switch frequently and reflects the last found token
                if self.exclusive and ikname > 0:
                    self.polarity = False
                else:
                    self.polarity = True

                alreadyFound = True

                if self.isUnknown():
                    self.lastConst = f
                else:
                    self.lastConst = self.knames[0]

            ikname += 1

        # If nothing was found, search iteratively inside the children
        if alreadyFound:
            if self.isUnknown() :#just for unknowns
                self.lastConst = f
            else:
                self.lastConst = self.knames[0] # f
            return [self]

        vars = []
        for child in self.children:
            foundC = child.findInText2(tokens, itok)
            if len(foundC) > 0:
                self.foundInChildren = True
                self.ifound.extend(child.ifound)
                self.ifound = nwutils.cleanFound(self.ifound)
                if child.knames[0]=='int' or child.knames[0]=='float':
                    self.lastConst = foundC
                else:
                    #self.lastConst = child.knames[0]
                    self.lastConst = child.lastConst

                if not alreadyFound: # (non functional)
                    self.polarity = child.polarity
                vars.extend(foundC)
        return vars  # empty list if none found in children


    def str(self, ntabs):
        tab = ""
        for i in range(ntabs):
            tab += "  "

        x = ""
        if self.found:
            x += "*"
        if self.explicit:
            x += self.knames[0]
        else:
            x += "[" + self.knames[0] + "]"
        return tab + x


    # use Print() for recursive print, or Print(0,False) for non-recursive
    def Print(self, ntabs=0, recurs=True):
        tab = ""
        for i in range(ntabs):
            tab += "  "

        endStr = tab + "knames:"
        # print(tab+"knames:"),
        for name in self.knames:
            if not self.exclusive:
                endStr += (name + " +")
                #print(name+" +"),
            else:
                endStr += (name + " |")
                #print(name+" |"),
        if self.found:
            tmp = "*"
        else:
            tmp = ""

        endStr += endStr + "\n" + tab + "found :" + tmp
        print(endStr)
        #print("\n" + tab+"found :"+ tmp )

        if self.foundInChildren:
            tmp = "*"
        else:
            tmp = ""
        print(tab + "foundC:" + tmp)
        print(tab + "plrty :" + str(self.polarity))
        if len(self.children) > 0:
            print(tab + "chldrn:")
        else:
            print("\n")

        if recurs:
            for child in self.children:
                child.Print(ntabs + 1, recurs)


    def PrintSimple(self, ntabs=0):
        output = ""
        tab = ""
        for i in range(ntabs):
            tab += "  "

        output += tab
        # print(tab),
        for name in self.knames:
            if not self.explicit:
                name = "[" + name + "]"
            if not self.exclusive:
                output += name + " "
            else:
                output += name + "|"
        if self.found:
            output += "*"
        if not self.polarity:
            output += "-"
        output += '\n'
        for child in self.children:
            output += child.PrintSimple(ntabs + 1)
        return output

  
    # operator '+'     # to match text against any Klist
    def __add__(self, other):
        Z = VAR()
        Z.knames += self.knames
        Z.knames += other.knames
        Z.exclusive = False
        return Z


    # operator '|'    # to match text against just one KList
    # matching text in more than one is considered a coding error but
    # it could be a contradiction in the text. We'll see.
    def __or__(self, other):
        Z = VAR()
        Z.knames += self.knames
        Z.knames += other.knames
        Z.exclusive = True
        return Z


    # connect with your children as in "addChild()"
    def sub(self, other):
        other.parent = self
        self.children.append(other)


    def numSlots(self):
        if self == NULL_VAR:
            return 0
        else:
            return 1


    def numSlotsUsed(self):
        if self == NULL_VAR:
            return 0
        if self.found or self.foundInChildren:
            return 1
        else:
            return 0


    # "Active" means explicit or currently used.
    def numSlotsActive(self):
        if self == NULL_VAR:
            return 0
        if self.found or self.foundInChildren or self.explicit:
            return 1
        else:
            return 0


    # like a minimal "print". It is used by nar.string()
    def string(self, ntabs=0):
        return self.knames[0]


    # KList VARS are used to produce "KList" NARs of order 0
    # So VAR become a class factory for NAR.
    # All NARs built from these KList NARs will be of higher order>0
    def nar(self):
        p = NAR()
        p.order = 0 
        p.polarity = True
        p.explicit = True

        p.thing = self         # so isinstance(p.thing,VAR) is True
        p.action = NULL_VAR
        p.relation = NULL_VAR
        p.value = NULL_VAR

        p.lastConst = "" # not self.knames[0] to avoid fake read event
        return p

    # note this does not climb up the tree of parents returning true if foundInChildren
    # This only returns true for the self VAR's knames[0] argument
    # nor does it climb down the tree searching for childern. (Gosh someone
    # should do that)
    def isA(self, name):
        return name == self.knames[0]

    #def __eq__(a,b):
    #    return a.knames[0]== b.knames[0]


    def isCommonParent(self,a,b):
        return a<=self and b<=self

    def LCP(self, v, w ):
        """The least common parent of a and b, beneath self"""
        if not self.isCommonParent(a,b):
            return None
        L = []
        for child in self.children:
            p = child.LCP(a,b)
            if p:
                L.append(p)

        if len(L) == 0 : # none found in children (but isCommonParent()==True
            return self
        elif len(L)>1 :  # found in several different children
            return self
        else:            # found in child or beneath it 
            return L[0]


# -----------ZERO for VAR type
NULL_VAR = NULL_KLIST.var()
# NOTE: when copying, but NULL_VAR and NULL_NAR are returned without being copied;


#######################################################################
#                            NAR                                      #
#######################################################################

class NAR:
    """
    NAR - the nestable entities that wrap VARs or other NARs. They are 
    considered to be narrative patterns. Note that nesting of NARs as 
    subnarratives, is a different hierarchical structure than the tree of 
    VARs.

    A NAR has these constant attributes:  

    order
    VARs are order 0 and all narratives built over them have
    order one greater [For the moment NARs built from VARs are also order 0]
    than the order of any subnarrative. 

    explicit
    When false, means it can be missing from the text and not count
    against matching. (Usually for a subnarrative. An empty narrative that is not
    explicit can never score more than 0.5)

    The four subnarratives that define a NAR are thing, action, relation, and value
    See code for their respective roles.
     
    Since NARs wrap VARs, all the bookeeping during a "read" done inside those VARs 
    is inherent within the wrapping NAR. The NAR itself has only one volatile entity:
    polarity - whether the filled story is good or bad - a formula derived from the 
    good/bad polarity of the underlying subnarratives (and VARs). Note that polarity
    is 'True' by default. And you may not care about that field.
    """
    def __init__(self):
        self.order = 0  # the level of pattern-inside-pattern depth. Currently it is informational
        # don't know if I want this [ANSWER: to implement implicit variables]
        self.explicit = True

        self.polarity = True

        self.thing = NULL_VAR
        self.action = NULL_VAR
        self.relation = NULL_VAR  # like "color" (or "with")
        self.value = NULL_VAR    # like "red" (or an other.thing)
        # The concept of "value" is overloaded here, and is being forced on me
        # by a lack of programming ability. "value" works as an adjective,
        # or as an object, or as whatever

        self.lastConst = "" # should hold records of most slot events

    # don't know if I want this
    def makeImplicit(self):
        self.explicit = False
        self.thing.makeImplicit()
        self.action.makeImplicit()
        self.relation.makeImplicit()
        self.value.makeImplicit()


    def makeExplicit(self):
        self.explicit = True
        self.thing.makeExplicit()
        self.action.makeExplicit()
        self.relation.makeExplicit()
        self.value.makeExplicit()


    # If x is a var, this calls .clear(), otherwise it calls into the sub
    # narratives.
    def clear(self):
        self.polarity = True
        self.thing.clear()
        self.action.clear()
        self.relation.clear()
        self.value.clear()
        self.lastConst = ""


    def clearPolarity(self):
        self.polarity = True
        self.thing.clearPolarity()
        self.action.clearPolarity()
        self.relation.clearPolarity()
        self.value.clearPolarity()


    def clearIFound(self):
        if ORDER(self) == 0:
            self.clearIFound()
            return
        self.thing.clearIFound()
        self.action.clearIFound()
        self.relation.clearIFound()
        self.value.clearIFound()


    def lastIFound(self):
        max = -1
        if max<self.thing.lastIFound():
            max = self.thing.lastIFound()
        if max<self.action.lastIFound():
            max = self.action.lastIFound()
        if max<self.relation.lastIFound():
            max = self.relation.lastIFound()
        if max<self.value.lastIFound():
            max = self.value.lastIFound()
        return max  


    # this copy uses the same VARs in the same tree as the original
    def copy(self):
        if self==NULL_NAR:
            return NULL_NAR
        n = NAR()
        n.order = self.order
        n.polarity = self.polarity
        n.explicit = self.explicit

        n.thing = self.thing.copy()
        n.action = self.action.copy()
        n.relation = self.relation.copy()
        n.value = self.value.copy()

        n.lastConst = self.lastConst

        return n

  
    def generateLastConst(self):
        lastC = ""

        t = self.thing.lastConst
        if nwutils.hasSeparator(t):
            lastC += '(' + t + ')' + ':'
        else:
            lastC += t + ':'

        a = self.action.lastConst
        if nwutils.hasSeparator(a):
            lastC += '(' + a + ')' + ':'
        else:
            lastC += a + ':'
        
        r = self.relation.lastConst
        if nwutils.hasSeparator(r):
            lastC += '(' + r + ')' + ':'
        else:
            lastC += r + ':'
  
        v = self.value.lastConst
        if nwutils.hasSeparator(v):
            lastC += '(' + v + ')'  
        else:
            lastC += v  
  
        #lastC = self.thing.lastConst + ":"
        #lastC += self.action.lastConst + ":"
        #lastC += self.relation.lastConst + ":"
        #lastC += self.value.lastConst
        #temp = lastC.split(':')
        self.lastConst = lastC

    def Thing(self):
        return nwutils.Thing(self.lastConst)
        #temp = self.lastConst.split(':')
        #if len(temp)<4 :
        #    return ''
        #return temp[0]
    def Action(self):
        return nwutils.Action(self.lastConst)
        #temp = self.lastConst.split(':')
        #if len(temp)<4 :
        #    return ''
        #return temp[1]
    def Relation(self):
        return nwutils.Relation(self.lastConst)
        #temp = self.lastConst.split(':')
        #if len(temp)<4 :
        #    return ''
        #return temp[2]
    def Value(self):
        return nwutils.Value(self.lastConst)
        #temp = self.lastConst.split(':')
        #if len(temp)<4 :
        #    return ''
        #return temp[3]


    # When this tree is a copy of the one where the NAR is defined,
    # NAR.copyUsing returns a "copy" of the same name as self, but
    # using VARs from a other tree
    def copyUsing(self, tree):
        if self == VAR_SO or self == VAR_THEN:  # these do not get copied
            return self

        if isinstance(self, VAR):  # so it is a var
            name = self.thing.knames[0]
            x = tree.lookup(name)  # find VAR with same name, in this tree
            if x != NULL_VAR:
                n = x.nar()
                return n
        # happens if parent had empty children (like so and so)
        elif self.order == 0:
            return NULL_NAR

        n = NAR()
        n.order = self.order
        n.polarity = self.polarity
        n.explicit = self.explicit

        # for the sub NARs
        n.thing = self.thing.copyUsing(tree)

        # This is not really right but I do not want to make
        # copies of these "constant" NARs. It means
        # we should never rely on the found or ifound of the VARs beneath
        # these "constants", since different users may also be using them
        if self.action == VAR_SO:
            n.action = VAR_SO
        elif self.action == VAR_THEN:
            n.action = VAR_THEN
        else:
            n.action = self.action.copyUsing(tree)

        n.relation = self.relation.copyUsing(tree)
        n.value = self.value.copyUsing(tree)
        return n


    def numSlots(self):
        if isinstance(self, VAR):
            return self.numSlots()
        n = 0
        n += self.thing.numSlots()
        n += self.action.numSlots()
        n += self.relation.numSlots()
        n += self.value.numSlots()
        return n


    def numSlotsUsed(self):
        if isinstance(self, VAR) and self.found:
            return self.numSlotsUsed()
        else:
            n = 0
            n += self.thing.numSlotsUsed()
            n += self.action.numSlotsUsed()
            n += self.relation.numSlotsUsed()
            n += self.value.numSlotsUsed()
            return n


    def numSlotsActive(self):
        if isinstance(self, VAR):
            return self.numSlotsActive()
        else:
            n = 0
            n += self.thing.numSlotsActive()
            n += self.action.numSlotsActive()
            n += self.relation.numSlotsActive()
            n += self.value.numSlotsActive()
            return n


    def getIFound(self):
        if self == NULL_VAR:
            return []

        # ifound in one slot
        if isinstance(self, VAR):
            return self.ifound[:]

        # ifound in several in the different slots
        all = []
        all.extend(self.thing.getIFound())
        all.extend(self.action.getIFound())
        all.extend(self.value.getIFound())
        all.extend(self.relation.getIFound())
        # consolidate them and count
        all = nwutils.cleanFound(all)
        return all


    def numIFound(self):
        return len(self.getIFound())


    def getType(nar):
        thing = nar.thing
        action = nar.action
        relation = nar.relation
        # nar.value not part of type

        if relation != NULL_VAR:
            return ATTRIB_NARTYPE
        elif action == VAR_SO:
            return SO_NARTYPE
        elif action == VAR_THEN:
            return THEN_NARTYPE
        elif action != NULL_VAR:
            return EVENT_NARTYPE
        elif thing != NULL_VAR:
            return THING_NARTYPE
        else:
            return NULL_NARTYPE


    def printType(self):
        print(strNarType(self.getType()))


    def str(nar, ntabs=0):
        tab = ""
        for i in range(ntabs):
            tab += "  "

        if nar == NULL_NAR:
            return "nullN"

        x = ""
        if isinstance(nar, VAR):
            if nar.found:
                x += "*"
            if nar.explicit:
                x += nar.knames[0]
            else:
                x += "[" + nar.knames[0] + "]"
        elif isinstance(nar, NAR):
            x += "\n"
            t = nar.thing.str(ntabs + 1)
            r = nar.relation.str(ntabs + 1)
            a = nar.action.str(ntabs + 1)
            v = nar.value.str(ntabs + 1)

            x += tab + "T:" + t + "\n"
            x += tab + "R:" + r + "\n"
            x += tab + "A:" + a + "\n"
            x += tab + "V:" + v + "\n"
        return x


    def Print(nar, ntabs=0):
        s = nar.str(ntabs)
        print(s)
#####################################################


 
NULL_NAR = NULL_VAR.nar()  # used as a default arg
# NOTE: when copying, but NULL_VAR and NULL_NAR are returned without being copied;

def isNullNar( R ):
    if not isinstance(R,NAR):
        return False
    T = R.thing
    if isinstance(T,VAR) and T.isA('nullK'):
        return True
    else:
        return False


# NOTE: NULL_VAR is used to indicate an uninitialized NAR
# and NULL_NAR is used to indicate a NAR that is empty. NULL_NAR
# is used as a deliberate place holder

# ----------- UTILITIES FOR VARS AND NARS


def ORDER(X):
    if isinstance(X, VAR):
        return 0
    else:
        return X.order


# ----------- OPERATORS that should have been methods of NAR() but I could not
# figure out how to program them. Their default args need to be globals that are
# not acceptable to the VAR() class.
#
# These are narratives of higher order than their members. Eg order 1 for NARs that wrap VARs
#
# The proccessing priority is: attribute, event, cause, sequence -
# implemented in the read methods

# NOTE: all these operators allow args to be a NAR or a list containing one
# NAR. The list brackets "[]" indicates the contained NAR should be
# set to 'implicit'. The next  methods change values in the underlying tree
# So a client cannot use the same VAR as implicit in one place and explicit
# in another. A VAR copy is needed for that.

# This co-ops the list syntax of Python, to indicate implicit arguments
# It returns (possibly modified) input
def a2n(arg):
    if isinstance(arg, list):
        n = arg[0]
        n.explicit = False
    else:
        n = arg
    return n


# -------implements:  "X_REL_/A" - the adjective relation. X,A, and REL are NARs
#  ATTN! only use the REL variable if it is defined with A
# TODO: put in a check for this

def attribute(x, y, rel=NULL_NAR):
#def attribute(x, y, rel=NULL_VAR):
    X = a2n(x)  # interpret args
    Y = a2n(y)
    REL = a2n(rel)

    n = NAR()
    n.thing = X  # "noise"
    n.relation = REL  # "outside"
    n.action = NULL_VAR
    n.value = Y  # "loud"

    n.order = max(ORDER(X), ORDER(REL), ORDER(Y)) + 1
    return n

# -------implements:  "X-ACT->Y" - the verb relation


def event(x, y, act):
    X = a2n(x)  # interpret args
    Y = a2n(y)
    ACT = a2n(act)

    n = NAR()
    n.thing = X  # "I"
    n.relation = NULL_VAR
    n.action = ACT  # "see"
    n.value = Y  # "bird"

    n.order = max(ORDER(X), ORDER(ACT), ORDER(Y)) + 1
    return n


# The next two OPERATORS have the same syntax but different text matching rules.
# They both describe sequential events X and Y but the cause(X,Y) function describes them
# as causally connected, and the seq(X,Y) function describes them purely as a sequential.
# Note "SO" is used internally for cause and "THEN" and "AND" for sequence.

# -------Implements:  causal "X::Y" . This operator indicates transformation, becoming, causality,
# and is a bit like logical "therefor". Words in text like "so", "because", or "but"
# are listed in internal KLists and are not needed from the client
# Worth mentioning (as part of another rant below) that these words in English are
# translated by logicians into "therefor" - which is supposed to be timeless
#  - exactly opposite to the usage here.

# a dummy to identify the "cause" type of statement
VAR_SO = KList("so", "").var()
VAR_SO.makeImplicit()
# the correct word searching is handled by internal lists

# Worth mentioning: the internal list searching marks token indices in ifound[]
# so those indices are not counted in the r/f part of the gof() formula.
# Ensuring that VAR_SO and also VAR_THEN (below) are implicit, means ensuring they 
# are NOT counted as slots in the u/n part of the formula.



def cause(x, y):
    X = a2n(x)  # interpret args
    Y = a2n(y)

    n = NAR()
    n.thing = X  # "we were happy"

    n.action = VAR_SO   # (encode a "so" operation)
    n.value = Y  # "we laughed"
    n.order = max(ORDER(X), ORDER(Y)) + 1
    return n


# ----Implements: sequence "X,Y" . Words like "and" or "or" or "then A then B then C" are handled internally
# Screw the symbolic logicians who co-opted "then" for use only in "if..then..". Its natural use
# is closer to some versions of "and". Meanwhile they co-opted "or" and created the straw horse
# of "and not both". Further, don't tell me that chronology "X,Y" can be co-opted as a bi-
# directional relation like logical "or" and "and", or as a sub-part of an "if then" (which has
# lost its connection to chronology) So here, for a change, it means chronology. To achieve bi-
# directionalty,for now, requires using both X,Y and Y,X and you can
# design code making them equivalent
# used to identify the "and"/"then" type of statement
VAR_THEN = KList("then", "").var() 
VAR_THEN.makeImplicit() #revisit


def sequence(x, y):
    X = a2n(x)  # interpret args
    Y = a2n(y)

    n = NAR()
    n.thing = X  # "we ate cookies"
    n.action = VAR_THEN  # (encode a "then" operation)
    n.value = Y  # "we ate pie"
    n.order = max(ORDER(X), ORDER(Y)) + 1
    return n

##########################################
# the num slots used doesn't work correctly here.
#def combo(x,y,z,w):
#    X = a2n(x)
#    Y = a2n(y)
#    Z = a2n(z)
#    W = a2n(w)
#    n = NAR()
#    n.thing = X  # "we ate cookies"
#    n.action = Y
#    n.relation = Z
#    n.value = W
#    n.order = max(ORDER(X), ORDER(Y)) + 1
#    return n


####################### REFERENCE CONSTANTS for NAR class ################
NULL_NARTYPE = 0  # for empty nar, like NULL_NAR
THING_NARTYPE = 1  # for nar without actioN or relation
ATTRIB_NARTYPE = 2  # non empty relation
EVENT_NARTYPE = 3  # user defined event
SO_NARTYPE = 4  # cause/"so" nar ("so" is more for internal use)
THEN_NARTYPE = 5  # sequence/"then" nar ("then is more for internal use)


def strNarType(nar_type):
    if nar_type == NULL_NARTYPE:
        return "NULL"
    elif nar_type == THING_NARTYPE:
        return "THING"
    elif nar_type == ATTRIB_NARTYPE:
        return "ATTRIB"
    elif nar_type == EVENT_NARTYPE:
        return "EVENT"
    elif nar_type == SO_NARTYPE:
        return "CAUSE"
    elif nar_type == THEN_NARTYPE:
        return "SEQ"
