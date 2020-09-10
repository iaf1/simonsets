#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 21:07:57 2020

@author: ivan
"""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cv2

orientations = [30, 150, 90, 0, 60, 120]

dd = 40

thickness = 8

def HEX2RGB(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

colors_hex = list(colors.TABLEAU_COLORS.values())
colors = [HEX2RGB(el) for el in colors_hex]

def draw_pattern(img, masks, idx_sets):
    
    out = img.copy()
    
    Y, X, Z = img.shape
    print('X: {}; Y: {}'.format(X, Y))
    
    masks = np.array(masks)
    
    for cur_idx_set in range(len(idx_sets)):
        
        col = colors[cur_idx_set]
                
        pattern = np.zeros_like(img)
        
        cur_set = list(idx_sets[cur_idx_set])
        
        cur_mask = np.uint8(np.sum(masks[cur_set], axis=0)/255)
        
        (i1, i2, i3) = cur_set
        ori = orientations[cur_idx_set]
        col = colors[cur_idx_set]
                
        theta = ori *np.pi / 180
        
        csc = 1/np.sin(theta)
        cot = 1/np.tan(theta)
        z1 = 0
        
        if ori < 90:
            while True:
                
                pt1 = (X - z1*dd*csc/cot, 0)
                pt2 = (X, z1*dd*csc)
                
                if pt1[0] <= 0: pt1 = (0, -X*cot + z1*dd*csc)
                if pt2[1] >= Y: pt2 = (X + (Y - z1*dd*csc)/cot, Y)
                                
                if pt1[1] > Y: break
            
                pt1 = (int(np.round(pt1[0])), int(np.round(Y-pt1[1])))
                pt2 = (int(np.round(pt2[0])), int(np.round(Y-pt2[1])))
                            
                cv2.line(pattern, pt1, pt2, col, thickness)
                
                z1+=1
            
        elif ori > 90:
            while True:
                
                pt1 = (0, z1*dd*csc)
                pt2 = (z1*dd*csc/cot, 0)
                
                if pt1[1] >= Y: pt1 = ((Y-z1*dd*csc)/cot, Y)
                if pt2[0] <= 0: pt2 = (X, X*cot + z1*dd*csc)
                                
                if pt2[1] > Y: break
            
                pt1 = (int(np.round(pt1[0])), int(np.round(Y-pt1[1])))
                pt2 = (int(np.round(pt2[0])), int(np.round(Y-pt2[1])))
                
                cv2.line(pattern, pt1, pt2, col, thickness)
                
                z1+=1
        
        rep_mask = np.dstack((cur_mask,)*3)
        masked_pattern = pattern * rep_mask
        
# =============================================================================
#         plt.subplots()
#         plt.subplot(311)
#         plt.imshow(pattern)
#         plt.subplot(312)
#         plt.imshow(rep_mask)
#         plt.subplot(313)
#         plt.imshow(masked_pattern)
#                 
#         plt.imshow(out)
# =============================================================================
        
        out = np.where(masked_pattern != 0, masked_pattern, out)
                    
    return out, masked_pattern


def put_text(img_rgb, board, boxes):
    from initSettings import cf
    from PIL import Image, ImageFont, ImageDraw
    from sys import platform

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
    
    for card, box in zip(board, boxes):
            ############################################################ PIL ###############
        draw.text((box[0, 0], box[0, 1]), card.chars(), cf.font_color, font=font) #
        ################################################################################
    
    return np.array(img_pil)
    
    
                    
#output = draw_pattern(np.zeros((2000, 1500, 3)), None, [(1,2,3)])

#plt.imshow(output)