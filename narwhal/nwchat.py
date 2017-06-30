from narwhal.nwtypes import *
from narwhal.nwutils import *
from narwhal.nwcontrol import *
from narwhal.nwvault import *
from narwhal.nwnreader import *

from stdtrees.quantities import QUANTITY

strAPOLOGY = "Sorry, I did not understand that."
strINFO = "Here is an link article about"
"""
This defines the NWChatnode base class and the ChatManager that
manages a system of multiple NWChatnodes.
"""

class NWResponder():
    def __init__(self):
        self.node = None

    def respond(self, text):
        s = self.node.respondText(text)
        if self.node.pending:
            s = self.node.respondText('')
        return s

    def getContext(self):
        s = self.node.getContext()
        return s

######################################

class NWChatnode():
    def __init__(self, treeroot, nars, cals = []):
        self.tree = treeroot.copy()
        self.nreaders = []
        i = 0
        for nar in nars:
            if len(cals)==0:
                self.nreaders.append( NWNReader( nar, False) )
            else:
                self.nreaders.append( NWNReader( nar, cals[i] ))
                i += 1
    
        self.ibest = -1    # index of bet fit narrative
        self.maxGOF = 0.0  # goodness of fit
        self.response = "" # what chatbot says back

        self.responder = None # needs to be set externally
        #self.responder = self # who currently answers questions

        self.parent = self # sub classes may take a parent CTOR argument
                           # it is used to return control
        self.lastConst = ""

        self.pending = False

    def updatePending(self):
        self.pending = False

    def bestFitI(self):
        ibest = -1
        max = 0.0
        lastConst = ""
        for i in range(len(self.nreaders)):
            N = self.nreaders[i]
            v = N.vault.maxGOF()
            if max < v:
                max = v
                ibest = i
                lastConst = N.vault.lastConst()

        self.maxGOF = max
        self.lastConst = lastConst
        return ibest

    def readAll( self, segment, tokens ):
        """basic read method, do not call directly. Use respond() """
        for N in self.nreaders:
            N.readText(segment,tokens)

    #----Typically the next two methods get overriden in derived classe
    def getContext(self):
        ibest = self.ibest
        return str(ibest)
  
    def read(self, segment, tokens):

        self.readAll( segment, tokens)# does the read
 
        self.ibest = self.bestFitI() # collects the GOFs

        ibest = self.ibest
        if ibest<0:
            self.response = strAPOLOGY
            return ibest
    
        # For debug
        N = self.nreaders[ibest]   
        s = N.vault.lastConst() 
        h = self.getContext() 
        print(h + " " + s)
        #print("\n")
        return ibest


    def respondText(self, text):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree,tokens)
        self.read( segment, tokens )
        return self.response

   # if you cannot do this at construction, do it later
   # it does not change the responder, just this instance
    def setParentAndResponder(self, parent, responder):
        self.parent = parent        
        self.responder = responder  
 
    def getResponder(self):
        return self.responder

    def restoreParentControl(self):
        self.responder.node = self.parent  


class NWDatanode():
    def __init__(self, id, treeroot, nar, cal=False):
        self.id = id

        self.tree = treeroot.copy()
        self.nar = nar # convenient to use outside the reader
        self.reader = NWNReader( nar, cal )

        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''
        self.eventGOF = 0.0

    def clear(self):
        self.lastConst = ''
        self.GOF = 0.0
        self.eventrecord = ''

    def read( self, text ):
        tokens = prepareTokens(text)
        segment = PrepareSegment(self.tree, tokens) #not efficient, could do this at higher level,
 
        self.clear()

        # look for structured data
        self.eventrecord = recordSlotEvents( self.nar, segment )
        self.eventGOF = maxEventGOF( self.eventrecord )

        # freeform read
        self.nar.clear()
        self.reader.readText(segment,tokens)
        self.GOF = self.reader.vault.maxGOF()
        self.lastConst = self.reader.vault.lastConst #the method not the value

    def getEvents(self):
        out = ''
        for event in self.eventrecord:
            out += event[1] + ", "
        return out

    def summary(self):
        g = self.GOF
        k = int(1000*g)
        g = float(k)/1000.0
        if self.nar.polarity==False and g>0:
            g = -g
        e = self.eventGOF
        L = self.getEvents()
        ID = self.id.ljust(15)
        out = ID +  "g=" + str(g).ljust(5) + " " + "    e=" + str(e).ljust(5) + "    events=" + L
        return out


    #######################

def bool32( ):
    array = []
    for i in range(33):
        array.append(False)
    return array
def str32():
    array = []
    for i in range(33):
        array.append('')
    return array


class NWChat():
    def __init__(self, R):
        self.nodes = R
        self.maxGOF = 0.0
        self.updated = False # becomes true when stored data is changing

    def read(self, text ):
        self.maxGOF = 0.0
        for node in self.nodes:
            node.read( text )
            if self.maxGOF<node.GOF:
                self.maxGOF= node.GOF
            print( node.summary() )

         # absorb the info
        self.updateAll()

    def updateAll(self):
        x=2 # do nothing. override in derived class

    def getNode(self, id ):
        for node in self.nodes:
            if node.id==id :
                return node
   
            
#######################################################
#######################################################
#######################################################




class NBChat( NWChat ):
    def __init__(self, R):
        
        NWChat.__init__(self,R )

        self.inforesponse = ''

        # these should form the backbone of the data
        self.teeth = bool32()

        self.abtmaterial = ''#str32() #will use slot 0 for name without toothnumber

        self.abutmentsOK = False
        self.abutmentsOKPending = False
        self.crownsOK = False
        #self.crownsOKPending = False
        self.okcount = 0

            
    # after a read
    def updateTeeth( self ):
        t = self.getNode('toothno')
        mkorder = self.getNode('makeorder') # to disambiguate
        if mkorder.GOF==1 and t.GOF<=0.5:
            return

        for event in t.eventrecord:
            if event[0]<0.5:
                continue
            if not Value(event[1]):
                continue
            ntooth = int( Value(event[1]) )

            if 0<ntooth and ntooth<33:
                self.teeth[ntooth] = True

    def updateAbutments( self ):
        mkorder = self.getNode('makeorder')

        polarity = mkorder.nar.polarity # can negate an order
          
        for event in mkorder.eventrecord:
            if event[0] >= 0.5:
                r = Relation( event[1] )
                if r=='abutment':
                    self.abutmentsOK = polarity
                elif r=='crown':
                    self.crownsOK = polarity
        if mkorder.GOF>0.6:
            return True


     
    def updateMaterial( self ):
        getMat = self.getNode('getmaterial') 
        askMat = self.getNode('askmaterial')
        if askMat.GOF>getMat.GOF :
            return True
        for event in getMat.eventrecord:   
            r = Relation( event[1] )
            val = Value(event[1])
            if event[0]>0.3 :
                if r == 'titanium' or r=='zirconia':
                    self.abtmaterial =  r
        return True
        #            self.abtmaterial[0] = r
        #        if asInt( val ):
        #            n = int( asInt(val) )
        #            if 0<n and n<33 :
        #                self.abtmaterial[0] = r
        #                self.abtmaterial[n] = r
        #x = 2     
     
    def updateHi(self):
        h = self.getNode('hi')
        if h.GOF>=0.5:
            return True
        else:
            return None
    
    def updateAccount(self):
        a = self.getNode('account')
        if a.GOF>0.5:
            return True
        else:
            return None   

    def updateAbout(self):
        a = self.getNode('about')
        if a.GOF>0.5:
            return True
        else:
            return None   
             
    def updateProductInfo(self):
        p = self.getNode('productinfo')
        if p.GOF>0.5:
            return True
        else:
            return None        
                         
    def updateYesNo(self):
        yn = self.getNode('yesno')
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
            # clear the pending flag
            self.abutmentsOKPending = False

        return self.abutmentsOK

    def updateInfoRequest(self):
        self.inforesponse = ''
        if self.getNode('hi').GOF >= 0.5:
            self.inforesponse = "Hi, hello, good morning."
            return True

        node = self.getNode('about')
        if node.GOF>0.6:
            T = Thing( node.lastConst() )  
            if len(T)==0:
                self.inforesponse = "Please give me a little more information." 
            elif T=='how':
                self.inforesponse = "Good, thank you. I finally got my mood swings under control."
            else:
                self.inforesponse = "I am Naomibot, hoping to help you order a custom abutment.\
                \nDo you want abutments or other products?"
            return True

        node = self.getNode('orderinfo')
        if node.GOF>0.6:
            self.inforesponse = "Do you have a case number I can reference?"
            self.inforesponse += "\n[UNDER CONSTUCTION HERE]"
            return True

        node = self.getNode('productinfo')
        val = Value(node.lastConst())
        if node.GOF>0.6:
            self.inforesponse = "[HERE SUMMARY about " +val + "].\n[HERE LINK]\n[HERE recommend]"
            return True
     
        node = self.getNode('account') 
        if node.GOF>0.6:
            self.inforesponse = "For questions about your account please call Customer Service at 1-844-848-0137" 
            return True
        
        node = self.getNode('askmaterial')
        if node.GOF > 0.6:
            self.inforesponse =  "[Ti versus Zr: HERE SUMMARY, RECOMMEND, LINK]"
            return True

        return False
                
    def updateAll( self ):
        if self.maxGOF==0.0:
            self.updated = False
            return
        #if self.maxGOF==1.0:
        #    self.updated = True
        #    return

        self.updated = False
        if self.updateAbout():
            self.updated = True
        if self.updateHi():
            self.updated = True
        if self.updateAccount():
            self.updated = True
        if self.updateProductInfo():
            self.updated = True
        if self.updateYesNo():
            self.updated = True        
        if self.updateTeeth():
            self.updated = True
        if self.updateAbutments():
            self.updated = True
        if self.updateMaterial():
            self.updated = True
   
    def respondNext( self ):
        if self.updated==False:
            return "I wish I could help with that. My porpoise is to help you make an order\
            \nor help if you have questions about our abutments, crowns, and bridge products. "
        else: # reset for future use 
            self.updated = False

        # deflect questions
        if self.updateInfoRequest():
            return self.inforesponse

        r = ""
        if countBool( self.teeth ) ==0:
            r += "Please enter the tooth numbers"

 #       elif countStr( self.abtmaterial )==0:
        elif len( self.abtmaterial)==0:
            r += "Do you want titanium or zirconia abutments?"

        elif not self.abutmentsOK: #or crownsOK):
            if self.okcount==0: 
                r += "Do you want abutments for those tooth numbers?" # A YESNO
                self.okcount = 1
            else: # (so customer already said "no" once
                r += "OK, let's leave that blank for now, and add crowns etc later\n"
                r += self.simpleOrderString()
                self.okcount = 0
            self.abutmentsOKPending = True

        else:
            r = self.simpleOrderString()
        
        if r=='':
            r = "Oops. My programmers missed the possibility you would say that"

        return r

    def simpleOrderString(self):
        r = ""
        c = countBool(self.teeth)
        if countBool(self.teeth)==1:
            th = "tooth "
        else:
            th = "teeth "
            
        n = countBool( self.teeth )
        mat = self.abtmaterial 
        q = ''  
        if self.crownsOK and self.abutmentsOK:
            q = " abutment/crown"

        r += "So far, I have " + str(n) + q + " unit(s) of " + mat + " on " + th
        for i in range(1,len(self.teeth)):
            if self.teeth[i]:
                r += "#"+str(i) + ", "
        r += "\nShall we continue with your patient data? \nScans, interface IDs, etc?"
        return r

    def getOrder(self):
        order = Order()

        # get the abutments
        mat = self.abtmaterial 
        if self.abutmentsOK and countBool( self.teeth )>0:
            for i in range(0,33):
                if self.teeth[i]:
                    abutment = Abutment()
                    abutment.material = mat
                    abutment.tooth_number = i
                    order.abutments.append( abutment )
        
        # transfer referece

        # transfer scanner name

        return order
        


class Abutment(object):
    def __init__(self):
        self.tooth_number = 0 # 1-32
        self.material = ''# "Titanium" # Ti or Zr

class Order(object):
    def __init__(self):
        self.reference = "" # user-entered order identifier
        self.scanner = "" # the scanner being used in the lab -- 3SHAPE etc.
        self.tooth_numbering_system = "US" # US, FDI

        self.abutments = [] # abutment objects
 
                    