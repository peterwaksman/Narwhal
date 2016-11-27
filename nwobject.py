from nwutils import *
from nwtypes import *
from nwcontrol import *
from nwvault import *

##########################################################
#  The official narwhal "object" is an NWObject
#  It is built as a wrapper for NWReader, that manages
#  final polarity interpretation, final "was said" thresholds
#  and structures the "found" data. Currently, few details 
#  are retained from the filled nar: polarity, GOF, and snippet
#  but not which particular nar slots were filled. 
#  Anyway...the NarInfo is a "most final" version of things
# So we have a partially filled nar converted to a NarRecord 
# Which is stored in a vault inside a NarFoundData. Could be
# better organized. Now here, a NarFoundData is converted into 
# final structured form as NarInfo.


# A structured version of  the NarRecord
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

 

class NWObject:
    def __init__(self, treeroot, nars, calibs, thresholds):
        self.numNars = len(nars)
        if not( self.numNars==len(calibs) and self.numNars==len(thresholds)):
           return

        self.reader = NWReader(treeroot,nars)
        self.reader.setCalibration(calibs)
        self.thresholds = thresholds
        self.infos = []         
        for thresh in thresholds:
            info = NarInfo(thresh)
            self.infos.append( info )

    def report(self):
        self.reader.report()
               
    def readText( text ):
                # clear the mutable fields
        self.reader.clearAll()
        for info in self.infos:
            info.clear()

        ############# READ ###############
        self.reader.readText( text)
        ##################################

        numToks = len( self.reader.tokens )
       
        for n in range(self.numNars):
            nard = self.narD[n]      # nth narrative found data
            gofMAX = 0.0
            for i in range(numToks):       
                record = nard.V.getRecordByCtrl(i)  
                if record==None: # if ith token is not a control
                    continue
             
                info = NarInfo(self.thresholds[n])
                info.fillFromRecord(record, calibs[n])

                if gofMAX<info.GOF:
                    gofMAX = info.GOF
                    self.info[n] = info

        # The last and almost only sanity check
        p = self.info[0].polarity  
        for n in range( self.numNars ):
            if self.info[n].polarity != p:
                print("MIXED n="+str(self.info[n].polarity))
            else:
                print("OK") 

 