#!/usr/bin/env python
"""Basic example.

Shows how to construct narrative attributes and apply them to a sentence.

This example uses the narrative tree:

EXPERIENCE(KW_EXP)
    FOOD(KW_FOOD)
    AFFECT()
        SAD(KW_SAD)
        | HAPPY(KW_HAPPY)
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

KW_FOOD = 'cheese,cilantro'
VAR_FOOD = nwt.KList('food', KW_FOOD).var()

KW_SAD = 'sad,unhappy,angry'
KW_HAPPY = 'gleeful,not $ happy'
VAR_SAD = nwt.KList('sad', KW_SAD).var()
VAR_HAPPY = nwt.KList('happy', KW_HAPPY).var()
VAR_AFFECT = VAR_SAD | VAR_HAPPY

KW_EXPERIENCE = 'experience,we found,I found,we did find'
VAR_EXPERIENCE = nwt.KList('experience', KW_EXPERIENCE).var()
VAR_EXPERIENCE.sub(VAR_FOOD)
VAR_EXPERIENCE.sub(VAR_AFFECT)

NAR_EATING = nwt.cause(VAR_FOOD, VAR_AFFECT)

NARS = [NAR_EATING]
CALIBS = [True]
THRESHOLDS = [0.6]

APP_FOOD = nwa.NWApp(VAR_EXPERIENCE, NARS, CALIBS, THRESHOLDS)

SENTENCES = [
    'Cheese makes me happy.',
    'Cilantro makes me sad.',
]


def main():
    """Run the model against some sentences."""
    for sentence in SENTENCES:
        print('Sentence: ' + sentence)
        APP_FOOD.readText(sentence)
        report = APP_FOOD.report(sentence)
        print(report)


if __name__ == '__main__':
    main()
