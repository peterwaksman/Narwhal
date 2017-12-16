import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *


class EmergenceProfile:
    def __init__(self):
        self.value = "off" # also known as a straight emergence profile
                           # will use name of EPSTYPE VAR
    def __eq__(self, other):
        self.value = other.value

class TissuePressure():
    def __init__(self):
        self.value = 0.0 # positive value means TOWARDS/INTO the tissue
    def __eq__(self, other):
        self.value = other.value

class AbutmentBase:
    def __init__(self):
        self.eps = EmergenceProfile()    
        self.pressure = TissuePressure()
    def __eq__(self, other):
        self.eps = other.eps
        self.pressure = other.pressure

#---------------------------------------
class MarginSpec:
    def __init__(self):
        self.relation = 'low' # name of dictionary containing "sub"
        self.reffeature = 'gum' # name of dictionary containing "gingiva"
        self.value = 0.2       # or customer's preferred default, eg "margins subgingival"

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
        self.tooth = 0 # even if redundant, keep this here

    def __eq__(self, other):
        self.M = other.M 
        self.D = other.D 
        self.F = other.F 
        self.L = other.L 
        self.tooth = other.tooth

#---------------------
class AbutmentData:
    def __init__(self):
        self.base = AbutmentBase()
        self.margin = MarginData()
    def __eq(self, other): 
        self.base = other.base
        self.margin = other.margin
