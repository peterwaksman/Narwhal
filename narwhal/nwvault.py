from narwhal.nwtypes import *  # brings in nwutils and nwfind
from narwhal.nwutils import *
from narwhal.nwcontrol import *

# The "vault" (NarVault below) is a repository for instances of a
# narrative, encountered in the course of reading a text.
# It consists of an array of NarRecords.

# for convenience, the nar record includes the relevant snippet of
# original text


def getSnippet(istart, ictrl, tokens):
    if ictrl <= istart:
        return ""
    snippet = tokens[istart:ictrl]
    return snippet

# for convenience, the nar record includes the relevant snippet of original text
# plus some embelishments


def getSnippet2(istart, ictrl, ifound, tokens):
    if ictrl <= istart:
        return ""

    newtokens = tokens[:]
    for j in range(len(ifound)):
        i = ifound[j]
        newtokens[i] = newtokens[i] + "*"

    snippet = ""
    for i in range(istart, ictrl):
        snippet += newtokens[i] + " "

    return snippet


# The NarRecord reflects a collapsing of the data that has been kept
# as separate count of numSlotsUsed() and ifound (the indices of found tokens)
# during the reading process. These get scored and perhaps saved or "vaulted".
# There is a poetic analogy with how superposition of waves is
# additive until an event is observed. Events are not additive. In any case,
# the creation of a record and vaulting are an event. GOF means "goodness of fit"
# between narrative and text
# DEPRECATED IN FAVOR OF NarSRecord



class NarVault:
    def __init__(self):
        self._vault = []
        self.pre = 0
        self.nblocks = 0

# self.pre is or will be what is proposed for vaulting.
# It is "previous" to vaulting.
# You can block self.pre before or after you encounter the nar
# that proposes data into it. This gives rise to awkward phrases like
# "pre-preblocking" and "post-preblocking". The point is that
# Pre can be blocked while still empty, eg when you see "although".

    def clear(self):
        self._vault = []
        self.pre = 0
        self.nblocks = 0

    def vault(self, Threshold):
        if self.pre != 0 and self.pre.GOF > Threshold:
            # Apply blocks. Although polarity of a nar need
            # not behave like a boolean, the blocks arising from
            # controls perhaps DO behave like booleans
            if 1 == self.nblocks % 2:
                self.pre.block = True
                self.nblocks = 0
            self._vault.append(self.pre)
        self.pre = 0
        # resetting nblocks is someone else's job

    def abandonPre(self):
        self.pre = 0
        self.nblocks = 0

    def addBlock(self):
        self.nblocks = self.nblocks + 1

    def removeBlock(self):
        if self.nblocks > 0:
            self.nblocks = self.nblocks - 1

    def rollUp(self, record, Threshold, block=False):
        self.vault(Threshold)

        if block:
            self.addBlock()

        if record != None:
            self.vault(Threshold)  # saves old pre, as needed
            self.pre = record
            return True
        else:
            return False

        # Retrieve a record with specified ictrl.
        # Given way vault is created, at most one is possible
    def getRecordByCtrl(self, ictrl):
        for r in self._vault:
            if r.ictrl == ictrl:
                return r
        return None

    def getRecordByCtrl2(self, itok):
        for r in self._vault:
            if len(r.ifound) > 0 and max(r.ifound) == itok:
                return r
        return None
# This is a class manages nar and related "found" information after a read
# It is a nar plus ifound plus Vault
# It relieves some of the complexity of the NarReader.

