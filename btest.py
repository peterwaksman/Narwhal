
#--------- some core includes
from nwtypes import *
from nwutils import *
from nwread import *
from nwcontrol import *
from nwsegment import *


#--------- app specific
from NoiseTree import *
E = EXPERIENCE

letin = event( BARRIER, SOUND, LETINOUT )

text = "word spoken was heard through the walls"
text = "the hotel was far from the border and near to town"
segment = prepareSegment( E, text)
s = showSEG(segment)
print(s)

x = 0

#ReadSegment(letin, segment)
#G = gof(segment, letin, 0, len(text))
#x = 2
E.clearImplicits()
ab = ABReader(E,letin)
ab.readText(text)

N = NWSReader(E, [letin] )
N.readText(text)
x = 2




