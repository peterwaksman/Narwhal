import os 
import sys

# Add local narwhal to the module path
this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)

from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *  
from stdtrees.ask import *  


####################### THINGS ###########################
BALL = KList( "ball", "ball").var()
SCALE = KList("scale", "scale, rule").var()
THING = KList( "thing" , "thing, object" ).var()
THING.sub(BALL)
THING.sub(SCALE)

######################## DIMENSIONS #####################
RED = KList("red", "red").var() #shorthand
GREEN = KList("green","green").var()
COLOR = KList("color", "color").var()
COLOR.sub(RED)
COLOR.sub(GREEN) 

kLARGE = "big, large"
LARGE = KList("big", "big, large").var()
SMALL = KList("small", "small, normal").var()
SIZE = SMALL | LARGE #make negatives of each other

RIGHTDIR = KList("right","right, to the right").var()
LEFTDIR = KList("left", "left, to the left").var()
DIRECTION = RIGHTDIR|LEFTDIR


kDIMENSION = "dimension, attribute, property"
DIMENSION = KList("dimension", kDIMENSION).var()
DIMENSION.sub(COLOR) # modifiers of ball
DIMENSION.sub(SIZE)

DIMENSION.sub(DIRECTION) # modifiers of movement

####################### ACTIONS ##############################
SHOW = KList("show", "show").var()
HIDE = KList("hide", "hide, get rid of").var()
DISPLAY = SHOW | HIDE

ZOOMIN = KList("zoomin","zoom in, go in, magnify").var()  
ZOOMOUT = KList("zoomout","zoom out, go out, shrink").var()  
ZOOM = ZOOMIN | ZOOMOUT

MAKE = KList("make", "make, make it, turn, turn it").var()

MOVE = KList("move", "move").var()


kACTION = "do, act"
ACTION = KList("action", kACTION).var()
ACTION.sub(DISPLAY)
ACTION.sub(ZOOM)
ACTION.sub(MAKE)
ACTION.sub(MOVE)


BOUNCYSAYS = KList("bouncysays", "bouncy").var()
BOUNCYSAYS.sub(ACTION)
BOUNCYSAYS.sub(THING)
BOUNCYSAYS.sub(DIMENSION)

doAction = event( THING, [DIMENSION], ACTION)

R = [ NWTopicReader("bouncyreader", BOUNCYSAYS, doAction ) ]

BouncyTopic = NWTopic( BOUNCYSAYS, R ) 






