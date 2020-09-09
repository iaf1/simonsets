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

from PIL import Image, ImageFont, ImageDraw
from matplotlib import cm

img = cv2.imread('full_image.jpeg')  # cv2 uses BGR

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to HSV
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale

############################################################################ PIL #
img_pil = Image.fromarray((img_rgb).astype(np.uint8))                     ##
draw = ImageDraw.Draw(img_pil)                                                  ##
font = ImageFont.truetype('arial.ttf',40) ##
##################################################################################

# Then we define the color thresholds in the HSV space

low_red = np.array([161, 80, 100])
high_red = np.array([179, 255, 255])
red_mask = cv2.inRange(img_hsv, low_red, high_red)

low_green = np.array([40, 100, 100])
high_green = np.array([90, 255, 255])
green_mask = cv2.inRange(img_hsv, low_green, high_green)

low_blue = np.array([110, 100, 50])
high_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)

# We apply a Canny edge detector

edges = cv2.Canny(img_gray, 200, 500)

# We find the contours


contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

masks = []
board = []


cv2.drawContours(img_gray, contours, -1, 255, thickness=5)

for idx in range(len(contours)):
    #print(idx)
    mask = np.zeros_like(img_gray) # Create mask where white is what we want, black otherwise
    
    cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask
    mask2 = mask.copy()
        
    perc_nonzero = np.count_nonzero(mask) / (mask.shape[0]*mask.shape[1])
    
    if perc_nonzero < 0.01: continue

    out = np.zeros_like(img) # Extract out the object and place into output image
    out[mask == 255] = img[mask == 255]
    
    rect = cv2.minAreaRect(contours[idx])
    box = cv2.boxPoints(rect)

    # Show the output image
    cv2.imshow('Output', cv2.resize(out, (750, 1000)))
    tup_props = classification(out)
    num, shape, col, fil = tup_props
    print('Number: {n} | Shape: {s} | Color: {c} | Filling: {f}'.format(c=COLORS[col], f=FILLS[fil], s=SHAPES[shape], n=str(num)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    board.append(Card(tup_props))
    masks.append(mask)

    ############################################################ PIL #
    draw.text((box[0, 0], box[0, 1]), board[-1].chars(), (255, 0, 255), font=font)
    ##################################################################

img_text = np.array(img_pil)
plt.figure()
plt.imshow(img_text)

list_of_sets = []
for ii in range(len(board)-2):
    for iii in range(len(board)-2-ii):
        for iv in range(len(board)-2-ii-iii):
            selected = [board[ii], board[ii + iii + 1], board[ii + iii + iv + 2]]
            result = is_set(selected)
            if result is True:
                list_of_sets.append([ii, iii, iv])

print(list_of_sets)
plt.show()

