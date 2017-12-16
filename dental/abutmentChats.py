import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
 
from dentalTree import *  
from dentalData import *


SENSE_CUTOFF = 0.3

BaseResponder = DefaultResponder() #NWTopicResponder(aResponse, aResponseV)

###################################################
class BaseChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, BaseTopic, BaseResponder)
        
        # implement data
        self.data     = AbutmentBase()
        self.prevdata = AbutmentBase()
         
        #self.caveat = ''   # for out-of-bounds warning 

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
                data.eps.value = v
                self.responder.stage = AOK
            
            elif id=='tpReader' and reader.GOF>=0.66: 
                data.pressure.value = float(v)
                self.responder.stage = AOK

            elif id=='tpReader2' and reader.GOF>=0.66: 
                if v=='weak' or (polarity==False and v=='strong' ):
                    data.pressure.value = 0.1
                    self.responder.stage = AOK
               
 
    def write(self):
        return self.responder.getStageResponse()

################################################

class MarginChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, MarginTopic , DefaultResponder())
        
        # implement data
        self.data     = MarginData()
        self.prevdata = MarginData()

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return

                # margin reader  
        mReader = self.topic.readers[0]
        margin = mReader.getLastThing()
        amount = mReader.getLastAction()
        rel = mReader.getLastRelation()
        ref = mReader.getLastValue()  
          
        polarity = mReader.nar.polarity # assume it is same for both nars

                # tooth and side surface reader (no action)
        mtReader = self.topic.readers[1]
        tmargin = mtReader.getLastThing()      
        toothno = mtReader.getLastRelation()
        side = mtReader.getLastValue()
        x=2
        #setMarginData( data, margin, amount, rel, ref, side, toothno, side)

    def write(self):
        return self.responder.getStageResponse()