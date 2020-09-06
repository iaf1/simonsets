#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 19:33:31 2020

@author: ivan
"""

inv_dict = lambda dct: {v: k for (k, v) in dct.items()}
FILLS = {1: 'empty', 2: 'half', 3: ' full'}
COLORS = {1: 'red', 2: 'green', 3: 'blue'}
SHAPES = {1: 'circle', 2: 'ondulated', 3:'square'}
AMOUNTS = {1: 'one', 2: 'two', 3: 'three'}

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