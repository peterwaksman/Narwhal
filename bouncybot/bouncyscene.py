from Tkinter import *

from PIL import ImageTk, Image, ImageDraw, ImageFont

SMALLZOOM = 1.0
BIGZOOM = 2.0
MAXZOOM = BIGZOOM
MINZOOM = SMALLZOOM/2

SMALLRAD = 60
BIGRAD = 120

TICWIDTH = 15 # use 30 when sscale
NUMTICS = 12

SCALELEN = (NUMTICS+1)*TICWIDTH
IMGWIDTH = 320
IMGHEIGHT = 400
Ox = 20
Oy = IMGHEIGHT - 20

MYTEMP = "C:\\Users\\Edge540\\Desktop\\temp\\"

class BouncySceneData:
    """
    Attributes of the ball:
    color - a string like "red"
    display - a bool for hide/show
    size - a radius like BIGRAD or SMALLRAD
    xy - a 2 tuple of positive ints the center of the ball
    
    Attributes of the scale are prefixed with 's'. sxy is the start of scale
    """

    def __init__(self, color='white', display=False, size=0, xy=(0,0), sdisplay=False, ssize=0, sxy=(0,0)):
        self.ballcolor = color
        self.balldisplay = display
        self.ballsize = size
        self.ballxy =  xy

        self.scaledisplay = sdisplay
        self.scalesize = ssize
        self.scalexy = sxy

        self.zoom = SMALLZOOM

    def comp(self, other): 
        if ( self.ballcolor==other.ballcolor  and
             self.balldisplay==other.balldisplay and
             self.ballsize==other.ballsize and
             self.ballxy==other.ballxy and
             self.scaledisplay==other.scaledisplay and
             self.scalesize==other.scalesize and
             self.scalexy==other.scalexy and
             self.zoom== other.zoom ):
            return True
        else:
            return False

    def copy(self,other):         
        self.ballcolor=other.ballcolor  
        self.balldisplay=other.balldisplay 
        self.ballsize=other.ballsize 
        self.ballxy=other.ballxy 
        self.scaledisplay=other.scaledisplay 
        self.scalesize=other.scalesize 
        self.scalexy=other.scalexy 
        self.zoom = other.zoom

    def drawBall(self, im):
        if not self.balldisplay:
            return

        draw = ImageDraw.Draw( im )
        Z = self.zoom
        xy = self.ballxy
        X = xy[0]*Z
        Y = xy[1]*Z
        xy1 = (X-self.ballsize*Z, Y-self.ballsize*Z)
        xy2 = (X+self.ballsize*Z, Y+self.ballsize*Z)
        draw.ellipse( [xy1, xy2], self.ballcolor)


    def drawScale(self, im):
        if not self.scaledisplay:
            return

        draw = ImageDraw.Draw( im )
        
        Z = self.zoom
        xy = self.scalexy
        X = xy[0]*Z
        Y = xy[1]*Z
        draw.line( [(X,Y), (X + NUMTICS*TICWIDTH*Z, Y)], "black" )

        for i in range(0, NUMTICS+1):
            iX = X + i*TICWIDTH*Z
            draw.line( [ (iX, Y-10), (iX, Y+10 )], "black" )

    def drawScene(self, im):  
        self.drawBall(im)
         
        self.drawScale(im)       
         

        # drawScale(self, im)
        #if self.scaledisplay:
        #    Z = self.zoom
        #    xy = self.scalexy
        #    X = xy[0]*Z
        #    Y = xy[1]*Z 
        #    draw.line( (X,Y,X+ NUMTICS*TICWIDTH*Z, Y))

        #    lo = xy[1]-10
        #    hi = xy[1]+10
        #    for i in range(0, NUMTICKS+1):
        #        xy1 = (xy[0] + i*TICWIDTH*Z, lo*Z )
        #        xy2 = (xy[0] + i*TICWIDTH*Z, hi*Z )
        #        draw.line( xy1, xy2 )
