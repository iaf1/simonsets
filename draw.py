#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 21:07:57 2020

@author: ivan
"""

from matplotlib import colors

orientations = [30, 150, 90, 0, 60, 120]

def HEX2RGB(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

colors_hex = list(colors.TABLEAU_COLORS.values())
colors = [HEX2RGB(el) for el in colors_hex]

def draw_pattern(img, masks, idx_sets):
    for cur_set in range(len(idx_sets)):
        (i1, i2, i3) = idx_sets[cur_set]
        ori = orientations[cur_set]
        col = colors[cur_set]
        