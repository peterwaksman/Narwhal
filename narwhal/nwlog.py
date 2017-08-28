"""
nwlog.py - to handle logging. A log file is named after a day of the week. 
For each entry, the file is opended and appended to; then closed.
Each time the NWLog is instantiated it writes a header line to that day's file
"""

import sys
import os 
from time import gmtime, strftime


class NWLog:
    def __init__(self):
        # standard day-of-week log file
        tstr = gmtime()
        day = strftime("%a", tstr )
        self.fname = "log" + day + ".txt" 

        # header for this instance of the logger
        f = open(self.fname, 'a') 
        t = strftime("%a, %d %b %Y %H:%M:%S", tstr ) +"\n----------------------\n"
        f.write(t)
        f.close() 


    def add(self, t ):
        f = open(self.fname, 'a') 
        f.write(t)
        f.close() 
