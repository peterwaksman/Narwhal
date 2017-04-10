#!/usr/bin/env python
"""Basic example.

Shows how to construct narratives and apply them to a sentence. The lower case 
letters ((a),(b), etc.) refer to notes at the end of this file. Here the prefix
"k" means list of keywords.

This example uses this narrative tree:

        EXPERIENCE(kEXPERIENCE)
            FOOD("foodIlike, foodIhate")
                POSFOOD(kPOSFOOD))
                NEGFOOD(kNEGFOOD))
            AFFECT()
                SAD(kSAD) | HAPPY(kHAPPY)
            EAT(kEAT)

(a) That is preferable to this tree: 

        EXPERIENCE(kEXPERIENCE)
            FOOD(kPOSFOOD + kNEGFOOD)
            AFFECT()
                SAD(kSAD)| HAPPY(kHAPPY)
            EAT(kEAT)
 
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

# (e) for testing the tree:
#tokens = nwu.TOKS('cilantro makes me sad')
#EXPERIENCE.findInText2(tokens, 0)    
#segment = nws.PrepareSegment(EXPERIENCE, tokens)


#####################################################
#              NARs narratives formulas in the VARs
#####################################################

foodaffect = nwt.cause(FOOD, AFFECT) # "What I eat affects how I feel"

eating = nwt.event(SELF,FOOD,EAT)  #we ate food

#(e) for testing the nar:
#nws.ReadSegment(foodaffect,segment)
#print foodaffect.str()


#####################################################
#              NWApp - the application object
#####################################################

# Prepare initializers - line up arrays, to ensure same number of elements
nars       = [foodaffect,eating]
calibs     = [False,False] # (f) no calib needed, polarities are correctly arranged
thresholds = [0.6,0.6]   # (g) slightly higher than 0.5

#nars       = [eating]
#calibs     = [False] # (f) no calib needed, polarities are correctly arranged
#thresholds = [0.6]   # (g) slightly higher than 0.5



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

(a) Since conceptually Cheese is "good" and Cilantro is "bad", it is better 
to make a good/bad distinction in the arrangement of these VARs in the 
tree - separately from the good bad affect. If they are grouped (as in the second 
tree format) then sentences lacking the additional "affect" values remain neutral, 
which reduces the scope of understanding.


(b) 'hamburger,' and 'hamburger ,' have different matching behavior. The
former matches "hamburger" or "hamburgers". The second only matches "hamburger"


(c) Narwhal handles a number of "logical connectors" such as 'not' and 'and'. 
It also handles punctuations. These are in nwcontrol.py. So the client does not 
need to. Actually it can backfire if you try something like
    kHAPPY = 'gleeful,not $ happy'

Because this matches "I was happy" but does not match "I was not happy". You 
would need to put 'not happy' into the list for kSAD in order to understand 
the second sentence. Let Narwhal take care of that.


(d) Narwhal can interpret good/bad value statements. These values are encoded
at the lowest level in VARs, in definitions of the form 
            V = V1 | V2. 
A VAR defined this was is called "exclusive". 
  
By convention V1 is considered 'good' and V2 as 'bad'. If you set it up 
backwards, it can be corrected later with calibrations. But a well designed    
VAR tree encodes the 'good' as the first of two alternatives. For reference 
good/bad handling is done with the "polarity" member variable in the Narwhal 
classes.


(e) If you comment-in this code and examine the EXPERIENCE variable before and
after, it shows how the tokens are being prcessed. This can help in designing 
a tree or just to see how the code works. 
    Continuing: you can examine the process of building a segement, where
most of the work happens, then step into the ReadSegment( ) code to see the
reading "inner loop". 
    Finally the eating.str() shows the form of the 'eating' narrative, with
asterisks marking slots whose VARs were found in the read operation.


(f) The "calibration" is simply a way of sticking a minus sign in the front
of the final result. It is a fudge factor but often masks problems with
tree design or bugs in Narhwal.


(g) The "threshold" is a lower limit on the goodness-of-fit ("gof") score 
between the nar and the input text. A score of 0.5 is possible with 
only one out of two words matching. Setting the threshold slightly higher 
at 0.6 means that will not be considered as "something read".
"""