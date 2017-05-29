"""
nwnreader.py does reading with a single nar. Tree and segmentation
are handled externally
"""
from narwhal.nwvault import *
from narwhal.nwsegment import *

class NWNReader:
    def __init__(self, nar, flipPolarity = False):
        self.nar = nar
        self.vault = NarVault()
        self.cal = flipPolarity
 
    def clearAll(self):
        self.nar.clear() 
        self.vault.clear()
      
    def read(self, segment):
        ReadSegment(self.nar, segment)

    def unblockNar(self):
        self.nar.polarity = not self.nar.polarity
         
    def makeRecord(self, segment, imin, imax, tokens):
        nar = self.nar
        s = nar.getIFound()
        g = segment[imin:imax + 1]
        lo = getLo(g)
        hi = getHi(g)
        if isInLoHi(nar, lo, hi):
            return NarSRecord(nar, segment, lo, hi, tokens)
        else:
            return None     

    def rollUp(self, record, Threshold, block=False):
        """
        To "rollUp" means to put a record into the vault's "pre" 
        and move anything already in pre to the final storage.
        """
        V = self.vault
        V.rollUp(record, Threshold, block)      

    def rollUpAndVault(self, record, Threshold, block=False):
        """
        This is a rollUp that also flushes the "pre"
        """
        V = self.vault 
        V.rollUp(record, Threshold, block)
        V.vault(Threshold) 

    def rollUpCanVaultOrAbandon(self, record, Threshold, block=False):
        V = self.vault 
        rOK = V.rollUp(record, Threshold, block)
        if rOK:
            V.vault(Threshold)
        else:
            V.abandonPre()
            self.nar.clearPolarity()

  
    def rollUpCanVault(self, record, Threshold, block=False):
        V = self.vault 
        rOK = V.rollUp(record, Threshold, block)
        if rOK:
            V.vault(Threshold)

    def addBlock(self):
        V = self.vault
        V.addBlock()

    def removeAllBlocks(self):
        self.vault.nblocks = 0
        self.nar.clearPolarity() # AD HOC? 

    def clearIFound(self):
        self.nar.clearIFound()

    def clear(self):
        self.nar.clear()

    def newStart(self, CD, istart):
        # a control occupies only one index in the segment (wrong!)
        return CD.ictrl + 1

    def lastConst(self):
        return self.nar.lastConst
    def Thing(self):
        return self.nar.Thing()
    def Action(self):
        return self.nar.Action()
    def Relation(self):
        return self.nar.Relation()
    def Value(self):
        return self.nar.Value()

  #####################################################
    ##################### outer read loop ###############
    def readText(self, segment, tokens):
        self.clearAll()  
        if len(segment) == 0:
            return

        istart = 0  # i will be the index of a VAR in the whole segment
        CD = scanNextControl2(segment, istart)

        N = self.nar
        while CD.type != END_CTRLTYPE:
            subseg = segment[istart: CD.ictrl]

            self.read(subseg)

            istart = self.applyControl(CD, istart, segment,tokens)

            CD = scanNextControl2(segment, istart)

        subseg = segment[istart: len(segment)]
        self.read(subseg)
        self.applyControl(CD, istart, segment,tokens)


    ############################################
    ############################################
    ############################################

    def applyControl(self, CD, istart, segment,tokens):
        if CD.type == NO_CTRLTYPE:
            return istart

            
        record = self.makeRecord(segment, istart, CD.ictrl,tokens)
        #if record == None :
        #    # For now, really just istart = istart+1
        #    istart = istart + 1 
        #    return istart

        if CD.type == END_CTRLTYPE:
            self.rollUpAndVault(record, 0.1)
            return len(segment)

        control = CD.ctrl

        # this is current "AND" processing. It is closely tied to
        # to how "AND" is declared, as a SKIP, or LOGIC OPerator.
        # Take this code out if you want it to SKIP
        # Also consider changing the 0.5 to tune sub-vaulting
        if control.isA("AND"):
            self.rollUp(record, 0.5)
            # self.clearIFound()

        elif control.isA("NEG") or control.isA("HEDGE"):
            BLOCK = True  # block backward
            self.rollUpCanVaultOrAbandon(record, 0.5, BLOCK)
            self.unblockNar()
            # self.clearIFound()

        elif control.isA("FNEG") or control.isA("FHEDGE"):
            self.rollUpAndVault(record, 0.5)
            # self.clearIFound()
            self.addBlock()  # block forward

        elif control.isA("COMMA") or control.isA("SEMICOLON"):
            self.rollUpCanVault(record, 0.5)
            self.removeAllBlocks()
            self.clear()
            # self.clearIFound()

        # note: no "OPENPAREN" processing yet
        elif control.isA("CLOSEPAREN"):
            self.rollUpCanVault(record, 0.5)
            self.removeAllBlocks()

        elif control.isA("OPENPAREN"):
            self.rollUpCanVault(record, 0.5)
            self.removeAllBlocks()

        elif control.isA("PERIOD") or control.isA("EXCLAIM") or control.isA("DASH") or control.isA("QUERY"):
            self.rollUpCanVault(record, 0.1)
            self.removeAllBlocks()

            self.clear()   

        else:
            print("did not apply contol: " + CTRL.knames[0])
            self.clearIFound()
            return istart + max(1, len(CD.ctrl.ifound))

        # self.clearIFound()

        istart = self.newStart(CD, istart)

        return istart

    def report(self, tokens):
        out = ""
        L = len(tokens)
        for i in range(len(tokens) + 1):
            if i < len(tokens):
                out += tokens[i].rjust(10) + " "
            else:
                out += "END".rjust(10) + " "
                          
            V = self.vault      
            r = None
            if i > 0:
                r = V.getRecordByCtrl2(i - 1)  # i not j!
            if r == None:
                out += " .      "
            else:
                P = r.finalPolarity(self.cal)
                if P:
                    sign = "+"
                else:
                    sign = "-"
                out += sign
                out += ("{0:.4g}".format(r.GOF)).ljust(6) + " "

            out += "\n"
        out += "\n"
        return out

    def tabulate(self,numTokens):
        x = self.vault.tabulate(numTokens, self.cal)
        return x

   