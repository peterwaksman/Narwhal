#!/usr/bin/env python
"""
Basic example. 
"""
temppath = "C:\\Users\\Edge540\\Desktop\\temp\\"
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

#from narwhal.nwchat import NWTopicChat
from stdtrees.tchats import *
from abutmentChats import BaseChat, MarginChat , DentalChat

Q = DentalChat()
#Q = AboutChat()  + BaseChat()
#Q = BaseChat()
#Q = MarginChat()  + BaseChat() + AboutChat()


IMGHWIDTH=300
IMGHEIGHT=300

def initImage():

    h = Image.new("RGB",(IMGHWIDTH,IMGHEIGHT), "white")    

    #drawReferenceFeatures(h)

    #K = ABT.sketch
    #K.Draw(h)  

    img = ImageTk.PhotoImage(h)
    panel = Label(root, image = img)
    panel.grid(row=8, column = 0)
    
    panel.configure( image=img )
    panel.image = img


def readText(event):
    text = T.get()
    Q.Read(text)

    h = Image.new("RGB",(IMGHWIDTH,IMGHEIGHT), "white")    

    #drawReferenceFeatures(h)

    #K = ABT.sketch
    #K.Draw(h)  
     
    img = ImageTk.PhotoImage(h)

    panel = Label(root, image = img)
    panel.grid(row=8, column = 0)
    
    panel.configure( image=img )
    panel.image = img
 
    s = Q.Write()#''#ABT.responder.getStageResponse()
    response.set(s)

#This creates the main root of an application
root = Tk()
root.title("AbutmentChat")
root.geometry("640x480")
root.configure(background='grey')

# text entry
T = Entry(root, width=80)
T.bind("<Return>", readText)
T.grid(row=1, column=0) 
 
# display blank background for starters
initImage()

response = StringVar()
e = Entry(root, textvariable=response)
e.config(width=60)
e.grid()
response.set("")


root.mainloop()

