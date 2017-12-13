""" geometry.py is a place to define the vocabulary of geometric basics

And anything else you can think of. Grouped as I see fit but you
can re-arrange it or sub divide it if you like.

GEN_GEOMETRY
    DIRECTION
        VERTICAL
        ...
    DIMENSION
        SIZE
        SURFACEFEEL
        ...
    SHAPE
        RECT
        CIRC
        ... 
    POSITION
        CENTER
        SIDE

"""
from narwhal.nwtypes import * #KList, attribute

GEN_GEOMETRY= KList("geometry", "geometry").var()


#-----------------
DIRECTION= KList( "direction", "direction").var()

# values
UP = KList("up", "up").var()
DOWN = KList("down", "down").var()
UP_DOWN = UP|DOWN

VERTICAL= KList("vertical", "vertical, vert").var()
HORIZONTAL = KList( "horizontal", "horizontal, horz").var()
FORWARD= KList("forward", "forward, mesially, towards the front").var()
BACKWARD= KList("backward", "backward, distally, towards the back").var()
ANGLE= KList("angle", "angle, angulation" ).var() # ??overlaps with the verb

DIRECTION.sub(UP_DOWN)
DIRECTION.sub(VERTICAL)
DIRECTION.sub(HORIZONTAL)
DIRECTION.sub(FORWARD)
DIRECTION.sub(BACKWARD)
DIRECTION.sub(ANGLE) #??


#------------------
DIMENSION= KList( "dimension", "dimension, length, lenght").var()
BIG= KList("big", "more, much , large, big, huge, \
    thick, tall, long, wide, witdth , deep, depth, heavy , max, a lot ").var()
SMALL= KList("small", "small, slight, short, tiny , little, light\
    narrow, thin , min, a bit, a little, up to, less").var()
SIZE = BIG|SMALL

STRONG= KList("strong",  "strong, heavy, tight").var()
WEAK= KList("weak",  "weak, light, loose ").var()
STRENGTH = STRONG|WEAK

# and alternative to SIZE and STRENGTH separately
#MORE = KList("more", "").var()
#LESS = KList("less", "").var()
#MORE.sub(BIG)
#MORE.sub(STRONG)
#LESS.sub(SMALL)
#LESS.sub(WEAK)
#MORE_LESS = MORE|LESS 

SMOOTH= KList("smooth", "smooth, round , soft # tissue").var()
SHARP= KList( "sharp", "sharp, sarp").var()
SURFACEFEEL = SMOOTH|SHARP  

DIMENSION.sub(SIZE)
DIMENSION.sub(STRENGTH)
DIMENSION.sub(SURFACEFEEL)

#-------------geometric objects based on scene entities-----------
POSITION = KList("position", "position, pos ").var()
CENTER= KList( "center", "center, midpoint, mid point").var()
SIDE= KList( "side", "side").var()
AXIS = KList("axis", "axes, axial").var()

POSITION.sub(CENTER)
POSITION.sub(SIDE)
POSITION.sub(AXIS)

#-----------------scene entities-------
SHAPE= KList( "shape", "shape").var()
FLAT= KList("flat", "flat").var()
RECT= KList( "rect", "rect").var()
CIRC= KList( "circ","circ, round ").var()
OVAL= KList( "oval", "oval, egg").var()
SHAPE.sub(FLAT)
SHAPE.sub(RECT)
SHAPE.sub(CIRC)
SHAPE.sub(OVAL)
#------------------------
RELATION= KList("relation", "relation, relative to").var()
AMOUNT= KList("amount", "amount, quantity").var()
AT = KList("at"," at, flush, even with, match, noimpingment, level, even ").var()
CLOSEST= KList("just", "just, close, close to, closest, slightly, possible, \
                if possible, as poss, as possible, as much as possible").var()
BETWEEN= KList( "between", "between, mid ").var()
OFFSET = KList( "offset", "offset, distance, clearance, clearance, clerance, \
                clearence, room, space").var()
PARALLEL= KList("parallel",  "para, parra, pare, parre, splint").var()
MATCH= KList("match", "match, follow, according" ).var()
MATCH.sub(PARALLEL) #??? parallel is a kind of matching
HI= KList("hi",  " positive, pos , hi , high,  raise, above, over, sup, supra, supra-, supra_, \
          super, super-, super_, positive, up, hi as possible, high as possible").var()
LO= KList("low",  " negative, neg , lo , low, deep, lower, drop, below, sub, sub-, sub_, under, \
          depth , down , lo as possible, low as possible").var()
HI_LO= HI|LO  

NEAR= KList("near",  "near, near to").var()
FAR= KList( "far", "far, far from, away, out, away from, out from").var()
NEAR_FAR = NEAR|FAR 

RELATION.sub(AMOUNT)
RELATION.sub(AT)
RELATION.sub(CLOSEST)
RELATION.sub(BETWEEN)
RELATION.sub(OFFSET)
#RELATION.sub(PARALLEL) #part of MATCH
RELATION.sub(MATCH)
RELATION.sub(HI_LO)
RELATION.sub(NEAR_FAR)

#------------------------

GEN_GEOMETRY.sub(DIRECTION)
GEN_GEOMETRY.sub(DIMENSION)
GEN_GEOMETRY.sub(POSITION)
GEN_GEOMETRY.sub(SHAPE)
GEN_GEOMETRY.sub(RELATION)


