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
        sepf.pressure = other.pressure

class AbutmentData:
    def __init__(self):
        self.base = AbutmentBase()
    def __eq(self, other): 
        other.base = self.base
