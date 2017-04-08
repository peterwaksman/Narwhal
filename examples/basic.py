#!/usr/bin/env python
"""Basic example.

Shows how to construct narrative attributes and apply them to a sentence.

This example uses the narrative tree:

EXPERIENCE(KW_EXP)
    FOOD(KW_FOOD)
    AFFECT()
        SAD(KW_SAD)
        | HAPPY(KW_HAPPY)


OR
EXPERIENCE(kEXPERIENCE)
    FOOD("foodIlike,foodIhate")
        POSFOOD(kPOSFOOD))
        NEGFOOD(kNEGFOOD))
    AFFECT()
        SAD(kSAD) | HAPPY(kHAPPY)

"""
import os
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal import nwtypes as nwt
from narwhal import nwapp as nwa
from narwhal import nwutils as nwu
from narwhal import nwsegment as nws

# TODO - revisit whether to use one "food" category or to split into good and 
# bad food.
#kFOOD = 'cheese,cilantro'
#FOOD = nwt.KList('food', kFOOD).var()

# ---------------VAR TREE
kPOSFOOD = 'cheese, hamburger' #NB no traing 's' on hambrugers, OK cuz of termination  
POSFOOD = nwt.KList( "foodIlike", kPOSFOOD).var()
kNEGFOOD = 'cilantro,old fish'
NEGFOOD = nwt.KList("foodIhate", kNEGFOOD).var()
FOOD = POSFOOD | NEGFOOD

kSAD = 'sad,unhappy,angry,sick'
SAD = nwt.KList('sad', kSAD).var()

# Avoid this: "not" is an internally handled logic operator.
#kHAPPY = 'gleeful,not $ happy'   
kHAPPY = 'gleeful, happy'
HAPPY = nwt.KList('happy', kHAPPY).var()

#Avoid this: one wants to put positives before negatives
#AFFECT = SAD | HAPPY 
AFFECT = HAPPY | SAD

kEXPERIENCE = 'experience,we found,I found,we did find'
EXPERIENCE = nwt.KList('experience', kEXPERIENCE).var()
EXPERIENCE.sub(FOOD)
EXPERIENCE.sub(AFFECT)

# NARS
eating = nwt.cause(FOOD, AFFECT)
n = eating.numSlots()
#for testing
tokens = nwu.TOKS('cilantro makes me sad')
# 
#EXPERIENCE.findInText2(tokens, 0)    
#
segment = nws.prepareSegment(EXPERIENCE, tokens)
nws.ReadSegment(eating,segment)

# for now, lining up these arrays helps ensure same number of elements
nars       = [eating]
calibs     = [False] # no calib, because polarities are correctly arranged
thresholds = [0.6]

foodApp = nwa.NWApp(EXPERIENCE, nars, calibs, thresholds)

SENTENCES = [
    'Cilantro makes me sad.',
    'Cheese makes me happy.',
]


def main():
    """Run the model against some sentences."""
    for sentence in SENTENCES:
        print('Sentence: ' + sentence)
        foodApp.readText(sentence)
        report = foodApp.report(sentence)
        print(report)


if __name__ == '__main__':
    main()
