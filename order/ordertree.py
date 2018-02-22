from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
from stdtrees.ask import * 
from stdtrees.tchats import CLIENTASK 


PRODUCT = KList("product", " implant, abutment, crown, denture").var()

DELAY = KList("delay", "delay, late ").var()

#------------------------------------------------------
MYORDER = KList( "order", ' my order , my * order , order , the order  , an order , case , a case , the case ').var()
MYACCOUNT = KList( "account", ' account , payment , amount due , cost , pay , finance' ).var()
MY = KList("my","").var()
MY.sub(MYORDER)
MY.sub(MYACCOUNT)




#-----------------------------------------
orderask = attribute(QUESTION, MYORDER)
accountask =  attribute(QUESTION, MYACCOUNT)
productask = attribute(QUESTION,PRODUCT)
delayask = attribute(QUESTION,DELAY)

#-----------------------------------------
ORDERASK = [NWTopicReader('orderask', CLIENTASK, orderask ),
            NWTopicReader('productask', CLIENTASK, productask ) ,
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
#---------------------------------
OrderAskTopic = NWTopic(OTREE, ORDERASK)
AccountAskTopic = NWTopic(OTREE, ACCOUNTASK)

 





