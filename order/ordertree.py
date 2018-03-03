from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
from stdtrees.ask import * 
from stdtrees.tchats import CLIENTASK 


ORDERNO1 = KList("STR_ORDERNO1", "__sufx__order").var()
ORDERNO2  = KList("STR_ORDERNO2", "__sufx__order _hash_").var()
ORDNOS = KList("ordnos", "").var()
ORDNOS.sub(ORDERNO1)
ORDNOS.sub(ORDERNO2)

PRODUCT = KList("product", " implant, abutment, crown, denture").var()

# use of "not" is not recommended but...trying it revealed a deep bug.
DELAY = KList("delay", "delay, late , not ready ").var()

ONTIME = KList("ontime", "on time , not $ ready, on schedule").var()

#TIMING = ONTIME|DELAY
TIMING = KList("timing","").var()
TIMING.sub(DELAY)
TIMING.sub(ONTIME)

#------------------------------------------------------
MYORDER = KList( "order", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
MYACCOUNT = KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()
MY = KList("my","").var()
MY.sub(MYORDER)
MY.sub(MYACCOUNT)




#-----------------------------------------
inputask = attribute(QUESTION,ORDNOS) #telling the orderno
orderask = attribute(QUESTION, MYORDER)
accountask =  attribute(QUESTION, MYACCOUNT)
productask = attribute(QUESTION,PRODUCT)
#delayask = attribute(QUESTION,DELAY)
delayask = attribute(QUESTION,TIMING)

#-----------------------------------------
ORDERASK = [
            NWTopicReader('inputask', CLIENTASK, inputask ), 
            NWTopicReader('orderask', CLIENTASK, orderask ),
            NWTopicReader('productask', CLIENTASK, productask ),
            NWTopicReader('delayask', CLIENTASK, delayask ) 
            ]

#PRODUCTASK = [NWTopicReader('prodcutinfo', CLIENTASK, productask ) ]

ACCOUNTASK = [NWTopicReader('accountinfo', CLIENTASK, accountask ) ]

#-----------------------------------------
OTREE = KList("otree","").var()
OTREE.sub(CLIENTASK)
#OTREE.sub(MY)
OTREE.sub(MYORDER)
OTREE.sub(MYACCOUNT)
OTREE.sub(PRODUCT)
OTREE.sub(DELAY)
OTREE.sub(IT)
OTREE.sub(ORDNOS) #does it work?
#---------------------------------
OrderAskTopic = NWTopic(OTREE, ORDERASK)
OrderAskTopic.seedContext( [MYORDER] )
AccountAskTopic = NWTopic(OTREE, ACCOUNTASK)

 





