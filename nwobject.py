from nwutils import *
from nwtypes import *
from nwcontrol import *
from nwvault import *
from nwread import *

# NarInfo: a structured version of  the NarRecord 
# The NarInfo is a "most final" version of things
# So we have a partially filled nar converted to a NarRecord 
# Which is stored in a vault inside a NarReadData (could be
# better organized).  
class NarInfo:
    def __init__(self, threshold):
        self.threshold = threshold
        self.found = False
        self.GOF = 0.0
        self.snippet = ""
        self.polarity   = True
 
    def clear(self):
        self.found = False
        self.GOF = 0.0
        self.snippet = ""
        self.polarity   = True
 
    def fillFromRecord(self, record, calib):
        if record==None:
            return
        G = record.GOF
        if G<self.threshold:
            return
        # finally! fill it in
        self.found = True
        self.GOF = G
        self.snippet = record.snippet
        self.polarity = record.finalPolarity( calib )
        return self.polarity


 ##########################################################
#  The official narwhal "object" is an NWObject
#  It is built as a wrapper for NWReader, that manages
#  final polarity interpretation, final "was said" thresholds
#  and structures the "found" data. Currently, few details 
#  are retained from the filled nar: polarity, GOF, and snippet
#  but not which particular nar slots were filled.
class NWObject:
    def __init__(self, treeroot, nars, calibs, thresholds):
        self.numNars = len(nars)
        if not( self.numNars==len(calibs) and self.numNars==len(thresholds)):
            print("Mismatched arguments in NWObject")
            return # no soup for you!

        self.reader = NWReader(treeroot,nars)
        self.reader.setCalibration(calibs)
        self.thresholds = thresholds
        self.infos = []         
        for thresh in thresholds:
            self.infos.append( NarInfo(thresh) )

    def report(self):
        return self.reader.report()
               
    def readText( self, text ):
                # clear the mutable fields
        self.reader.clearAll()
        for info in self.infos:
            info.clear()

        ############# READ ###############
        self.reader.readText( text)
        ##################################

        numToks = len( self.reader.tokens )
       
        ######## TRANSFER WHAT WAS SAID #######
        for n in range( self.numNars ):
            nard = self.reader.narD[n]      # nth narrative read data
            gofMAX = 0.0
            for i in range( numToks +1):       
                record = nard.V.getRecordByCtrl(i)  
                if record==None: # if ith token is not a control
                    continue
             
                info = NarInfo(self.thresholds[n])
                info.fillFromRecord(record, nard.calib)

                if gofMAX<=info.GOF: #want the terminal state, not the initial one
                    gofMAX = info.GOF
                    self.infos[n] = info

        # The last and only sanity check
        p = None
        for info in self.infos:
            if info.found:
                p = info.polarity
                break
        # no polarity 
        if p==None:
            print("NOTHING SAID")
            return

        mixed = False
        for info in self.infos:
            if info.found and info.polarity != p:
                mixed = True
        if mixed:
            print("INCOHERENT")
        else:
            print("COHERENT")
     