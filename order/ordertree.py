from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
from stdtrees.ask import * 
from stdtrees.tchats import CLIENTASK 


ORDERNO = KList("STR_ORDERNO", "__sufx__order").var()

PRODUCT = KList("product", " implant, abutment, crown, denture").var()

# use of "not" is not recommended but...trying it revealed a deep bug.
DELAY = KList("delay", "delay, late , not ready ").var()

#------------------------------------------------------
MYORDER = KList( "order", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
MYACCOUNT = KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()
MY = KList("my","").var()
MY.sub(MYORDER)
MY.sub(MYACCOUNT)




#-----------------------------------------
inputask = attribute(QUESTION,ORDERNO) #telling the orderno
orderask = attribute(QUESTION, MYORDER)
accountask =  attribute(QUESTION, MYACCOUNT)
productask = attribute(QUESTION,PRODUCT)
delayask = attribute(QUESTION,DELAY)

#-----------------------------------------
ORDERASK = [NWTopicReader('inputask', CLIENTASK, inputask ), 
            NWTopicReader('orderask', CLIENTASK, orderask ),
            NWTopicReader('productask', CLIENTASK, productask ),
            NWTopicReader('delayask', CLIENTASK, delayask ) ]

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
OTREE.sub(ORDERNO) #does it work?
#---------------------------------
OrderAskTopic = NWTopic(OTREE, ORDERASK)
OrderAskTopic.seedContext( [MYORDER] )
AccountAskTopic = NWTopic(OTREE, ACCOUNTASK)

 





