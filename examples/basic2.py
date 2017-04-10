#!/usr/bin/env python
"""Basic2 elaborates onBasic with other topics

The tree is extended to

        EXPERIENCE(kEXPERIENCE)
            FOOD("foodIlike, foodIhate")
                POSFOOD(kPOSFOOD))
                NEGFOOD(kNEGFOOD))
            AFFECT()
                SAD(kSAD) | HAPPY(kHAPPY)
            EAT(kEAT)
            VALUE()
                GOOD(kGOOD) | BAD(kBAD)

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

##############################################
#              VAR TREE 
##############################################

#(a)
#kFOOD = 'cheese,cilantro'
#FOOD = nwt.KList('food', kFOOD).var()

kPOSFOOD = 'cheese, hamburger' #(b) No trailing 's' on hamburger  
POSFOOD = nwt.KList( "foodIlike", kPOSFOOD).var()
kNEGFOOD = 'cilantro,old fish'
NEGFOOD = nwt.KList("foodIhate", kNEGFOOD).var()
FOOD = POSFOOD | NEGFOOD


kSAD = 'sad,unhappy,angry,sick'
SAD = nwt.KList('sad', kSAD).var()

# (c) "not" is an internally handled logic operator.
#kHAPPY = 'gleeful,not $ happy'   
kHAPPY = 'gleeful, happy'
HAPPY = nwt.KList('happy', kHAPPY).var()

# (d) It is better to put positives before negatives
#AFFECT = SAD | HAPPY 
AFFECT = HAPPY | SAD

kGOOD = "good"
kBAD = "bad"
GOOD = nwt.KList( "positive", kGOOD).var()
BAD = nwt.KList("negative", kBAD).var()
VALUE = GOOD | BAD


kEAT = ' eat,ate,consum,feed'
EAT = nwt.KList('eat',kEAT).var()

kSELF = ' I , we , me , us '
SELF = nwt.KList('self',kSELF).var()

kEXPERIENCE = 'experience,we found,I found,we did find'
EXPERIENCE = nwt.KList('experience', kEXPERIENCE).var()

EXPERIENCE.sub(FOOD)
EXPERIENCE.sub(AFFECT)
EXPERIENCE.sub(EAT)
EXPERIENCE.sub(SELF)
EXPERIENCE.sub(VALUE)

# (e) for testing the tree:
#tokens = nwu.TOKS('cilantro makes me sad')
#EXPERIENCE.findInText2(tokens, 0)    
#segment = nws.PrepareSegment(EXPERIENCE, tokens)


#####################################################
#              NARs narratives formulas in the VARs
#####################################################

foodaffect = nwt.cause(FOOD, AFFECT) # "What I eat affects how I feel"
#foodaffect = nwt.cause( nwt.attribute(FOOD, VALUE), AFFECT) # "What I eat affects how I feel"
#foodaffect = nwt.cause( nwt.attribute(FOOD, [VALUE]), AFFECT) # "What I eat affects how I feel"

eating = nwt.event(SELF, FOOD, EAT)  #we ate food



#####################################################
#              NWApp - the application object
#####################################################

# Prepare initializers - line up arrays, to ensure same number of elements
nars       = [foodaffect,eating]
calibs     = [False,False] # (f) no calib needed, polarities are correctly arranged
thresholds = [0.6,0.6]   # (g) slightly higher than 0.5

#nars       = [foodaffect]
#calibs     = [False]  
#thresholds = [0.6]   



FoodApp = nwa.NWApp(EXPERIENCE, nars, calibs, thresholds)

SENTENCES = [
    'Cilantro makes me sad.',
    'Cheese makes me happy.',
    'We ate good cheese',
    'We ate French cheese with cilantro',
    'We ate French cheese and we ate cilantro',
    'We did not eat Cilantro',
    'Although the place smelled of cilantro, we ate good cheese',
    'The place smelled of cilantro but we ate cheese'
]



def main():
    """Run the model against some sentences."""
    for sentence in SENTENCES:
        print('Sentence: ' + sentence)
        FoodApp.readText(sentence)
        report = FoodApp.report(sentence)
        print(report)


if __name__ == '__main__':
    main()


""" ENDNOTES
"""