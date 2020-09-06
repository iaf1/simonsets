#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:40:56 2020

@author: ivan
"""


import cv2
import urllib.request
import numpy as np
import time
from initSettings import cf

URL = "http://192.168.0.66:8080/shot.jpg"
#URL = "http://www.pyimagesearch.com/wp-content/uploads/2015/01/google_logo.png"


def shootpic():
    
    while True:
        # Use urllib to get the image and convert into a cv2 usable format
            imgResp=urllib.request.urlopen(cf.URL)
            imgNp=np.asarray(bytearray(imgResp.read()),dtype=np.uint8)
            img=cv2.imdecode(imgNp,-1)
        
            # put the image on screen
            cv2.imshow('IPWebcam',img)
        
            #To give the processor some less stress
            time.sleep(0.1) 
        
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break
    
    return img
