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
from stdtrees.quantities import FLOATx


GEN_GEOMETRY= KList("geometry", "geometry").var()


#-----------------
DIRECTION= KList( "direction", "direction").var()

# values duplicated in LO_HI
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
FLAT= KList("flat", "flat").var()
SURFACEFEEL = KList("surfacefeel", "").var()
SURFACEFEEL.sub(SMOOTH)
SURFACEFEEL.sub(SHARP)
SURFACEFEEL.sub(FLAT)
 

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
RECT= KList( "rect", "rect").var()
CIRC= KList( "circ","circ, round ").var()
OVAL= KList( "oval", "oval, egg").var()
SHAPE.sub(RECT)
SHAPE.sub(CIRC)
SHAPE.sub(OVAL)
#------------------------

RELATION= KList("relation", "relation, relative to").var()
#AMOUNT= KList("amount", "amount, quantity").var()
AT = KList("at"," at, flush, even with, match, noimpingment, level, even , keep ").var()
CLOSEST= KList("just", "just, close, close to, closest, slightly , as close as possible").var()
BETWEEN= KList( "between", "between, mid ").var()

HI= KList("above",  " positive, pos , hi , high,  raise, move * up, above, over, sup, supra, supra-, supra_, \
          super, super-, super_, positive, up, hi as possible, high as possible, up ").var()
LO= KList("below",  " negative, neg , lo , low, deep, lower, drop, move * down, below, sub, sub-, sub_, under, \
          depth , down , lo as possible, low as possible, down ").var()
NEAR= KList("near",  "near, near to").var()
FAR= KList( "far", "far, far from, away, out, away from, out from").var()


RELATION.sub(AT)
RELATION.sub(CLOSEST)
RELATION.sub(BETWEEN)
#RELATION.sub(OFFSET)
#RELATION.sub(MATCH)
RELATION.sub(HI)
RELATION.sub(LO)
RELATION.sub(NEAR)
RELATION.sub(FAR)

# offset is too neutral to consider as a "relation", use it explicitly
# if you want that much generality (see CLEARANCE for abutment core)
OFFSET = KList( "offset", "offset, distance, clearance, clearance, clerance, \
                clearence, room, space , reduction, from ").var()

PARALLEL= KList("parallel",  "para, parra, pare, parre, splint").var()
MATCH= KList("match", "match, follow, according" ).var()
MATCH.sub(PARALLEL) #parallel is a kind of matching
#----------------------------------
JUST = KList("just", "just, slightly ").var()
ASPOSS = KList("possible", "possible, as possible, as * as possible, as much as possible, if possible").var()
RELAMOUNT = KList("relamount", "amount").var()
RELAMOUNT.sub(JUST)
RELAMOUNT.sub(ASPOSS)
RELAMOUNT.sub(FLOATx)


#-----------------------------------

LIKE = KList("like","like, similar, same as, equivalent").var()
TYPE = KList("type", "type, category, kind").var()

#------------------------

GEN_GEOMETRY.sub(DIRECTION)
GEN_GEOMETRY.sub(DIMENSION)
GEN_GEOMETRY.sub(POSITION)
GEN_GEOMETRY.sub(SHAPE)
GEN_GEOMETRY.sub(RELATION)


