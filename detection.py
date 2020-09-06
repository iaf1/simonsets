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

img = 2461  # cv2 uses BGR

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to HSV
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale

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

edged = cv2.Canny(img_gray, 300, 550)

contours, hierarchy, _ = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#cv2.drawContours(img_gray, contours, -1, (0, 255, 0), 3)

plt.imshow(edged)
plt.show()