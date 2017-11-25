import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
 
from AbtTree import *  
from AbtSketch import *

SENSE_CUTOFF = 0.3

AOK = 0 # agree
ANOK = 1 # apologize but "no"
AQU = 2 # ask clarifaction


aResponse = {
    AOK : "ok",
    ANOK: "I {}",
    AQU : "please clarify {}"
    }

aResponseV = {
    AOK : [],
    ANOK : [],
    AQU : []
    }

AbutmentResponder = NWTopicResponder(aResponse, aResponseV)

###################################################
# Design is that you change the abtstate to change the scene data

class AbutmentChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, AbutmentTopic, AbutmentResponder)
        
        self.data     = AbutmentState()
        self.prevdata = AbutmentState()
         
        self.sketch = AbutmentSketch()
        self.caveat = ''   # for out-of-bounds warning 

    def Read(self, text):
        self.caveat = ''
        self.prevdata.copy(self.data) # keep copy
        NWTopicChat.Read(self, text)


    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return

        data = self.data #for convenience
        for reader in self.topic.readers:
            id = reader.id

            t = reader.getLastThing()
            a = reader.getLastAction()
            r = reader.getLastRelation()
            v = reader.getLastValue()
            T = reader.getLastThingVAR()
            A = reader.getLastActionVAR()
            R = reader.getLastRelationVAR()
            V = reader.getLastValueVAR()

           
            polarity = reader.nar.polarity

            if id=='epsReader' and reader.GOF>=0.75:
                if v=='convex':
                    data.epsshape = CONVEXEPS
                elif v=='concave':
                    data.epsshape = CONCAVEEPS
                elif v=='straight':
                    data.epsshape = STAIGHTEPS
                elif v=='ankylos':
                    data.epsshape = ANKYLOSEPS

                data.setEPSParams( self.sketch )

            elif id=='relationReader' and reader.GOF>=0.75: 
                if t=='gingiva':
                    data.mref = GUMREF
                    if r=='above':
                        data.mamt = ABOVEAMT 
                    elif r=='below':
                        data.mamt = BELOWAMT
                    elif r=='at':
                       data.mamt = ATAMT
                    elif r=='closest':
                        data.mamt = CLOSEAMT  
                data.setMarginReference( self.sketch ) 

            elif id == 'coreReader' and reader.GOF>=0.75:
                if v=='thick':
                    data.core = FATCORE
                elif v=='thin':
                    data.core = THINCORE
                elif v=='normal':
                    data.core = NORMALCORE

                data.setCoreThickness( self.sketch, data.core )
                     
 


    def write(self):
        return self.responder.getStageResponse()
