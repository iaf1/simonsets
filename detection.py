#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:40:02 2020

@author: ivan
"""

import cv2
from connection import shootpic
import matplotlib.pyplot as plt
import numpy as np
from functions import *
from classification import classification
from draw import draw_pattern, put_text

from initSettings import cf

from sys import platform
from PIL import Image, ImageFont, ImageDraw
from matplotlib import cm

img = cv2.imread('full_image.jpeg')  # cv2 uses BGR

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to HSV
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale

############################################################################ PIL #####
img_pil = Image.fromarray((img_rgb).astype(np.uint8))                               ##
draw = ImageDraw.Draw(img_pil)                                                      ##
if platform == "linux" or platform == "linux2":                                     ##
    font = ImageFont.truetype(cf.font_path_lin, cf.font_size)                       ##
elif platform == "darwin":                                                          ##
    raise NotImplementedError                                                       ##
elif platform == "win32":                                                           ## 
    font = ImageFont.truetype(cf.font_path_win, cf.font_size)                        ##
######################################################################################

# We apply a Canny edge detector

edges = cv2.Canny(img_gray, 200, 500)

# We find the contours


contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

masks = []
board = []
boxes = []


cv2.drawContours(img_gray, contours, -1, 255, thickness=5)

for idx in range(len(contours)):
    #print(idx)
    mask = np.zeros_like(img_gray) # Create mask where white is what we want, black otherwise
    
    cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask
    mask2 = mask.copy()
        
    perc_nonzero = np.count_nonzero(mask) / (mask.shape[0]*mask.shape[1])
    
    if perc_nonzero < cf.thresh_card_perc: continue

    out = np.zeros_like(img) # Extract out the object and place into output image
    out[mask == 255] = img[mask == 255]
    
    rect = cv2.minAreaRect(contours[idx])
    box = cv2.boxPoints(rect)

    tup_props = classification(out)
    
    num, shape, col, fil = tup_props
    print('Number: {n} | Shape: {s} | Color: {c} | Filling: {f}'.format(c=COLORS[col], f=FILLS[fil], s=SHAPES[shape], n=str(num)))
    
    if cf.show_cards:
        # Show the output image
        cv2.imshow('Output', cv2.resize(out, (750, 1000)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    board.append(Card(tup_props))
    masks.append(mask)
    boxes.append(box)


    
    
img_text = put_text(img_rgb, board, boxes)

plt.figure()
plt.imshow(img_text)

list_of_sets = find_sets(board)

print(list_of_sets)

img_out, _ = draw_pattern(img_text, masks, list_of_sets)

plt.figure()
plt.imshow(img_out)

