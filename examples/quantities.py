"""
quantities.py lists numbers in various forms, as VARs
"""

from narwhal.nwtypes import KList

kZERO = ' none , zero , 0 '
kONE  = ' one , an, a , 1 '
kTWO = ' two , 2 '
kTHREE = ' three , 3 '
kFOUR  = ' four , 4 '
kFIVE = ' five , 5 '
kSIX  = ' six , 6 '
kSEVEN = ' seven , 7 '
kEIGHT = ' eight , 8 '
kNINE = ' nine , 9 '
kTEN  = ' ten , 10 '
kELEVEN = ' eleven , 11 '
kTWELVE = ' twelve , 12 '
kTHIRTEEN = ' thirteen , 13 '
kFOURTEEN = ' fourteen, 14 '
kFIFTEEN = ' fifteen , 15 '
kSIXTEEN = ' sixteen, 16 '
kSEVENTEEN = ' seventeen , 17 '
kEIGHTEEN = ' eighteen , 18 '
kNINETEEN = ' nineteen , 19 '
kTWENTY = ' twenty # one|two|three|four|five|six|seven|eight|nine, 20 '
kTWENTYONE = ' twenty one , 21 '
kTWENTYTWO = ' twenty two , 22 '
kTWENTYTHREE = ' twenty three , 23 '
kTWENTYFOUR = ' twenty four , 24 '
kTWENTYFIVE = ' twenty five , 25 '
kTWENTYSIX = ' twenty six , 26 '
kTWENTYSEVEN = ' twenty seven , 27 '
kTWENTYEIGHT = ' twenty eight , 28 '
kTWENTYNINE = ' twenty none , 29 '
kTHIRTY = ' thirty # one|two, 30 '
kTHIRTYONE = ' thirty one , 30 '
kTHIRTYTWO = ' thirty two , 30 '

kQUANTITY = ' quantity '
QUANTITY = KList( "quantity", kQUANTITY).var()


ZERO = KList( kZERO ).var()
ONE = KList( kONE ).var()
TWO = KList( kTWO ).var()
THREE = KList( kTHREE ).var()
FOUR = KList( kFOUR ).var()
FIVE = KList( kFIVE ).var()
SIX = KList( kSIX ).var()
SEVEN = KList( kSEVEN ).var()
EIGHT = KList( kEIGHT ).var()
NINE = KList( kNINE  ).var()
TEN = KList( kTEN  ).var()
ELEVEN = KList( kELEVEN  ).var()
TWELVE = KList( kTWELVE ).var()
THIRTEEN = KList( kTHIRTEEN  ).var()
FOURTEEN = KList( kFOURTEEN ).var()
FIFTEEN = KList( kFIFTEEN  ).var()
SIXTEEN = KList( kSIXTEEN  ).var()
SEVENTEEN = KList( kSEVENTEEN ).var()
EIGHTEEN = KList( kEIGHTEEN  ).var()
NINETEEN = KList( kNINETEEN  ).var()
TWENTY = KList( kTWENTY  ).var()
TWENTYONE = KList( kTWENTYONE ).var()
TWENTYTWO =  KList( kTWENTYTWO ).var()
TWENTYTHREE = KList( kTWENTYTHREE  ).var()
TWENTYFOUR = KList( kTWENTYFOUR ).var()
TWENTYFIVE= KList( kTWENTYFIVE ).var()
TWENTYSIX= KList( kTWENTYSIX  ).var()
TWENTYSEVEN = KList( kTWENTYSEVEN  ).var()
TWENTYEIGHT = KList( kTWENTYEIGHT  ).var()
TWENTYNINE = KList( kTWENTYNINE  ).var()
THIRTY = KList( kTHIRTY  ).var()
THIRTYONE = KList( kTHIRTYONE  ).var()
THIRTYTWO = KList( kTHIRTYTWO  ).var()


kQUANTITY = ' quantity '
QUANTITY = KList( "quantity", kQUANTITY).var()
QUANTITY.sub(ZERO)
QUANTITY.sub(ONE)
QUANTITY.sub(TWO)
QUANTITY.sub(THREE)
QUANTITY.sub(FOUR)
QUANTITY.sub(FIVE)
QUANTITY.sub(SIX)
QUANTITY.sub(SEVEN)
QUANTITY.sub(EIGHT)
QUANTITY.sub(NINE)
QUANTITY.sub(TEN)
QUANTITY.sub(ELEVEN)
QUANTITY.sub(TWELVE)
QUANTITY.sub( THIRTEEN )
QUANTITY.sub(FOURTEEN)
QUANTITY.sub(FIFTEEN)
QUANTITY.sub(SIXTEEN)
QUANTITY.sub(SEVENTEEN)
QUANTITY.sub(EIGHTEEN)
QUANTITY.sub(NINETEEN)
QUANTITY.sub(TWENTY)
QUANTITY.sub(TWENTYONE)
QUANTITY.sub(TWENTYTWO)
QUANTITY.sub(TWENTYTHREE)
QUANTITY.sub(TWENTYFOUR)
QUANTITY.sub(TWENTYFIVE)
QUANTITY.sub(TWENTYSIX)
QUANTITY.sub(TWENTYSEVEN)
QUANTITY.sub(TWENTYEIGHT)
QUANTITY.sub(TWENTYNINE)
QUANTITY.sub(THIRTY)
QUANTITY.sub(THIRTYONE)
QUANTITY.sub(THIRTYTWO)
