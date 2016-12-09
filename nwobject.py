from nwutils import *
from nwtypes import *
from nwcontrol import *
from nwvault import *
from nwread import *


MIXED_POLARITY=0
UNDEFINED_POLARITY=10
POSITIVE_POLARITY=1
NEGATIVE_POLARITY=-1

 ##########################################################
#  The official narwhal "object" is an NWObject
#  It is built as a wrapper for NWReader, that manages
#  final polarity interpretation, final "was said" thresholds
#  and structures the "found" data. Currently, few details 
#  are summarized, mainly max GOF and polarity per nar
class NWObject:
    def __init__(self, treeroot, nars, calibs, thresholds):
        self.numNars = len(nars)
        if not( self.numNars==len(calibs) and self.numNars==len(thresholds)):
            print("Mismatched arguments in NWObject")
            return # no soup for you!
        
        ## fixed at construction time
        self.reader = NWReader(treeroot,nars)
        self.reader.setCalibration(calibs)
        self.thresholds = thresholds

        ## output after reading
        self.gofMax = []
        self.finalPolarity = []
        self.totalPolarity = UNDEFINED_POLARITY
        self.numToks = 0

        self.clear()

    def clear(self):
        self.totalPolarity = UNDEFINED_POLARITY
        self.numToks = 0
        self.gofMax = []
        self.finalPolarity = []

        for n in range( self.numNars ):

            self.gofMax.append( 0.0 )
            self.finalPolarity.append(UNDEFINED_POLARITY)
            
    def printFinal(self):
        #out = ""
        #for n in range( self.numNars ):
        #    out += str(self.gofMax[n]) + "," + str( self.finalPolarity[n]) + " "
        #print(out + "\n")
 
        out = ""
        polarity = self.totalPolarity
        if polarity==POSITIVE_POLARITY:
            out = "coherent +"
        elif polarity==NEGATIVE_POLARITY:
            out = "coherent -"
        elif polarity==MIXED_POLARITY:
            out = "incoherent"
        else:
            out = "nothing was said"         
        return out       
                   
    def report(self):
         return self.reader.report()

     # run through the vaults, find maxGOF/polarity for each
    def summarize(self):
        numToks = self.numToks
        for n in range( self.numNars ):
            rd = self.reader.RD[n]      # nth narrative read data
            cal = self.reader.RD[n].calib
            thresh = self.thresholds[n]

            lastPolarity = UNDEFINED_POLARITY
            maxGOF = 0.0
            
            # find max GOF and final polarity for each nar
            for i in range( numToks +1):       
                record = rd.V.getRecordByCtrl(i)  
                if record==None: # if ith token is not a control
                    continue

                G = record.GOF
                if G<thresh:
                    continue
                
                if G>=maxGOF:
                    maxGOF = G;
                    lastPolarity = record.finalPolarity( cal )

            if maxGOF>0: # if one gof above threshold
                self.gofMax[n] = maxGOF
                self.finalPolarity[n] = lastPolarity
            else:
                self.gofMax[n] = 0.0
                self.finalPolarity[n] = UNDEFINED_POLARITY
                # The last and only sanity check

        polarity = UNDEFINED_POLARITY
        for n in range( self.numNars ):
            if self.finalPolarity[n]==UNDEFINED_POLARITY:
                continue
            
            if polarity==UNDEFINED_POLARITY:
                polarity = self.finalPolarity[n] # first "defined" polarity
        
            if polarity != self.finalPolarity[n]:# look for conflicts
                self.totalPolarity = MIXED_POLARITY
                break
            
        if polarity==UNDEFINED_POLARITY:
            self.totalPolarity = UNDEFINED_POLARITY          
        elif polarity==True:
            self.totalPolarity = POSITIVE_POLARITY
        elif polarity==False:
            self.totalPolarity = NEGATIVE_POLARITY    
        else:
            self.totalPolarity =  MIXED_POLARITY            

        return self.totalPolarity
               
    def readText( self, text ):
        self.clear()
        self.reader.clearAll()

        ############# READ ###############
        self.reader.readText( text)
        ##################################

        self.numToks = len( self.reader.tokens )
        polarity = self.summarize(  )

        return polarity
        
