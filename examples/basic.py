#!/usr/bin/env python
"""Basic example.

Keywords exist in a tree, not a flat structure. The example below shows
how to define a topic-specific tree and how to define "narrative"
relationships between the nodes of the tree. Once defined, this tree and the
relationships initialize an application object that can read arbitrary 
sentences. The output is a sequence of values in [-1,1]. With negative
values being "bad" and positive values being "good".

The example is about liking cheese and disliking cilantro and it uses a tree 
of topic keywords arranged like this:

        EXPERIENCE(kEXPERIENCE)
            FOOD("foodIlike, foodIhate")
                POSFOOD(kPOSFOOD))
                NEGFOOD(kNEGFOOD))
            AFFECT()
                SAD(kSAD) | HAPPY(kHAPPY)
            EAT(kEAT)

That is preferable to the tree: 

        EXPERIENCE(kEXPERIENCE)
            FOOD(kPOSFOOD + kNEGFOOD)
            AFFECT()
                SAD(kSAD)| HAPPY(kHAPPY)
            EAT(kEAT)
 
Since cheese is "good" and cilantro is "bad", it is better to make 
a good/bad distinction in the arrangement of these VARs in the tree - 
separately from the good bad arrangement of AFFECT. If they are 
grouped (as in the second tree format) then sentences lacking the 
additional "affect" values remain neutral, which reduces the flexibility.

For more details, please see end notes indicated by lower case letters 
like #(b), #(c), etc.

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

 
# VAR tree --------------------------------------
#(b)

kPOSFOOD = 'cheese, hamburger' 
POSFOOD = nwt.KList( "foodIlike", kPOSFOOD).var()
kNEGFOOD = 'cilantro,old fish'
NEGFOOD = nwt.KList("foodIhate", kNEGFOOD).var()
FOOD = POSFOOD | NEGFOOD


kSAD = 'sad,unhappy,angry,sick'
SAD = nwt.KList('sad', kSAD).var()

#(c) 
kHAPPY = 'gleeful, happy'
HAPPY = nwt.KList('happy', kHAPPY).var()

#(d) 
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


# NARs: formulas in the VARs --------------

foodaffect = nwt.cause(FOOD, AFFECT) # "What I eat affects how I feel"
eating = nwt.event(SELF,FOOD,EAT)    # "we ate food"



# NWApp: the application object ---------------
# (e),(f)

nars       = [foodaffect,eating]
calibs     = [False,False]  
thresholds = [0.6,0.6]    


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

(b) No trailing 's' on hamburger : 'hamburger,' and 'hamburger ,' have different
matching behavior. The former matches "hamburger" or "hamburgers". The second 
only matches "hamburger"


(c) Narwhal handles a number of "logical connectors" such as 'not' and 'and'. 
It also handles punctuations. These are in nwcontrol.py. So the client does not 
need to. Actually it can backfire if you try something like
    kHAPPY = 'gleeful,not $ happy'

Because this matches "I was happy" but does not match "I was not happy". You 
would need to put 'not happy' into the list for kSAD in order to understand 
the second sentence. Let Narwhal take care of that.


(d) Use "AFFECT = HAPPY | SAD" instead of "AFFECT = SAD | HAPPY"
Narwhal can interpret good/bad value statements. These values are encoded
at the lowest level in VARs, called "exclusive VARs", defined in this form 
            V = V1 | V2. 
It is better to put positives before negatives
  
By convention V1 is considered 'good' and V2 as 'bad'. If you set it up 
backwards, it can be corrected later with calibrations. But a well designed    
VAR tree encodes the 'good' as the first of two alternatives. For reference 
good/bad handling is done with the "polarity" member variable in the Narwhal 
classes.

(e) If you insert this code and examine the EXPERIENCE variable before and
after, it shows how the tokens are being prcessed. This can help in designing 
a tree or just to see how the code works. 

    tokens = nwu.TOKS('cilantro makes me sad')
    EXPERIENCE.findInText2(tokens, 0)    
    segment = nws.PrepareSegment(EXPERIENCE, tokens)

Also, you can examine the process of building a segement, where
most of the work happens, then step into the ReadSegment( ) code to see the
reading "inner loop". Finally the eating.str() shows the form of the 
'eating' narrative, with asterisks marking slots whose VARs were found 
in the read operation.

    nws.ReadSegment(foodaffect,segment)
    print foodaffect.str()
 

(f) The "calibration" is simply a way of sticking a minus sign in the front
of the final result. It is a fudge factor but often masks problems with
tree design or bugs in Narhwal.

Thresholds are applied only at the level of final reporting, so the initializing
values have little affect on actualy processing. Generally a "threshold" 
is a lower limit on the goodness-of-fit ("gof") score between the nar and 
the input text. A score of 0.5 is possible with only one out of two words
matching. Setting the threshold slightly higher at 0.6 means that will 
not be considered as "something read". 

"""