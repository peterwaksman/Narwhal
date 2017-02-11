
#--------- some core includes
from nwtypes import *
from nwutils import *
from nwread import *
from nwcontrol import *
from nwsreader import *
print("\n\n")

# an original sample I wanted to handle
NoiseText = "We did find it a bit noisy with the balcony doors open due "
NoiseText += "to the McDonalds next door - especially late at night and at 6 am "
NoiseText += "when the deliveries started arriving." 

#ReadSegment(letin, segment)
#G = gof(segment, letin, 0, len(text))
#x = 2
#E.clearImplicits()

#--------- app specific
from NoiseTree import *
E = EXPERIENCE

letin = event( BARRIER, SOUND, LETINOUT )
affect  = cause( attribute(SOUND,[TOD]), AFFECT )
proximity = attribute( LOC, SOURCE, PROX)    

text = "word spoken was heard through the walls"
#text = "the maiden let in the noise"
#segment = prepareSegment( E, text)
#s = showSEG(segment, text)
#print(s)



text = NoiseText
text = "My room was far from the elevator and far from the lobby, so it was very quiet."


#ab = NWReader(E,[proximity])
#ab.readText(text)
#print ab.report()

nw = NWSReader(E, [proximity] )
nw.readText(text)
s = nw.report(text)
print s
x = 2
 



