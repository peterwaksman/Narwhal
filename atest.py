# Narwhal atest.py file shows examples, used in testing.

#--------- some core includes
#from nwtypes import *
#from nwutils import *
#from nwread import *
from nwobject import *

#--------- app specific
from NoiseTree import *
from NoiseApp import *

text="2 straight hours between the hours of 5:00am and 7:00am and I am a very light sleeper"
newtext = cleanAMPM(text)


#------------ this 'constant' is the root of the NoiseTree
E = EXPERIENCE 

#---------- examine simple narratives written with variables from the NoiseTree
#n = attribute( PROBLEM, SOUND )
#q = attribute( BARRIER, INSULATION)
#n = attribute( BARRIER, STATE)
#m = event( BARRIER, NOISE, LETINOUT )
#m = event( n, NOISE, LETINOUT )

#------------ experiement defining implicit variables
#s = attribute( SOUND, [attribute(SOURCE, [attribute(INTENSITY,[TOD])] )] )

#------------- experiement defining two part narratives
#c = sequence(r,s)
#c = cause(r,s)
 
 
#------------- single sentences used for testing
text = "windows let in the noise"
text = "walls were thin and noise carries"
text = "windows shut out the noise"
text = "I had no problem with noise but I could see the potential for issues given the wrong neighbors, so bring earplugs. I will definitely return"
text = "we stayed in the block farthest from the road and we heard nothing at all"
text = "There was toilet paper all over the floor and overflowing trash every day."
text = "the hotel was far from the border and near to town"
 
NoiseText = "We did find it a bit noisy with the balcony doors open due "
NoiseText += "to the McDonalds next door - especially late at night and at 6 am "
NoiseText += "when the deliveries started arriving."

text = "The hotel was over a bar and it was very noisy late at night"
text = "The hotel was near the border and far from downtown"
text = "My room was far from the elevator and far from the lobby, so it was very quiet."
text = "the noise outside the hotel was bad late at night"
text = "it was very noisy late at night"
text= "window open at night and found the ventilation equipment a bit noisy."
text = "Even though my room was close to an elevator and not far from the lobby, it was very quiet."
text = "it was very quiet"
text1="the room was over a noisy bar"
text2 = "my room got very hot as it was post-ac season (and opening windows lets in the noise)."
text3 = "It overlooks a main shopping street (hence very convenient) but could be a bit noisy in the evening."
text3 = "It overlooks a main shopping street"
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
textV="there is a continuing dreadful racket as the central heating starts up ever few minutes"
textA = "Fell into bed exhausted but there is a continuing dreadful racket as the central heating starts up ever few minus and makes a huge noise and whine and there is no switch that works to switch it off."
textB = "So blissfully quiet my wife was overjoyed (had suffered disturbed sleep in Firenze..whilst I slept like a log)."
textC = "We did find it a bit noisy with the balcony doors open due to the McDonalds next door - especially late at night and at 6 am when the deliveries started arriving."
textD = "window open at night and found the ventilation equipment a bit noisy."
textE = "The street outside was a busy one with a popular wine bar so a little noisy with the windows open"
textG = "The only downfall of our stay was there was a city work crew running extremely loud machinery (like cutting concrete) for almost 2 straight hours between the hours of 5:00am and 7:00am this was obviously beyond the control of the hotel staff, but nonetheless extremely disappointing for us as we were abruptly woken up and then unable to go back to sleep on our relaxing getaway. "

text5 = "Not one to complain normally I was able to overlook this however I was not able to overlook\
the fact that the walls are paper thin-every footstep, toilet flush, tap turned, and word \
spoken was heard through the walls and to top it all off we were unFortunate to have\
 a wedding party staying on our floor."
text6 = "the walls are paper thin-every footstep, toilet flush, tap turned, and word \
spoken was heard through the walls "  
text7 = "word spoken was heard through the walls"


#prox = attribute( LOC, attribute(SOURCE, [NOISE]), PROX)  
#letin = event( attribute(BARRIER,[STATE]), SOUND, LETINOUT )
#problem = attribute( PROBLEM, SOUND )
#sound = attribute(SOUND,INTENSITY)
#affect  = cause( attribute(SOUND,INTENSITY), AFFECT )
#letin = event( attribute(BARRIER,[STATE]), SOUND, LETINOUT )
 
#----------- read text for a single VAR
#tokens = TOKS(text)
#E.clear()
#f = SOUND.findInText(tokens)  # f=true or false
#ifound = SOUND.ifound
#x = showFound(tokens, ifound) # display text with found tokens marked with asterisk
#print(x)

#--------------- read full text without parsing or token preparation
#------------- here uses 'affect' narrative from the NoiseApp
#ifound = []
#x = ReadText(affect,tokens,ifound)   
#ifound = cleanFound(ifound)
#x = showFound(tokens, ifound)
#print(x) 
#RR = NarRecord(affect,ifound, tokens, len(tokens), 0)

#-------------------- read text with parsing and token prep, using single 'letin' narrative
#-------------------- results are in a "vault" ab.V
#E.clearImplicits()
#ab = ABReader(E,letin)
#ab.readText(text)
#x = 2

#-------------------- read text with parsing and token prep, multiple narratives
#-------------------- with "calibrated" polarity
#--- setup
#R = #[ r , s , cause(r,s)] 
#calibs = [true, true, true]
#R.setCalibration(calibs)
#K = NWReader(E, R  )   # this is the central reading capability

#--- read
#K.readText(textG)
#out = K.report()

#--- examine output
#print( out ) 
#x = 2

#--------------------- read text with parsing, etc AND thresholds to keep or drop results
#thresholds = [0.3 , 0.3, 0.3 ]
#O = NWObject(E, R, calibs, thresholds)
#O.readText(text)
#x = O.report()
#y = O.printFinal()
#print(x)
#print(y)


#-------------- test a final application
N = NoiseApp()
N.test(NoiseText)      # on a single sentence
N.testFile("Ones.txt") # on a file of sentences, for batch testing.




