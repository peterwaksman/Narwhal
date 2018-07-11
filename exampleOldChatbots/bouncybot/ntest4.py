#!/usr/bin/env python
"""
Basic example. 
"""
#temppath = "C:\\Users\\Edge540\\Desktop\\temp\\"
#path0 = temppath + "temp.jpg"

#class intswap():
#    def __init__(self):
#        self.val = 0

#GG = intswap()

#path = "c:\\MB.png"
#path2 = "c:\\MFlowers.png"
#path3 = "c:\\Blank.png"


#def testf(event):

#    img = ImageTk.PhotoImage(Image.open(path))
#    img2 = ImageTk.PhotoImage(Image.open(path2))
#    img3 = ImageTk.PhotoImage(Image.open(path3))

#    panel = Label(root, image = img)
#    panel.grid(row=8, column = 0)
#    if GG.val==0:
#        panel.configure( image=img2 )
#        panel.image = img2
#        GG.val = 1
#    elif GG.val==1:
#        panel.configure( image=img )
#        panel.image = img
#        GG.val = 2
#    elif GG.val==2:
#        panel.configure( image=img3 )
#        panel.image = img3
#        GG.val = 0
#    print "You typed " + T.get()

import sys
import os 

ver = sys.version.split('.')
majorV = ver[0]
if int(majorV)>2 :
    getinput = input
else:
    getinput = raw_input


this_file = os.path.abspath(__file__)
narwhal_dir = os.path.join(os.path.dirname(this_file), '..')
narwhal_dir = os.path.normpath(narwhal_dir)
sys.path.insert(0, narwhal_dir)


from Tkinter import *
from PIL import ImageTk, Image

from narwhal.nwchat import NWDataChat

from bouncyscene import *
from bouncychat import *

BScene = BouncySceneData("red",False,SMALLRAD,[Ox+SMALLRAD,Oy-2*SMALLRAD],False, TICWIDTH, [Ox,Oy] )
BB = BouncyChat( BScene )

def initImage():
    h = Image.new("RGB",(IMGWIDTH,IMGHEIGHT), "white")    
    img = ImageTk.PhotoImage(h)
    panel = Label(root, image = img)
    panel.grid(row=8, column = 0)
    
    panel.configure( image=img )
    panel.image = img

def readText(event):
    text = T.get()
    BB.Read(text)
    if False and BB.data.comp( BB.prevdata ):
        return

    h = Image.new("RGB",(IMGWIDTH,IMGHEIGHT), "white")    

    BB.data.drawScene( h )
    
    img = ImageTk.PhotoImage(h)

    panel = Label(root, image = img)
    panel.grid(row=8, column = 0)
    
    panel.configure( image=img )
    panel.image = img
 
    s = BB.Write()
    response.set(s)
    print s

#This creates the main root of an application
root = Tk()
root.title("Bouncy")
root.geometry("640x480")
root.configure(background='grey')

# text entry
T = Entry(root, width=80)
T.bind("<Return>", readText)
T.grid(row=1, column=0) 
 
initImage()

response = StringVar()

#e = Entry(root, textvariable=response)
#e.config(width=60, font="Courier 12 bold")
#e.grid()
response.set("")

e = Label(root, background='white', anchor=W, textvariable=response)
e.config(width=60, font="Courier 14 bold")
e.grid()

#Start the GUI
root.mainloop()

