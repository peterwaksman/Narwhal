from PIL import ImageTk, Image, ImageDraw, ImageFont
from math import sqrt

IMGWIDTH = 320
IMGHEIGHT = 320
Oxy = (100,230) # origin is left and low

def DIFF( xyA, xyB):
    a = xyA[0] - xyB[0]
    b = xyA[1] - xyB[1]
    return (a, b)

def SUM( xyA, xyB):
    a = xyA[0] + xyB[0]
    b = xyA[1] + xyB[1]
    return (a, b)

def DIST( xyA, xyB ):
    x = float((xyA[0] - xyB[0])*(xyA[0] - xyB[0]) + (xyA[1] - xyB[1])*(xyA[1] - xyB[1]))
    x = sqrt(x)
    return x

def SCALE( xy, r ):
    s = float(r)
    a = int( s*xy[0])
    b = int( s*xy[1])
    return (a,b)

########### draw functions
DASHLEN = 3.5 # used 
def dottedSegment( draw, P, Q, dashlen ):
    L = DIST( P, Q )
    s = 0.0
    sig=1
    while(1):
        P1 = SUM( P, SCALE( DIFF(Q,P), s/L ) )
        if s+dashlen>L:
            Q1 = Q
        else:
            Q1 = SUM( P, SCALE( DIFF(Q,P),(s+dashlen)/L) )
        
        if sig>0:
            draw.line( [P1,Q1], "black" )

        s += dashlen  
        sig = -sig  
        if s>L:
            break   

def dottedLine( draw, path, dashlen ):
    for i in range(0, len(path)-1):
        P = path[i]
        Q = path[i+1]
        dottedSegment( draw, P, Q, dashlen)


###########################################
# ADJACENT TEETH AND GUMLINE
ADJTEETH_GUM = [ (3,40), (30,40), (30,150), (180, 150), (180,40), (207,40) ]

def drawADJ( draw ):
    draw.line( ADJTEETH_GUM, "black", 3)

#######################
# OPPOSING TEETH
OPPTEETH = [ (35,10), (175,10) ]
def drawOPP( draw ):
    draw.line( OPPTEETH, "black", 3 )

####################################################
# IMPLANT
# 'L' and 'R' for left and right on 2D drawing
# op of the implant

IFACEL = SUM(Oxy,(-20,0))
IFACER = SUM(Oxy,( 20,0)) 

# outline
IMPLANT_1 = [ IFACEL, SUM(IFACEL,(4,55)) , SUM( IFACER, (-4,55)), IFACER ]
# threads
IMPLANT_2 = [ SUM(IFACEL,(1,14)), 
              IFACER, 
              DIFF(IFACER,(1,-14)), 
              SUM(IFACEL,(2,28)), 
              SUM(IFACEL, (3, 42)), 
              DIFF( IFACER, (2,-28)) 
            ]

def drawIMPLANT( draw ):
    draw.line( IMPLANT_1, "black" )
    draw.line( IMPLANT_2, "black" )

#######################################

def drawReferenceFeatures( im):
    draw = ImageDraw.Draw( im )
    drawADJ(draw)
    drawIMPLANT(draw)
    drawOPP(draw)


################ GENERALIZED ABUTMENT
class AbutmentSketch:
    def __init__(self):
        self.ORG = Oxy # if you want the abutment to match the reference features
        self.wbase = 20 # base
        self.wmarg = 36 # margin
        self.wshld = 20 # shoulder
        self.wcin  = 10 # cusp-inner
        self.wcout = 15 #cusp-outer

        # height offsets
        self.hmarg = 60 # margin
        self.hshld = 80 # shoulder
        self.hfos  = 170 # fossa
        self.hcout = 178 # cusp outer
        self.hcin  = 180 # cusp inner

        self.upcnt = 1.0 # used to shape the base
        self.vpcnt = 1.0
        self.cpcnt = 1.0 # used to fatten the core

    def copy(self,other):
        self.ORG   = other.Oxy  
        self.wbase = other.wbase
        self.wmarg = other.wmarg
        self.wshld = other.wshld
        self.wcin  = other.wcin 
        self.wcout = other.wcout

        # height offs# height oets
        self.hmarg = other.hmarg
        self.hshld = other.hshld
        self.hfos  = other.hfos 
        self.hcout = other.hcout
        self.hcin  = other.hcin 

        self.upcnt = other.upcnt
        self.vpcnt = v.vpcnt
        self.cpcnt = other.cpcnt 

        # should not need, as we comp() the AbutmentState data
    def comp( self, other):
        if( 
            self.ORG   == other.Oxy   and
            self.wbase == other.wbase and
            self.wmarg == other.wmarg and
            self.wshld == other.wshld and
            self.wcin  == other.wcin  and
            self.wcout == other.wcout and

            # height offs# height oets
            self.hmarg == other.hmarg and
            self.hshld == other.hshld and
            self.hfos  == other.hfos  and
            self.hcout == other.hcout and
            self.hcin  == other.hcin  and

            self.upcnt == other.upcnt and
            self.vpcnt == v.vpcnt  and
            self.cpcnt == other.cpcnt           
            ):
            return True
        else:
            return False
                                

    def getTOP( self ):
        ORG = self.ORG
        MARGL = SUM( ORG, (-self.wmarg,-self.hmarg) )
        MARGR = SUM(ORG, (self.wmarg, -self.hmarg) )

        u = self.cpcnt

        SHLDL = SUM( ORG,(-u*self.wshld,-self.hshld) )
        SHLDR = SUM( ORG, (u*self.wshld,-self.hshld) )

        FOS = SUM( ORG, (0,-self.hfos) )

        A = SUM(ORG, (-u*self.wcout,-self.hcout) )
        B = SUM( ORG, (-u*self.wcin,-self.hcin) )
        C = SUM( ORG, (u*self.wcin, -self.hcin) )
        D = SUM( ORG, (u*self.wcout,-self.hcout) )
        TOP = [ MARGL, SHLDL, A, B, FOS, C, D, SHLDR, MARGR ]
        return TOP

    def getBASE(self):
        ORG = self.ORG
        h = self.hmarg

        MARGL = SUM( ORG, (-self.wmarg,-h) )
        MARGR = SUM(ORG,   (self.wmarg,-h) )

        BASEL = SUM( ORG, (-self.wbase,0) )
        BASER = SUM( ORG,  (self.wbase,0) )
        
        u = self.upcnt 
        v = self.vpcnt 
        UL = SUM(ORG, (-self.wbase - u*0.6*(self.wmarg-self.wbase),-0.6*h) ) 
        VL = SUM(ORG, (-self.wbase - v*0.3*(self.wmarg-self.wbase), -.3*h) )
        UR = SUM(ORG, (self.wbase + u*0.6*(self.wmarg-self.wbase),-0.6*h) ) 
        VR = SUM(ORG, (self.wbase + v*0.3*(self.wmarg-self.wbase), -.3*h) )
        BASE = [ MARGL, UL, VL, BASEL, BASER, VR, UR, MARGR ]
        return BASE

    def getMARG(self):
        ORG = self.ORG
        MARGL = SUM( ORG, (-self.wmarg,-self.hmarg) )
        MARGR = SUM(ORG, (self.wmarg, -self.hmarg) )
        MARG = [MARGL, MARGR]
        return MARG

    def Draw( self, im ):
        draw = ImageDraw.Draw( im )

        B = self.getBASE()
        dottedLine( draw, B, DASHLEN )

        M = self.getMARG()
        draw.line( M, "black", 3)

        T = self.getTOP()
        dottedLine( draw, T, DASHLEN )

        # show a supragingival margin
    def makeSupraG(self):
        delta = 40
        if self.hmarg<80:
            self.hmarg += delta
            self.hshld += delta
 
            # default
    def makeSubG(self):
        self.hmarg = 60
        self.hshld = 80  

    def makeAtIface(self):
        self.hmarg = 10
        self.hshld = 30

        # same as makeSubG. The indicators will change but not picture
    def makeAtAdjacent(self):
        self.hmarg = 60
        self.hshld = 80

    def makeConvex(self):
        self.upcnt = 1.6
        self.vpcnt = 1.6
    def makeConcave(self):
        self.upcnt = 0.4
        self.vpcnt = 0.3
    def makeAnkylos(self):
        self.upcnt = 0.8
        self.vpcnt = 1.0

    def makeStraight(self):
        self.upcnt = 1.0
        self.vpcnt = 1.0

        # these do nothing but parallel indicator changes
    def makeNoDisplace(self):
        x=2
    def makeFullAnatomical(self): 
        x=2
    def makeContourTissue(self):
        x=2
    def makeSupportTissue(self):
        x=2

    def makeCoreNormal(self):
        self.cpcnt = 1.0
    def makeCoreFat(self):
        self.cpcnt = 1.3
###############################################

# eps settings
STAIGHTEPS = 0
CONCAVEEPS = 1
CONVEXEPS  = 2
ANKYLOSEPS = 3
# margin (height) reference settings
GUMREF = 0
IFACEMREF = 1
ADJMREF = 2

# AMOUNT rel reference
BELOWAMT = 0
ABOVEAMT = 1
ATAMT = 2
CLOSEAMT = 3

# tissue pressure (width settings
NODISPLACE = 0
FULLANATOM = 1
CONTOURTIS = 2
SUPPORTTIS = 3
# core thinkness
NORMALCORE = 0
FATCORE = 1
THINCORE = 2

class AbutmentState:
    def __init__(self):
        self.mref = GUMREF
        self.mamt = BELOWAMT
        self.tiss = NODISPLACE
        self.epsshape = STAIGHTEPS
        self.core = NORMALCORE

    def copy(self,other):
        self.mref     = other.mref   
        self.mamt     = other.mamt 
        self.tiss     = other.tiss    
        self.epsshape = other.epsshape
        self.core     = other.core    
    def comp(self, other ):
        if( 
            self.mref     == other.mref    and
            self.mamt     == other.mamt    and
            self.tiss     == other.tiss    and
            self.epsshape == other.epsshape and
            self.core     == other.core   ):
            return True
        else:
            return False

    def setEPSParams(self, sketch):
        h = sketch
        G = self

        if self.epsshape == STAIGHTEPS:
            sketch.makeStraight()
        elif self.epsshape == CONCAVEEPS:
            sketch.makeConcave()
        elif self.epsshape == CONVEXEPS:
            sketch.makeConvex()
        elif self.epsshape == ANKYLOSEPS:
            sketch.makeAnkylos()

    def setMarginReference(self, sketch):
          # TO DO, add other pics for AT and close
        if self.mref == GUMREF and (self.mamt==BELOWAMT or self.mamt==ATAMT or self.mamt==CLOSEAMT ):
            sketch.makeSubG()
        elif self.mref == GUMREF and self.mamt==ABOVEAMT:
            sketch.makeSupraG()
        elif self.mref == IFACEMREF:
            sketch.makeAtIFace()
        elif self.mref == ADJMREF:
            sketch.makeAtAdjacent()

    def setTissueDisplacement(self, sketch):
        if self.tiss == NODISPLACE :
            sketch.makeNoDisplace()
        elif self.tiss == FULLANATOM :
            sketch.makeFullAnatomical()
        elif self.tiss == CONTOURTIS: 
            sketch.makeContourTissue()
        elif self.tiss == SUPPORTTIS:
            sketch.makeSupportTissue()

    def setCoreThickness(self, sketch, thick):
                # to do
        if thick==NORMALCORE or thick==THINCORE:
            sketch.makeCoreNormal()
            self.core = thick
        elif thick==FATCORE:
            sketch.makeCoreFat()
            self.core = thick
            
    