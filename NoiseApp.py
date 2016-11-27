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
class ProblemInfo:
   def __init__(self):
       self.str = "PROBLEM"
       self.polarity = True
       self.found = False

   def transferRecord(self, nard, irecord):
        problemT = 0.6
        if irecord< len(nard.V) :
            record = nard.V[irecord]
        else:
            return

        if record==None:
            return

        if record.GOF>problemT :
            self.found = True
            self.polarity = finalPolarity()
            



# sound_/intensity_/source_/timeOfDay ::[me_/affect]
sound = attribute( attribute( attribute(SOUND, INTENSITY), SOURCE), TOD)
class SoundInfo:
    def __init__(self, pol, sound, source, intensity, tod):
        asd


#[sound->me] :: me_/affect
affect  = cause( attribute(NOISE,TOD), AFFECT )
class AffectInfo:
    def __init__(self, pol, affect, tod):
        self.polarity = pol
        self.affect = affect
        self.tod = tod

#location _nearfar_/ source
proximity = attribute( LOC, SOURCE, PROX)        
class SourceInfo:
    def __init(self, pol, loc, src, prox ):
        self.polarity = pol
        self.loc = loc
        self.src = src
        self.prox= prox


# (barrier_/state)-letInOut->sound
letin = event( attribute(BARRIER,STATE), NOISE, LETINOUT )
class BarrierInfo:
    def __init__(self,pol):
        self.polarity = pol

# this is the whole package of a noise statement
class NoiseInfoSummary:
    def __init__(self):
       self.problem = None
       self.sound = None
       self.affect = None
       self.proximity = None
       self.letin = None
    def finalPolarity():
        return True

class NoiseApp:
    nars      = [ problem, sound, affect, proximity, keepout ]
    calibs    = [ True,    True,  True,   True,      True ]     
    thresholds= [ 0.6,     0.6,   0.6,    0.6,  0.6       ]

    object = NWObject(EXPERIENCE, nars, calibs, thresholds) 

