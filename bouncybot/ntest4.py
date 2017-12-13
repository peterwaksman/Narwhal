#!/usr/bin/env python
"""
Basic example. 
"""

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

from narwhal.nwchat import NWTopicChat

from bouncyscene import *
from bouncychat import *

# Initialize the scene data, and the editor/reader chatbot
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
    print s

    response.set(s)


#----------- APP ------------------
root = Tk()
root.title("Bouncy")
root.geometry("640x480")
root.configure(background='grey')

# text entry bound to readText()
T = Entry(root, width=80)
T.bind("<Return>", readText)
T.grid(row=1, column=0) 
 
initImage()

response = StringVar()
e = Entry(root, textvariable=response)
e.config(width=60)
e.grid()
response.set("")

#Start the GUI
root.mainloop()

