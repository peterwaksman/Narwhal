from nwtypes import *
from nwread import *
from nwobject import *

# app specific
from NoiseTree import *

# here we structure the output variables as desired. Pick a prefix like "N_"
# and put a polarity field in each one. The total polarity is a formula you, the
# client, must write below in the N_Summary class
# Each NAR corresponds with an intermediate sub-structure of the final data

# problem_/noise
problem = attribute( PROBLEM, NOISE )

# sound_/intensity_/source_/timeOfDay ::[me_/affect]
sound = attribute( attribute( attribute(SOUND, INTENSITY), SOURCE), TOD)

#[sound->me] :: me_/affect
affect  = cause( attribute(NOISE,TOD), AFFECT )

#location _nearfar_/ source
proximity = attribute( LOC, SOURCE, PROX)        


# (barrier_/state)-letInOut->sound
letin = event( attribute(BARRIER,STATE), NOISE, LETINOUT )


class NoiseApp:
    def __init__(self):
        nars      = [ problem, sound, affect, proximity, letin]
        calibs    = [ True,    True,  True,   True,      True ]     
        thresholds= [ 0.6,     0.6,   0.6,    0.6,  0.6       ]
 
        self.object = NWObject(EXPERIENCE, nars, calibs, thresholds) 

    def run(self):
        text = ""
        while 1:
            text = input('Enter text: ')
            self.object.readText(text)
            h = self.object.report()
            print(h)
            print( self.object.printFinal())
