#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 12:07:22 2020

@author: ivan
"""

parameters = {"URL"                 : "http://192.168.0.66:8080/shot.jpg",
              
              # any contour that has less than this is not considered a card
              'thresh_card_perc'    : 0.01,
              
              # ellipses and rectangles must mach an amount larger than this with the fitted template
              'thresh_shape_match'  : 0.9,
              
              # treshold empty - half
              'thresh_low' : 0.05,
              
              # threshold half - full
              'thresh_high' : 0.9,
              
              # fonts (different OS)
              'font_path_win'       : 'aria.ttf',
              'font_path_lin'       : '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
              
              # font size
              'font_size'           : 40,
              
              # show cards individually
              'show_cards'          : False,
              
              'font_color'          : (255,255,255),
              
              }
              