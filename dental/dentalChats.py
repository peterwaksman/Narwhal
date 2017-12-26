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

from abtSketch2 import AbutmentSketch

SENSE_CUTOFF = 0.3

BaseResponder = DefaultResponder() #NWTopicResponder(aResponse, aResponseV)

###################################################
class BaseChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, BaseTopic, BaseResponder)
        
        self.data = None       
        self.caveat = ''   # for out-of-bounds warning 

    def SetData( self, data):
        if isinstance(data, AllAbutments):
            self.data = data.base
        else:
            self.data = data #??

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return

        self.responder.stage = AOK  

        data = self.data #for readablity

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
                data[0].eps.value = v
                self.responder.stage = AOK
                self.caveat = 'setting emergence profile ' + v
      
            elif id=='tpReader' and reader.GOF>=0.66: 
                data[0].pressure.value = float(v)
                self.responder.stage = AOK
                self.caveat = 'setting tissue pressure to ' + v 

            elif id=='tpReader2' and reader.GOF>=0.66: 
                if v=='weak' or (polarity==False and v=='strong' ):
                    data[0].pressure.value = 0.1
                    self.responder.stage = AOK
                    h = str( 0.1 )
                    self.caveat = 'setting tissue pressure to ' + h
                    x=2
 
    def write(self):
        s = self.responder.getStageResponse().format(self.caveat)
        return s

################################################

class MarginChat( NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, MarginTopic , DefaultResponder())
        
        # don't implement data ownership
        self.data     = None
         
    def Read(self, text):
        NWTopicChat.Read(self,text)
                # implement a policy for 0.5
        if self.gof==0.5:
            self.gof = 0 # so many implicits, when down to .5 you got nothin

        # assumes the data is an AllAbutments
    def SetData(self, data):
        if isinstance(data, AllAbutments):
            self.data = data.margin
        else:
            self.data = data # a reference, not a copy

    def fillData(self, Vault, toothno):
                        
        margin = self.data[toothno]  # allows toothno==0

        outtext = ''
        rel = ''
        ref = ''
        for v in Vault:
            lc = v.lastConst

            side = Thing(lc)

            amount = Action(lc)
            if amount and float(amount):
                a = float(amount)
            else:
                a = 2.0 # or use customer pref

            r = Relation(lc) # stores the relation
            f = Value(lc) # stores the reference feature
            
            if len(r)>0:
                rel = r
            if len(f)>0:
                ref = f

            if len(r)*len(f)==0 and side=='': # yu need something
                return outtext

            if len(r)*len(f)==0 and isinstance(spec,MarginSpec):
                spec.value = a
            else:
                spec = MarginSpec(rel,ref,a)

            isset = False
            if side=='mesial' or side=='md': # code is probably simpler using 'MD'    
                margin.M = spec
                isset = True
                outtext += ' mes margin '
            if side=='distal' or side=='md':
                margin.D = spec
                isset = True
                outtext += ' dist margin '

            if side=='facial' or side=='bf' or side=='labial':
                margin.F = spec
                isset = True
                outtext += ' bf margin '

            if side == 'lingual':
                margin.L = spec
                isset = True
                outtext += ' ling margin '

            if side=='remainder':
                print(" NOT IMPLEMENTED, use init values as signal?")
                isset = True
                outtext += ' others at '

            if not isset or side=='all':
                margin.M = spec
                margin.D = spec
                margin.F = spec
                margin.L = spec         
                outtext = ' all margins '
             
            outtext += str(a) + ' ' + rel + ' ' + ref

        return outtext

    def update(self):
        NWTopicChat.update(self)
        if self.gof==0:
            self.responder.stage = AQU  
            return
        
        self.responder.stage = AOK              

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

        if side=='' and amount=='' and ref=='':
            self.responder.stage = AQU              
            self.caveat = ''
            return
         
        # feature can be missing but not set to something else
        if feature != 'margin' and feature != '':
            return

        t = 0
        if toothno.isdigit():
            t = int(toothno)
        
        c = self.fillData( V, t)
        self.caveat = c

    def write(self):
        return self.responder.getStageResponse().format(self.caveat)


####################################################

class DentalChat(  NWTopicChat ):
    def __init__(self):
        NWTopicChat.__init__(self, ToothTopic, DefaultResponder())

        # root piece of data
        self.sites = ToothSites()

        self.sketch = AbutmentSketch()


        # language UI for one part
        self.abutmentChat = MarginChat() + BaseChat()
        self.abutmentChat.SetData(self.sites.abutments)

    
    def Read(self, text):
        self.abutmentChat.Read(text)
        self.gof = self.abutmentChat.gof
        x = 2

    def Write(self):
        s = self.abutmentChat.Write()
        return s

    def draw(self):
        self.sites.draw( self.sketch )