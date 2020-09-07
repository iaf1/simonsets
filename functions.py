#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 19:33:31 2020

@author: ivan
"""

inv_dict = lambda dct: {v: k for (k, v) in dct.items()}

AMOUNTS = {1: 'one', 2: 'two', 3: 'three'}
SHAPES = {1: 'circle', 2: 'ondulated', 3:'square'}
COLORS = {1: 'red', 2: 'green', 3: 'blue'}
FILLS = {1: 'empty', 2: 'half', 3: ' full'}


INV_FILLS = inv_dict(FILLS)
INV_COLORS = inv_dict(COLORS)
INV_SHAPES = inv_dict(SHAPES)
INV_AMOUNTS = inv_dict(AMOUNTS)

CHR_FILLS = {1: '□ ', 2: '⬔', 3: '■'}
CHR_SHAPES = {1: '⬭', 2: '～', 3: '▭'}
CHR_COLORS = {1: 'R', 2: 'G', 3: 'B'}

class Card:
    def __init__(self, array):
        import numpy as np
        """ Array:
                [fill,   color,    shape,    amount]
                fill:   1 - empty
                        2 - half
                        3 - full
                color:  1 - red
                        2 - green
                        3 - blue
                shape:  1 - circle
                        2 - ondulated
                        3 - square
                amount: 1 - one
                        2 - two
                        3 - three
        """
        
        self.array = np.array(array)
        self.fill = FILLS.get(self.array[3])
        self.color = COLORS.get(self.array[2])
        self.shape = SHAPES.get(self.array[1])
        self.amount = AMOUNTS.get(self.array[0])
        
    def chars(self):
        return str(self.array[0]) + CHR_SHAPES.get(self.array[1],'') + CHR_COLORS.get(self.array[2],'') + CHR_FILLS.get(self.array[3],'')
    
def is_set(inp):
    assert isinstance(inp, list)
    assert len(inp) == 4
    
        