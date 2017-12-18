import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *
from stdtrees.tchats import *
 
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
        
        # don't implement data ownership
        self.data     = None
         
        # assumes the data is an AllAbutments
    def SetData(self, data):
        self.data = data # a reference, not a copy

    def fillData(self, Vault, toothno):
        rel = ''
        ref = ''
        margin = self.data.margin[toothno]  
        for v in Vault:
            lc = v.lastConst

            side = Thing(lc)

            amount = Action(lc)
            a = float(amount)
            if not a:
                a = 0

            r = Relation(lc)
            f = Value(lc) 
            
            if len(r)>0:
                rel = r
            if len(f)>0:
                ref = f

            spec = MarginSpec(rel,ref,a)
            if side=='mesial':
                margin.M = spec
            elif side=='distal':
                margin.D = spec
            elif side=='facial':
                margin.F = spec
            elif side == 'lingual':
                margin.L = spec
            else:
                margin.M = spec
                margin.D = spec
                margin.F = spec
                margin.L = spec

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return

                # margin reader, side surface reader  
        mReader = self.topic.readers[0]
        mtReader = self.topic.readers[1]
         
        polarity = mReader.nar.polarity # assume it is same for both nars
              
        side = mReader.getLastThing()
        amount = mReader.getLastAction()
        rel = mReader.getLastRelation()
        ref = mReader.getLastValue()     
        V = mReader.reader.vault._vault   

        feature = mtReader.getLastThing()      
        toothword = mtReader.getLastRelation()
        toothno = mtReader.getLastValue()
         
        # feature can be missing but not something else
        if feature != 'margin' and feature != '':
            return
        t = 0
        if toothno.isdigit():
            t = int(toothno)

        
        self.fillData( V, t )

    def write(self):
        return self.responder.getStageResponse()


####################################################

class DentalChat(  NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, ToothNumTopic, DefaultResponder())

        # root piece of data
        self.sites = ToothSites()

        # language UI for one part
        self.abutmentChat = MarginChat() + BaseChat()
        self.abutmentChat.SetData(self.sites.abutments)
     
    def Read(self, text):
        self.abutmentChat.Read(text)
        x = 2

  