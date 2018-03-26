from narwhal.nwtypes import *
from narwhal.nwchat import *

from stdtrees.quantities import *
from stdtrees.geometry import * 
from stdtrees.ask import * 
from stdtrees.tchats import CLIENTASK 

# command strings
DOCOMMAND = KList("STR_DO", "__sufx__do").var()
CHANGEMATERIAL = KList("changematerial", "changematerial, materialchange").var();

# command handlers
def executeDo( args ):
    return True
def executeChangeMaterial( args ):
    return False # experiment

 # pairs of command word : handler function
CommandDictionary = {
                        DOCOMMAND: executeDo,
                        CHANGEMATERIAL: executeChangeMaterial
                    }

MyCommandsChat = CommandsChat( CommandDictionary )
 
 

