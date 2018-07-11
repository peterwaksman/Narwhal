#!/usr/bin/env python
""" 
order.py contains the underlying order object and its sub objects - abutments, scanner, etc.
It also implements a MetaOrder object to transfer data from text into that underlying
order. The MetaOrder reads with these (NWTopicReader) NARs:
    makeorder
    getToothNumber  
    getCaseNumber 
    getMarginDepth  
    getABTMaterial 

"""

import sys
import os 
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwutils import *
from narwhal.nwtypes import *

from nbtree import *


class Abutment(object):
    def __init__(self):
        self.tooth_number = 0 # 1-32
        self.material = "Titanium" # Ti or Zr

class Crown(object):
    def __init__(self):
        self.tooth_number = 0
        # etc.

class Order(object):
    def __init__(self):
        self.reference = "" # user-entered order identifier
        self.scanner = "" # the scanner being used in the lab -- 3SHAPE etc.
        #self.tooth_numbering_system = "US" # US, FDI

        self.abutments = [] # abutment objects
        self.crowns = []
########################################################



########################################################
# Stages of completion
STAGENONE = 0
STAGETEETH = 1
STAGEMATERIAL = 2
STAGEABUTMENTS = 3
STAGECROWNS = 4
STAGESCANNER = 5
STAGEREFERENCE = 6
STAGEDONE = 7
LASTSTAGE = 7

# When a response is generated, it is assumed to contain these VARs,
# which will be added to the context.
ResponseVARsAtStage = {
                    STAGENONE : [NULL_VAR],
                    STAGETEETH :  [ORDERSAYS, TOOTH], 
                    STAGEMATERIAL : [TITN, ZIRC] ,
                    STAGEABUTMENTS :  [ABUTMENT, TOOTH],
                    STAGECROWNS  : [NULL_VAR],
                    STAGESCANNER : [SCANNERSAYS],
                    STAGEREFERENCE:[NULL_VAR],
                    STAGEDONE:     [NULL_VAR]
                    }

ResponseAtStage = {  
                    STAGENONE : "\nHow may I help you?",
                    STAGETEETH :  "\nIf you are ready to start ordering, please enter the tooth number(s)",
                    STAGEMATERIAL : "\nDo you want titanium, gold hue titanium, or zirconia abutments?",
                    STAGEABUTMENTS :  "\nDo you want abutments for those tooth numbers?" ,
                    STAGECROWNS  : "\nAre there any details you would like to add?",
                    STAGESCANNER : "\nPlease tell me what kind of scanner do you have?" ,
                    STAGEREFERENCE:"\nWe are almost done. Please create an ID for the order. If you are\
                                    \nusing ScanToOrder(TM) you should use tracking number on the box.",
                    STAGEDONE:     "\n\nPlease submit your patient scans, following instructions\
                                    \non my 'surface'. If you are using ScanToOrder(TM), you will\
                                    \nbe able to review a design in a few minutes and submit the order\
                                    \nat that time. \
                                    \n\nI'll be here if you have any questions."
                  }


def initOrderStages( ):
    done = []
    for i in range(STAGENONE,LASTSTAGE+1):
        done.append(False)
    done[STAGENONE] = True
    #done[STAGECROWNS] = True # this is not a required stage
    return done

class MetaOrder:
    def __init__(self):
        self.scanner = ""
               # these should form the backbone of the data
        self.teeth = bool32()

        
        self.done = initOrderStages()

        self.abtmaterial = str32() #will use slot 0 for name without toothnumber
        self.crown = str32()

        self.abutmentsOK = None # set to True or False
        self.crownsOK = None
        self.orderReference = ''

    def numUnits(self):
        return countBool(self.teeth)

    def responseAtStage(self, stage):
        if stage<STAGENONE or stage>LASTSTAGE:
            return ''
        else:
            return ResponseAtStage[stage]
    
    def responseAtCurrentStage(self):
        for stage in range(STAGENONE,LASTSTAGE+1):
            if not self.done[stage]:
                return ResponseAtStage[stage]
        else:
            return ""

    def responseVARsAtCurrentStage(self):
        for stage in range(STAGENONE,LASTSTAGE+1):
            if not self.done[stage]:
                return ResponseVARsAtStage[stage]
        else:
            return [NULL_VAR]


    """ 
    Design principles for these updateX() functions:
         - Their purpose is to transfer NWTopicReader into local data objects.
         The updates are said to "fill" the parts of the data.
         - There should be one update fn for each part of local data (a single 
        updateX() *could* fill more than one part). 
         - They should return True or False depending on whether their 
         data is changed. Refilling with the same values is sometimes considered 
         a change, for consistency of the parent logic.
         For the moment, they are much too tightly coupled to NWTopicReaders
         from the client.
    """
    def updateTeeth(self, tnum, mkorder):
        if not tnum or tnum.GOF<0.5:
            return False

       # to prevent seeing a tooth number in "I want 3 abutments"
        if tnum.GOF<=0.5 and mkorder.GOF>=0.6 and mkorder.GOF<0.75:
            return False

        polarity = tnum.nar.polarity #turn tooth on or off

        if polarity and mkorder:
            polarity = mkorder.nar.polarity   

        for event in tnum.eventrecord:
            if event[0]<0.5:
                continue
            if not Value(event[1]):
                continue

            ntooth = int( Value(event[1]) )

            if 0<ntooth and ntooth<33:
                if not self.abtmaterial[ntooth] and not self.crown[ntooth]:
                    self.teeth[ntooth] = polarity
                    if not polarity: # cannot use "not" twice
                        mkorder.nar.polarity = True
                elif self.abtmaterial[ntooth] and not polarity:
                    self.abtmaterial[ntooth] = False
                    if not self.crown[ntooth]:
                        self.teeth[ntooth] = False
                    mkorder.nar.polarity = True

                if self.abtmaterial[0] and not self.abtmaterial[ntooth]:
                    if polarity:
                        self.abtmaterial[ntooth] = self.abtmaterial[0]
                    else:
                        self.abtmaterial[ntooth] = ''

        self.done[STAGETEETH] = True
        return True

    def updateAbutments( self, mkorder ):
        if not mkorder or mkorder.GOF<0.5:
            return False
      
        polarity = mkorder.nar.polarity # can negate an order
    
        if mkorder.GOF==0.5 and not polarity:
            self.done[STAGETEETH] = False
            self.done[STAGENONE] = False
            return True


        ok = mkorder.GOF>0.5
        for event in mkorder.eventrecord:
            if event[0] >= 0.5:
                ok = True
                r = Relation( event[1] )
                if r=='abutment':
                    self.done[STAGEABUTMENTS] = True
                    self.abutmentsOK = polarity
                elif r=='crown':
                    self.done[STAGECROWNS] = True
                    self.crownsOK = polarity
                    if polarity:
                        self.crown[0] = 'True'
                    else:
                        self.crown[0] = 'False'
                    if polarity :
                        for n in range( 0, len(self.teeth) ):
                            if self.teeth[n]:
                                s = self.crown[n]
                                if len(s)==0:
                                    s = 'crown'
                                self.crown[n] = s

                    #for n in range(1, len(self.teeth)):
                    #        if self.teeth[n]:
                    #            self.crown[n] = 'crown'

        if not polarity and countBool(self.teeth)<=1:
            self.teeth = bool32()
            self.done[STAGETEETH] = False
            self.done[STAGEABUTMENTS] = False
            self.done[STAGENONE] = False # special circumstance, where there is no data (again)

        return ok

    def updateCrowns( self, getCrown):
        if not getCrown:
            return False

        p = getCrown.nar.polarity

        r = Relation( getCrown.nar.lastConst  )
        s = 'crown'
        for event in getCrown.eventrecord:  
            r = Relation( event[1] )
            #embarrisingly awkward, to save the more particular value
            if r != 'crown':
                s = r
            r = s


        # special case for one tooth (implicit, since already named)
        numfound = 0
        theN = -1
        if getCrown.GOF==0.5 and r:
            for n in range(1, len(self.teeth)):
                if self.teeth[n]:
                    numfound = numfound+1
                    theN = n
            if numfound==1: 
                if p:
                    self.crown[theN] = r
                else:
                    self.crown[theN] = ''
                return True
            elif numfound>0: # added
                for n in range(1, len(self.teeth)):
                    if self.teeth[n]:
                        self.crown[n] = r
                return True
            else:
                return False

        if getCrown.GOF<=0.7 :
            return False
 
        s = 'crown'
        for event in getCrown.eventrecord:  
            r = Relation( event[1] )
            #embarrisingly awkward, to save the more particular value
            if r != 'crown':
                s = r
            r = s

            v = Value( event[1] )
            if v and asInt( v ):
                n = int( asInt( v ) )
                if 0<n and n<33 :
                    if p:
                        self.crown[n] = r
                        self.teeth[n] = True
                    else:
                        self.crown[n] = ''
        return True             

    def updateMaterial( self, getMat ):
        if not getMat or getMat.GOF<0.5:
            return False

        ok = False
        theN = -1
        for event in getMat.eventrecord:   
            r = Relation( event[1] )
            val = Value( event[1] )
            if event[0]>0.3 :
                ok = True
                if r == 'titanium' or r=='zirconia' or r=='goldTi':
                    self.done[STAGEMATERIAL] = True    
                    self.done[STAGEABUTMENTS] = True            
                if asInt( val ):
                    n = int( asInt(val) )
                    if 0<n and n<33 :
                        self.abtmaterial[n] = r
                        self.done[STAGETEETH] = True
                        self.teeth[n] = True
                        theN = n
                else:
                     self.abtmaterial[0] = r


        # move default material (at zero) to all un-committed teeth
        if ok:
            for n in range(1,33):
                if n==theN:
                    continue
                if self.teeth[n]==True and self.abtmaterial[n]=='':
                    self.abtmaterial[n] = r

        return ok

    def updateScannerType(self, getScanner ):
        if not getScanner or getScanner.GOF<0.5:
            return False
        L = len( getScanner.eventrecord)
        if L>0:
            event = getScanner.eventrecord[L-1]
            t = Thing( event[1] )
            v = Value( event[1] )
            if t==v: #(the only check I can think of)
                #self.scanner = v
                self.done[STAGESCANNER] = True  
                self.scanner = v
                return True
        else:
            return False

    ######################################################


    def simpleOrderString(self):
        r = ''

        if self.scanner:
            r = "Scanner: " + self.scanner

        r += "\nOrder ID=" + self.orderReference + "\n"
        r += str( countBool(self.teeth) )
        if self.abutmentsOK:
            r += " abutment"
        if self.crownsOK:
            r += " /crown" 
        r += " unit(s)" 
                
        for i in range(1,len(self.teeth)):
            if self.teeth[i]:
                r += "\n#"+str(i)+ " in "
                if self.abtmaterial[i]!='':
                    r += self.abtmaterial[i]
                else:
                     r += self.abtmaterial[0] 

                if self.crown[i]!='':
                    r += "(+" + self.crown[i] + ")"
        return r

    def getOrder(self):
        order = Order()
        
        order.reference = self.orderReference

        if self.scanner:
            order.scanner = self.scanner

        mat = self.abtmaterial[0] 
#        if (self.abutmentsOK or self.crownsOK) and countBool( self.teeth )>0:
        if countBool( self.teeth )>0:
            for i in range(1,33):
                if self.teeth[i]:
                    ABT = Abutment()

                    if self.abtmaterial[i] != '':
                        ABT.material = self.abtmaterial[i]
                    else:
                        ABT.material = mat

                    ABT.tooth_number = i

                    if self.crown[i] != '':
                        ABT.crown = self.crown[i]
                        c = Crown()
                        c.tooth_number = i;
                        order.crowns.append(c)

                    order.abutments.append( ABT )
        
        # transfer reference

        # transfer scanner name

        return order

