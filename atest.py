
from nwtypes import *
from NoiseTree import *
#from nwread import *
from nwutils import *
#from nwreader import *
from nwread import *


n = attribute( PROBLEM, SOUND )



n = attribute( BARRIER, STATE)
m = event( BARRIER, NOISE, LETINOUT )
m2 = event( n, NOISE, LETINOUT )



# "open windows let in the noise"
# "the walls were thin and noise carries"


text = "windows shut out the noise"
#text = "I had no problem with noise but I could see the potential for issues given the wrong neighbors, so bring earplugs. I will definitely return"
#text = "we stayed in the block farthest from the road and we heard nothing at all"
#text = "There was toilet paper all over the floor and overflowing trash every day."
#text = "the hotel was far from the border and near to town"
 
NoiseText = "We did find it a bit noisy with the balcony doors open due "
NoiseText += "to the McDonalds next door - especially late at night and at 6 am "
NoiseText += "when the deliveries started arriving."

E = EXPERIENCE

r = attribute( LOC, SOURCE, PROX )

#A = NWReader(E,r)
#A.readText("The hotel was near the border and far from downtown")
 

s = attribute( SOUND, INTENSITY )
c = sequence(r,s)
#c = cause(r,s)

text = "The hotel was over a bar and that was noisy"
#text = "The hotel was near the border and far from downtown"
#text = NoiseText
tokens = TOKS(text)
ifound = []
x = ReadText(c,tokens,ifound)

ifound = cleanFound(ifound)
R = NarRecord(c, ifound, tokens)

c.clear()

C = NWReader(E,c)
C.readText(text)
#C.readText(NoiseText)

x=2