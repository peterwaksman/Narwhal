
from nwtypes import *
from NoiseTree import *
from nwutils import *
from nwread import *
from nwobject import *

from NoiseApp import *




n = attribute( PROBLEM, SOUND )
 


q = attribute( BARRIER, INSULATION)

a = cause( attribute( NOISE, TOD ), AFFECT )

n = attribute( BARRIER, STATE)
m = event( BARRIER, NOISE, LETINOUT )
m2 = event( n, NOISE, LETINOUT )

sext = "even though there was a wind"
sokens = TOKS(sext)
x = isLogicControl(sokens,0)

j=2
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
 
I = INTENSITY
s = attribute( SOUND, I)


s = attribute( SOUND, [attribute(SOURCE, [attribute(INTENSITY,[TOD])] )] )


#c = sequence(r,s)
c = cause(r,s)
#c=r
 



#text = "The hotel was over a bar and it was very noisy late at night"
#text = "The hotel was near the border and far from downtown"
#text = NoiseText
#text = "My room was far from the elevator and far from the lobby, so it was very quiet."
#text = "the noise outside the hotel was bad late at night"
#text = "it was very noisy late at night"
#text= "window open at night and found the ventilation equipment a bit noisy."
text0 = "Even though my room was close to an elevator and not far from the lobby, it was very quiet."
#text = "it was very quiet"

#text="bar"
#tokens = TOKS(text)
#noi = attribute(SOURCE,NOISE)


#ifound = []
#x = ReadText(noi,tokens,ifound)
#ifound = cleanFound(ifound)
 
#x=2

text="the room was over a noisy bar"
prox = attribute( LOC, attribute(SOURCE, [NOISE]), PROX)  
#prox = attribute( LOC, SOURCE, PROX)  
#prox = attribute(LOC, SOURCE,PROX)
#text = "bar"
#noi = attribute(SOURCE,NOISE)
#D = ABReader(E,noi)
#D.readText(text)
#x = 2
 
R = [ r , s , cause(r,s)] 
K = NWReader(E, R  )
calibs     = [True, True, True]
#K.setCalibration(calibs)

K.readText(text0)
out = K.report()
print( out ) 
#x = 2

#thresholds = [0.3 , 0.3, 0.3 ]
#O = NWObject(E, R, calibs, thresholds)
#O.readText(text)
#x = O.report()
#y = O.printFinal()
#print(x)
#print(y)


  

#N = NoiseApp()
#N.run()


#x = 2


