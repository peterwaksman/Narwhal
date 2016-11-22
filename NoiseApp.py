from nwtypes import *
from nwread import *
# app specific
from NoiseTree import *

# here we structure the output variables as desired. Pick a prefix like "N_"
# and put a polarity field in each one. The total polarity is a formula you, the
# client, must write below in the N_Summary class
# "problem with noise" = attribute(PROBLEM, SOUND)
class N_Problem:
   def __init__(self, true_false):
       self.polarity = true_false

# sound_/intensity_/source_/timeOfDay ::[me_/affect]
class N_Sound:
    def __init__(self, pol, sound, source, intensity, tod):
        asd

#[sound->me] :: me_/affect
class N_Affect:
    def __init__(self, pol, affect, tod):
        self.polarity = pol
        self.affect = affect
        self.tod = tod

#location _nearfar_/ source  
class N_Source:
    def __init(self, pol, loc, src, prox ):
        self.polarity = pol
        self.loc = loc
        self.src = src
        self.prox= prox


# (barrier_/state)-letInOut->sound
class N_Barrier:
    def __init__(self,pol):
        self.polarity = pol

class N_NoiseSummary:
    def __init__(self):
       self.problem = None
       self.sound = None
       self.affect = None
       self.source = None
       self.barrier = None
    def finalPolarity():
        return True

     