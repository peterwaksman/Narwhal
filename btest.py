
#--------- some core includes
from nwtypes import *
from nwutils import *
from nwread import *
from nwcontrol import *
from nwsreader import *
from nwapp import *
from nwobject import *

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


problem = attribute( PROBLEM, SOUND )
sound = attribute( attribute( attribute(SOUND, SOURCE), INTENSITY), TOD)
affect  = cause( attribute(SOUND,[TOD]), AFFECT )
proximity = attribute( LOC, SOURCE, PROX)        
letin = event( attribute(BARRIER,[STATE]), SOUND, LETINOUT )


text = "word spoken was heard through the walls"
#text = "the maiden let in the noise"
#segment = prepareSegment( E, text)
#s = showSEG(segment, text)
#print(s)



text = NoiseText
text = "My room was far from the elevator and far from the lobby, so it was very quiet."
text = "Although my room was next to the elevator, it was perfectly quiet and dark at night so I was able to sleep much better than most European cities"
text = "it was perfectly quiet and dark at night "
text = "We did find it a bit noisy with the balcony doors open due to the McDonalds next door."
 

ab = NWReader(E,[proximity])
ab.readText(text)
print ab.report()

nw = NWSReader(E, [proximity] )
nw.readText(text)
s = nw.report(text)
print s
x = 2
 
#nars      = [ problem, sound, affect, proximity, letin]
#calibs    = [ True,    True,  True,   True,      True ]     
#thresholds= [ 0.6,     0.6,   0.6,    0.6,  0.6       ]


#nwo = NWObject(E, nars, calibs, thresholds)
#nwo.readText(text)
#s = nwo.report()
#print s
 
#nwa = NWApp(E, nars, calibs, thresholds)
#nwa.readText(text)
#s =  nwa.report(text)
#print s
#x = 2

