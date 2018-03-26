#!/usr/bin/env python

import sys
import os 
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwutils import *
from narwhal.nwchat import *
from stdtrees.quantities import *
from stdtrees.ask import *
from nbtree import *
from order import *
from query import MetaQuery

######################################################
######################################################
######################################################
"""
A first attempt at a mult-topic entity. Hopefully to be deprecated.
"""
# init with an array of TopicFamilies
class NWChat():
    def __init__(self, topics):
        self.topics = topics
        self.updated = False # becomes true when stored data is changing
        self.numtokens = 0   #you'll see why this is helpful
        self.stringmode = False
        self.responseVARs = []

        self.log = NWLog()
        self.loggingOn = True

    def read(self, text ):
        if self.loggingOn:
            self.log.add("Q: "+text + "\n")

        for topic in self.topics:
            topic.read( text )         
            self.numtokens = topic.numtokens
            print( topic.summary() )

         # absorb the info
        self.updateAll()

    def updateAll(self):
        """ 
        To be overridden in derived classes. Assuming a derived class contains a data object "meta"
        and a narrative narX, we might call meta.updateX( narX ) after a read() and consider accessing 
        these sorts of values 
         - is narX==None?
         - is narX.GOF>=0.5? (The goodness of fit of the narX to the text)
         - is narX.polarity True or False? (False means a negative of some kind)
         - is len( narX.eventRecord )>0?
         for event in narX.eventRecord:
            access event[0], the event GOF 
            access event[1] content with Thing(event[1]), Action(event[1]), 
            Relation(event[1]), or Value(event[1]) 
        access narX.lastConst (also via the Thing(), Action(), Relation(), Value() functions
        """
        x=2 # do nothing. override in derived classes


    def RespondNext( self ):
        x = 2 # override in derived classes


    def respondNext( self ):
        self.responseVARs = [] # to store internally generated VARs for addition to the context

        response = self.RespondNext() # also sets the self.responseVARs, per derived class

        for topic in self.topics:
            #topic.context.extend( self.responseVARs )
            topic.Context.addSegment( self.responseVARs )

        if self.loggingOn:
            self.log.add("A: "+ response + "\n\n")

        return response

 
    def getTopic(self, id ):
        for topic in self.topics:
            if topic.tree.knames[0]==id :
                return topic

    # tid and nid are, respectively, names of a topic reader and its (sub) TREE
    def getReader( self, tid, nid):
        topic = self.getTopic( tid )
        if topic:
            return topic.getReader( nid )


class NBChat( NWChat ):
    def __init__(self ):
                
        NWChat.__init__(self, chattopics )

        self.myorder = MetaOrder()
        self.myquestion = MetaQuery()

        self.abutmentsOKPending = False
        self.materialPending = False
        #self.scannerPending = False
        self.orderReferencePending = False
        self.okcount = 0

        self.updated = ''

        # order reference is a random string
        self.string = ''
        #self.stringmode = False

    def read( self, text ):
        if self.stringmode:
            self.string = text
            return
        NWChat.read( self, text )
        #petersWorld(self)

    def clear(self):
        self.myorder = MetaOrder()
        self.myquestion = MetaQuery()

        self.abutmentsOKPending = False
        self.materialPending = False
        #self.scannerPending = False
        self.okcount = 0
        self.responseVARs = []


        #################### YES NO
    def updateYesNo(self):
        yn = self.getReader('yesno','yesno')
        if not yn:
            return None
        if not yn.eventrecord:
            return None
        
        # extact the yes or no - quite a hassle
        isYes = None
        event = yn.eventrecord[0]
        if event[0]>=0.5:
            if Value(event[1])=='YES':
                isYes = True
            elif Value(event[1])=='NO':
                isYes = False
        else:
            return None

        # apply yes/no to the pending confirmation
        if self.abutmentsOKPending:
            self.abutmentsOK = isYes
            if isYes:
                self.myorder.done[STAGEABUTMENTS] = True    
                self.myorder.done[STAGECROWNS] = True # not really a stage
                self.myorder.abutmentsOK = True
            # clear the pending flag
            self.abutmentsOKPending = False

        if self.materialPending and not isYes:
            self.myorder.done[STAGEABUTMENTS] = True    
            self.materialPending = False

        if self.orderReferencePending:
            if isYes:
                self.myorder.orderReference = self.string
                self.orderReferencePending = False
                self.myorder.done[STAGEREFERENCE] = True


        return True              
              
    def updateAll( self ):
        gof = 0.0
        for topic in self.topics:
            if gof < topic.maxGOF:
                gof = topic.maxGOF      
        if gof==0.0:
            self.updated = ''
            return ''

        self.updated = ''
    
        x = self.myorder.updateTeeth( self.getReader('ordersays','toothno'),
                                      self.getReader('ordersays','makeorder')  )
        y = self.myorder.updateAbutments(     self.getReader('ordersays','makeorder') )
        z = self.myorder.updateMaterial(      self.getReader('ordersays','getmaterial'))
        
        R0 = self.getReader('ordersays', 'getcrowntooth')
        R1 = self.getReader('ordersays', 'getcrownXtooth')
        if R0 and R1 and R1.GOF > R0.GOF:
            k = self.myorder.updateCrowns( R1)
        else:
            k = self.myorder.updateCrowns( R0 )

        q = self.myorder.updateScannerType(  self.getReader('scannersays','scantype') )
        #if self.scannerPending:
        #    self.scannerPending = False
        #    self.myorder.done[STAGESCANNER] = True

        if x or y or z or q:
            self.updated = 'order'

        self.myquestion.response = ''
        self.myquestion.action = []
        x = self.myquestion.updateHi(          self.getReader('clientsays','hi'))
        y = self.myquestion.updateAbout(       self.getReader('clientsays','about') )
        z = self.myquestion.updateAccount(     self.getReader('clientsays','account') )
        w = self.myquestion.updateProductInfo( self.getReader('clientsays','productinfo') )
        order = self.myorder.simpleOrderString()
        u = self.myquestion.updateOrderInfo(   self.getReader('clientsays','orderinfo'), order )
        v = self.myquestion.updateMaterialInfo(self.getReader('clientsays', 'askmaterial') )
 

        if x or y or z or w or u or v:
            self.updated = 'question' 

        if self.updateYesNo():
            self.updated = 'y'


        if not self.updated and self.materialPending:
            v = self.myquestion.updateMaterialInfo(self.getReader('clientsays', 'askmaterial'))
            self.materialPending = False
            if v:
                self.updated = 'question'

    def RespondNext( self ):
        if self.stringmode: #currently used ONLY for order reference ID
            self.stringmode = False
            r = "You entered: " + self.string + "\n"
            r += "Is this correct?"
            self.orderReferencePending = True
            return r


        self.materialPending = False

        if self.updated=='':
            if self.numtokens==1:
                r= "I am not good with single words. Can you be more explicit?"
            else:
                r = "I don't understand. Can you be more explicit?\nOr can I help with something else?" 

            h = self.myorder.responseAtCurrentStage()
            if len( h )>0 :
                r += "\n" + h       
            # (here no change to the responseVARs)          
            return r

        elif self.updated == 'question':
            r = self.myquestion.response
            r += self.myorder.responseAtCurrentStage()

            self.responseVARs = self.myorder.responseVARsAtCurrentStage()  
           
            return r
        elif self.myorder.done[STAGENONE]==False: 
            r = self.myorder.responseAtStage(STAGENONE)
            self.responseVARs = self.myorder.responseVARsAtCurrentStage()  
            return r

  
        r = ""
        if not self.myorder.done[STAGETEETH]:
            r += self.myorder.responseAtStage(STAGETEETH) 
            
        elif not self.myorder.done[STAGEMATERIAL]:
            if self.okcount==0:
                r += self.myorder.responseAtStage(STAGEMATERIAL)
                self.materialPending = True
                self.okcount = 1
            else: # so customer said no to ANY abutment
                r += self.myorder.simpleOrderString() + "\n"
                r += self.myorder.responseAtStage(STAGEMATERIAL)               
                self.okcount = 0

        elif not self.myorder.done[STAGEABUTMENTS]:
            if self.okcount==0: 
                r += self.myorder.responseAtStage(STAGEABUTMENTS) 
                self.okcount = 1
                self.abutmentsOKPending = True

            else: # (so customer already said "no" once)
                r += "OK, let's leave that blank for now\n"
                r += self.myorder.simpleOrderString()
                r += "\n\n" + strDETAILS 
                self.okcount = 0
                self.myorder.done[STAGEABUTMENTS] = True
               

        elif not self.myorder.done[STAGESCANNER]:
            r = self.myorder.simpleOrderString() + "\n"
            if self.okcount==0:
                r += strDETAILS + "\n"
                self.okcount = 1              
            else:
                 #
                r += self.myorder.responseAtStage(STAGESCANNER)
                #self.scannerPending = True

        elif not self.myorder.done[STAGEREFERENCE]:
                r += self.myorder.simpleOrderString() + "\n"
                r += self.myorder.responseAtStage(STAGEREFERENCE)
                self.myquestion.action.append( { 'SCAN':"" } )
                self.stringmode = True

        elif not self.myorder.done[STAGEDONE]:
             r += self.myorder.responseAtStage(STAGEDONE) 

        self.responseVARs = self.myorder.responseVARsAtCurrentStage()  

        if r=='':
            r = "Oops. My programmers did NOT anticipate that"

        return r

    def getOrder(self):
        return self.myorder.getOrder()

    def getAction(self):
        return self.myquestion.action
