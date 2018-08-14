from narwhal.nwtypes import *
from narwhal.nwchat import *
from narwhal.nwcontextrecord import *

from stdtrees.geometry import *

from faqVARs import *

def InfoRead( segment, tree, tokens, id, mod, MODS):
    record = ContextRecord(id, MODS)

    nar = faqinfo
    reader = NWTopicReader("faqinfo", tree, nar)

    reader.readSegment( segment, tokens)

    if reader.GOF>=0.6:
        x = reader.lastConst()
        a = reader.getLastAction()
        record.details[mod][0] = a
        record.details[mod][1] = HARDDETAIL 
    return [record]
 
def WantHumanRead( segment, tree, tokens, id, mod, MODS):
    record = ContextRecord(id, MODS)

    nar = faqcontact
    reader = NWTopicReader("faqcontact", tree, nar)

    reader.readSegment( segment, tokens) 
    if reader.GOF>0.6:
        record.details[mod][0] = ''
        record.details[mod][1] = HARDDETAIL 
    return [record]

FaqHandlers = {
            PERSONAL_INFO : InfoRead, 
            PERSONALCONTACT_INFO :  InfoRead,
            PERSONALPHOTO_INFO :  InfoRead,
            BENEFITS_INFO : InfoRead,
            EXPENSES_INFO :  InfoRead,
            FAQHUMAN_ : WantHumanRead
    }
 
