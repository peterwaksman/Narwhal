import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *

from abtSketch2 import AbutmentSketch

class EmergenceProfile:
    def __init__(self):
        self.value = '' # also known as a straight emergence profile
                           # will use name of EPSTYPE VAR
    def __eq__(self, other):
        self.value = other.value

    def hasData(self):
        if self.value:
            return True
        else:
            return False

class TissuePressure():
    def __init__(self):
        self.value = None # positive value means TOWARDS/INTO the tissue
    def __eq__(self, other):
        self.value = other.value
    def hasData(self):
        if self.value:
            return True
        else:
            return False
class AbutmentBase:
    def __init__(self):
        self.eps = EmergenceProfile()    
        self.pressure = TissuePressure()
    def __eq__(self, other):
        self.eps = other.eps
        self.pressure = other.pressure
    def hasData(self):
        if self.eps.hasData() or self.pressure.hasData():
            return True
        else:
            return False
#---------------------------------------
class MarginSpec:
    def __init__(self, relation='', reffeature = '', value=0.0 ):
        self.relation = relation  
        self.reffeature = reffeature  
        self.value = value    

    def hasData(self):
        if self.relation or self.reffeature:
            return True
        else:
            return False

    def __eq__(self, other):
        self.relation = other.relation
        self.reffeature = other.reffeature
        self.value = other.value 

class MarginData:
    def __init__(self):
        self.M = MarginSpec()
        self.D = MarginSpec()
        self.F = MarginSpec()
        self.L = MarginSpec()

    def hasData(self):
        if self.M.hasData() or self.D.hasData() or self.F.hasData() or self.L.hasData():
            return True
        else:
            return False

    def __eq__(self, other):
        self.M = other.M 
        self.D = other.D 
        self.F = other.F 
        self.L = other.L 
 
#---------------------
class AllAbutments:
    def __init__(self):
        self.base = []
        self.margin = []
        for tooth in range(0, 33):
            self.base.append(AbutmentBase())
            self.margin.append(MarginData())

    def __eq__(self, other): 
        for tooth in range(0, 33):
            self.base[tooth] = other.base[tooth]
            self.margin[tooth] = other.margin[tooth]
 
class ToothSites:
    def __init__(self):
        self.abutments = AllAbutments()
 
       # later...dude
    def updateSketch(self, abtSketch):
        # decide about redrawing cuz a margin spec
        toothno = -1
        for n in range(0, 33):
            if self.abutments.margin[n].hasData() or self.abutments.base[n].hasData():
                toothno = n
                break

        if toothno<0 :
            return
        
        margin = self.abutments.margin[toothno]
        base = self.abutments.base[toothno]
        if base.hasData():
            if base.eps.hasData():
                x = base.eps.value
                if x=='convex':
                    abtSketch.makeConvex()
                elif x=='off':
                    abtSketch.makeStraight()
                elif x=='concave':
                    abtSketch.makeConcave()
                elif x=='ankylos':
                    abtSketch.makeAnkylos()
            # tissue pressure not sketched 
        if margin.hasData():
            M = margin.M
            D = margin.D
            F = margin.F
            L = margin.L
            if M.relation=='below' or D.relation=='below' or \
               F.relation=='below' or L.relation=='below':
                abtSketch.makeSubG()
            elif M.relation=='above' or D.relation=='above' or \
               F.relation=='above' or L.relation=='above':
                abtSketch.makeSupraG()




                
       

