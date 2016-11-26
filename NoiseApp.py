from nwtypes import *
from nwread import *
# app specific
from NoiseTree import *

# here we structure the output variables as desired. Pick a prefix like "N_"
# and put a polarity field in each one. The total polarity is a formula you, the
# client, must write below in the N_Summary class
# Each NAR corresponds with an intermediate sub-structure of the final data

# problem_/noise
problem = attribute( PROBLEM, NOISE )
class N_Problem:
   def __init__(self, true_false):
       self.polarity = true_false



# sound_/intensity_/source_/timeOfDay ::[me_/affect]
sound = attribute( attribute( attribute(SOUND, INTENSITY), SOURCE), TOD)
class N_Sound:
    def __init__(self, pol, sound, source, intensity, tod):
        asd


#[sound->me] :: me_/affect
affect  = cause( attribute(NOISE,TOD), AFFECT )
class N_Affect:
    def __init__(self, pol, affect, tod):
        self.polarity = pol
        self.affect = affect
        self.tod = tod

#location _nearfar_/ source
proximity = attribute( LOC, SOURCE, PROX)        
class N_Source:
    def __init(self, pol, loc, src, prox ):
        self.polarity = pol
        self.loc = loc
        self.src = src
        self.prox= prox


# (barrier_/state)-letInOut->sound
letin = event( attribute(BARRIER,STATE), NOISE, LETINOUT )
class N_Barrier:
    def __init__(self,pol):
        self.polarity = pol

# this is the whole package of a noise statement
class N_NoiseSummary:
    def __init__(self):
       self.problem = None
       self.sound = None
       self.affect = None
       self.proximity = None
       self.letin = None
    def finalPolarity():
        return True

class NoiseReader:
    nars = [ problem, sound, affect, proximity, keepout ] 
    # all have negative interpetations
    calibs=[ True,    True,  True,   True,   True ]     
   
    def __init__(self ):
        self.reader = NWReader(EXPERIENCE, nars)
        self.reader.setCalibration(calibs)
    
    def readText(self, text ):
        self.reader.clearAll()
        self.reader.readText( text)
                
