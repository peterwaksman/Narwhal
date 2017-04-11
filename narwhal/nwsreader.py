"""
nwreader.py contains the NWSReader object, the highest level reader. 

Members include:
     - app specific tree
     - app specific array of nars
     - array of vaults, one per nar, for storing NarSRecords
Implements two key algorithms, readText() and applyControl().
    readText() implements the "outer loop" for reading
        - convert text-to-tokens
        - convert tokens-to-VARs (the resulting sequence of VARs is called 
        a "segment".
        - for each subsegment between controls it calls "inner loop" 
        ReadSegment() 
        - at each control it pauses and tries to store things (in "vaults"), and 
        resets ("clears") more or less of the tree and the nars. This is
        the done in the following:

   applyControl() is where Narwhal's does its version of logical operations. 
        There is a delicate (and probably imperfect) balance between clearing 
        the information inside the VARs of the tree and clearing the 
        information inside the NARs during these control operations. Two key 
        activities are saving  read nar info in the vaults, and clearing 
        parts of the tree and parts of the nar array.

    Note use of "Many" indicates looping through the array of nars and 
    doing the same thing to each one. There is NO cross-talk between the
    nars for now.

"""
from narwhal.nwvault import *
from narwhal.nwsegment import *


##########################################################################
#  "NWS" = (N)ar(W)hal (S)egment reader
##########################################################################
class NWSReader:
    # assume the nars are defined using treeroot
    # The will retains their individual explicit/implicit settings
    def __init__(self, treeroot, nars):
        self.tree = treeroot.copy()
        self.tree.clear()
        self.tree.clearImplicits()

        self.nars = nars  # [:]

        self.calibs = []
        # later you can call set calibs with some 'True' entries
        self.setCalibration([])

        # for vaulting NarSRecords
        self.vaults = []
        for nar in self.nars:
            self.vaults.append(NarVault())

        # for recording what is found
        self.tokens = []

    def setCalibration(self, newcalibs):
        self.calibs = []
        for nar in self.nars:
            self.calibs.append(False)

        for i in range(min(len(self.nars), len(newcalibs))):
            self.calibs[i] = newcalibs[i]

    def clearAll(self):
        self.tree.clear()
        GENERAL_OP.clear()
        i = 0
        for nar in self.nars:
            nar.clear()
            self.vaults[i].clear()
            i = i+1
        self.tokens = []

    def readMany(self, segment):
        for nar in self.nars:
            ReadSegment(nar, segment)
            x = 2

    def unblockNars(self):
        for nar in self.nars:
            nar.polarity = not nar.polarity

    def recordMany(self, segment, imin, imax):
        records = []
        for nar in self.nars:
            s = nar.getIFound()
            g = segment[imin:imax + 1]
            lo = getLo(g)
            hi = getHi(g)
            if isInLoHi(nar, lo, hi):
                record = NarSRecord(nar, segment, lo, hi, self.tokens)
            else:
                record = None
            records.append(record)
        return records

    # each "rollUp" method works slightly differently. I did not see
    # a better way to generalize
    def rollUpMany(self, records, Threshold, block=False):
        for i in range(len(self.nars)):
            V = self.vaults[i]
            V.rollUp(records[i], Threshold, block)
            

    def rollUpCanVaultOrAbandonMany(self, records, Threshold, block=False):
        for i in range(len(self.nars)):
            V = self.vaults[i]
            rOK = V.rollUp(records[i], Threshold, block)
            if rOK:
                V.vault(Threshold)
            else:
                V.abandonPre()
                nar[i].clearPolarity()

    def rollUpAndVaultMany(self, records, Threshold, block=False):
        for i in range(len(self.nars)):
            V = self.vaults[i]
            V.rollUp(records[i], Threshold, block)
            V.vault(Threshold)

    def rollUpCanVaultMany(self, records, Threshold, block=False):
        for i in range(len(self.nars)):
            V = self.vaults[i]
            rOK = V.rollUp(records[i], Threshold, block)
            if rOK:
                V.vault(Threshold)

    def addBlockMany(self):
        for V in self.vaults:
            V.addBlock()

    def removeAllBlocksMany(self):
        for i in range(len(self.nars)):
            self.vaults[i].nblocks = 0
            self.nars[i].clearPolarity()  # comment out AD HOC?

    def clearIFoundMany(self):
        for nar in self.nars:
            nar.clearIFound()

    def clearMany(self):
        for nar in self.nars:
            nar.clear()

    def newStart(self, CD, istart):
        # a control occupies only one index in the segment
        return CD.ictrl + 1

    #####################################################
    ##################### outer read loop ###############
    def readText(self, text):
        self.clearAll()
        self.tokens = prepareTokens(text)

        segment = PrepareSegment(self.tree, self.tokens)

        if len(segment) == 0:
            return

        istart = 0  # i will be the index of a VAR in the whole segment
        CD = scanNextControl2(segment, istart)

        N = self.nars
        while CD.type != END_CTRLTYPE:
            subseg = segment[istart: CD.ictrl]

            self.readMany(subseg)

            istart = self.applyControl(CD, istart, segment)

            CD = scanNextControl2(segment, istart)

        subseg = segment[istart: len(segment)]
        self.readMany(subseg)
        self.applyControl(CD, istart, segment)

    ############################################
    def applyControl(self, CD, istart, segment):
        if CD.type == NO_CTRLTYPE:
            return istart

            # prepare records for all nars (some can be  "None")
        records = self.recordMany(segment, istart, CD.ictrl)
        if records == None or len(records) == 0:
            return istart

        if CD.type == END_CTRLTYPE:
            self.rollUpAndVaultMany(records, 0.1)
            return len(segment)

        CTRL = CD.ctrl

        # this is current "and" processing. It is closely tied to
        # to how "AND" is declared, as a SKIP, or LOGIC OPerator.
        # Take this code out if you want it to SKIP
        # Also consider changing the 0.5 to tune sub-vaulting
        if CTRL.isA("AND"):
            self.rollUpMany(records, 0.5)
            # self.clearIFoundMany()

        elif CTRL.isA("NEG") or CTRL.isA("HEDGE"):
            BLOCK = True  # block backward
            self.rollUpCanVaultOrAbandonMany(records, 0.5, BLOCK)
            self.unblockNars()
            # self.clearIFoundMany()

        elif CTRL.isA("FNEG") or CTRL.isA("FHEDGE"):
            self.rollUpAndVaultMany(records, 0.5)
            # self.clearIFoundMany()
            self.addBlockMany()  # block forward

        elif CTRL.isA("COMMA") or CTRL.isA("SEMICOLON"):
            self.rollUpCanVaultMany(records, 0.5)
            self.removeAllBlocksMany()
            self.clearMany()
            # self.clearIFoundMany()

        # note: no "OPENPAREN" processing yet
        elif CTRL.isA("CLOSEPAREN"):
            self.rollUpCanVaultMany(records, 0.5)
            self.removeAllBlocksMany()

        elif CTRL.isA("OPENPAREN"):
            self.rollUpCanVaultMany(records, 0.5)
            self.removeAllBlocksMany()

        elif CTRL.isA("PERIOD") or CTRL.isA("EXCLAIM") or CTRL.isA("DASH"):
            self.rollUpCanVaultMany(records, 0.1)
            self.removeAllBlocksMany()

            self.clearMany()  # a clean start

        else:
            print("did not apply contol: " + CTRL.knames[0])
            self.clearIFoundMany()
            self.clearIFoundMany()
            return istart + max(1, len(CD.ctrl.ifound))

        # self.clearIFoundMany()

        istart = self.newStart(CD, istart)

        return istart

    def report(self, text):
        tokens = prepareTokens(text)
        out = ""
        L = len(tokens)
        for i in range(len(tokens) + 1):
            if i < len(tokens):
                out += tokens[i].rjust(10) + " "
            else:
                out += "END".rjust(10) + " "

            for j in range(len(self.nars)):
                V = self.vaults[j]     # j not i!
                cal = self.calibs[j]

                r = None
                if i > 0:
                    r = V.getRecordByCtrl2(i - 1)  # i not j!
                if r == None:
                    out += " "
                else:
                    P = r.finalPolarity(cal)
                    if P:
                        val = "+"
                    else:
                        val = "-"
                    out += val
                if r == None:
                    out += ".      "
                else:
                    out += ("{0:.4g}".format(r.GOF)).ljust(6) + " "
            out += "\n"
        out += "\n"
        return out
