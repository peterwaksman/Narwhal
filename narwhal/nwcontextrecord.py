
""" 
Context Record is going to be another tree structure

"""
# Detail status
EMPTYDETAIL=0 # never written or copied 
SOFTDETAIL=1  # when copied to programmatically, as an assumption
HARDDETAIL=2  # when written to, because of the incoming text

def strStatus(status):
    if status==EMPTYDETAIL:
        return '0'
    elif status==SOFTDETAIL:
        return 'S'
    else:
        return 'H'


class ContextRecord():
    def __init__(self, id = '', contextMods = []):
        self.id = id

        # details are indexed by mods of the context
        self.details = {}
        for m in contextMods:
            self.details[ m ] = ['' , EMPTYDETAIL]

        self.children = []

    def str(self, ntabs=0):
        pre = ''
        for i in range(0,ntabs):
            pre += "\t"

        out = pre

  
                        # id
        out += self.id + ":"

                        # details (mod values)
        M = self.details
        out += '('
        for mod in M:
            out += '['
            out +=  M[mod][0] + ',' + strStatus(M[mod][1])
            out += "]"

            if mod<len(M)-1:
                out += ','
            
        out += ')\n'

        for c in self.children:
            out += c.str(ntabs+1) + '\n' # use record.str()

        return out 
 

    def merge(self, other):
        if self.id!=other.id:
            print("OOPS!")
        for d in self.details:
            self.details[d] = other.details[d] # copy
            if self.details[d][0]:
                self.details[d][1] = HARDDETAIL #harden content

    def copy(self):
        other = ContextRecord( self.id, self.mods)
        other.details = {}
        for d in self.details:
            detail = self.details[ d ][:]  # copy the list
            other.details[d] = detail      # store here

            if detail[0]: # the mod has a value
                detail[1] = SOFTDETAIL

        other.children = []
        return other

        for child in self.children:
            q = child.copy()
            other.children.append( q )

        return other  
    
    def harden( self ):
        for d in self.details:
            if self.details[d][0]: # the mod has a value
                self.details[d][1] = HARDDETAIL

        for child in self.children:
            child.harden() 

    def currentDetails(self):
        nesting = [self]
        if self.children:
            child = self.children[ len(self.children)-1 ] 
        else:
            child = None 
             
        if child:
            nesting.extend( child.currentDetails() )

        return nesting


    def append(self, id, mod, val):
        nesting = self.currentDetails()
        for detail in nesting:
            if id != detail.id:
                continue
            else:
                x = 2

    def getDetail(self, mod):
        try:
            return self.details[mod][0]
        except:
            return ''



                