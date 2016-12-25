
from nwtypes import *
from NoiseTree import *
from nwutils import *
from nwread import *
from nwobject import *

from NoiseApp import *




n = attribute( PROBLEM, SOUND )
 


q = attribute( BARRIER, INSULATION)

a = cause( attribute( NOISE, [TOD] ), AFFECT )

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
text1="the room was over a noisy bar"
text2 = "my room got very hot as it was post-ac season (and opening windows lets in the noise)."
text3 = "It overlooks a main shopping street (hence very convenient) but could be a bit noisy in the evening."
#text3 = "It overlooks a main shopping street"
text4 = "Stayed here back in 2002 and was lovely and decided to return for a 'date night' \
with the husband. After paying extortionate valet parking prices check in was uneventful. \
The foyer looks lovely and lulls you into a false sense of security, however The rooms \
whilst clean are outdated and old fashioned .i think the rooms actually looked better back\
 in 2002. The bathrooms were standard and smelt of mould and damp and the towels were\
 stained and grotty. The Pool area is tiny (thank god we didn't have the children with us).\
 Not one to complain normally I was able to overlook this however I was not able to overlook\
 the fact that the walls are pAper thin-every footstep, toilet flush, tap turned, and word \
 spoken was heard through the walls and to top it all off we were unFortunate to have a \
 wedding party/guests staying on our floor. These guests took it upon themselves to ruin \
 our night. From 12.18am til 3.30am the fourth floor was a 3ring circus. At one point \
 10 people were outside my room having.a party. Only when I called reception did it go \
 quiet-not for long though -yep it started again- people running up and down hallways, \
 slamming doors, in and out of each other's rooms and being VERY loud. Then at 7am it was \
 all on again. Don't know how it can be \
 called 5 star hotel. Very disappointing Duxton. For the price of hotels or anything in \
 Perth \for that matter I expect a lot more. No wonder I and others prefer to spend our \
 hard earned cash overseas when this is the service and standard we get in Perth. Shame."

text7 = "word spoken was heard through the walls"
text6 = "the walls are paper thin-every footstep, toilet flush, tap turned, and word \
spoken was heard through the walls "  
text5 = "Not one to complain normally I was able to overlook this however I was not able to overlook\
the fact that the walls are paper thin-every footstep, toilet flush, tap turned, and word \
spoken was heard through the walls and to top it all off we were unFortunate to have\
 a wedding party staying on our floor."
text8 = "we were unFortunate to have a wedding party staying on our floor."
textQ = "You cannot go wrong staying at the Dolphin. Great location at a great price. Simple healthy breakfast and friendly helpful staff and free parking. Walk to the wharfs; great seafood and Mexican dining a stroll away and an easy drive to most of the highlights of the city. Only real critiscm is the wifi speed is good enough for surfing the net and e-mail but not for Netflix. Highly recommend; amazing value for $$. "

textU="Fell into bed exhausted but there is a continuing dreadful racket as the central heating starts up ever few minutes"
textA = "Fell into bed exhausted but there is a continuing dreadful racket as the central heating starts up ever few minus and makes a huge noise and whine and there is no switch that works to switch it off."
textB = "So blissfully quiet my wife was overjoyed (had suffered disturbed sleep in Firenze..whilst I slept like a log)."
textC = "We did find it a bit noisy with the balcony doors open due to the McDonalds next door - especially late at night and at 6 am when the deliveries started arriving."

E.clearImplicits()
#prox = attribute( LOC, attribute(SOURCE, [NOISE]), PROX)  
#letin = event( attribute(BARRIER,[STATE]), SOUND, LETINOUT )
#problem = attribute( PROBLEM, SOUND )


sound = attribute(SOUND,INTENSITY)
#affect  = cause( attribute(SOUND,INTENSITY), AFFECT )
affect  = cause( AFFECT, attribute(SOUND,INTENSITY)  )

tokens = TOKS(textU)
ifound = []

#E.clear()
#x = E.findInText(tokens)
#r = histo(E.ifound, len(tokens))

#x = ReadText(affect,tokens,ifound)  # CAUTION: no PrepareTokens() 
#ifound = cleanFound(ifound)
#x = showFound(tokens, ifound)
#print(x) 

#D = ABReader(E,letin)
#D.readText(text)
#x = 2

 

R = [affect] #[ r , s , cause(r,s)] 
K = NWReader(E, R  )

K.readText(textU)
out = K.report()
print( out ) 
x = 2

#thresholds = [0.3 , 0.3, 0.3 ]
#O = NWObject(E, R, calibs, thresholds)
#O.readText(text)
#x = O.report()
#y = O.printFinal()
#print(x)
#print(y)


text5 = "Not one to complain normally I was able to overlook this however I was not able to overlook\
the fact that the walls are paper thin-every footstep, toilet flush, tap turned, and word \
spoken was heard through the walls and to top it all off we were unFortunate to have\
 a wedding party staying on our floor."

#text6 = "the walls are paper thin-every footstep, toilet flush, tap turned, and word \
#spoken was heard through the walls "  
##text7 = "word spoken was heard through the walls"

#N = NoiseApp()

#N.testFile("Ones.txt")


#x = 2


