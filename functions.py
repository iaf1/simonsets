#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 19:33:31 2020

@author: ivan
edit: simon
"""
import numpy as np
import itertools as it

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

CHR_FILLS = {1: '□ ', 2: '⬔', 3: '■'}
CHR_SHAPES = {1: 'O', 2: '~', 3: '▭'}
CHR_COLORS = {1: 'R', 2: 'G', 3: 'B'}

#CHR_FILLS = {1: 'E', 2: 'H', 3: 'F'}
#CHR_SHAPES = {1: 'C', 2: 'W', 3: 'S'}
#CHR_COLORS = {1: 'R', 2: 'G', 3: 'B'}

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

'''
params = [[□, ⬔, ■], [R, G, B], [⬭, ～, ▭], [1, 2, 3]]'''
def is_set(inp):
    assert isinstance(inp, list) or isinstance(inp, np.ndarray)
    assert len(inp) == 3
    params1 = np.array([np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)])
    params2 = np.array([np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)])
    params3 = np.array([np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)])
    params1[0][inp[0].array[0] - 1] = 1
    params1[1][inp[0].array[1] - 1] = 1
    params1[2][inp[0].array[2] - 1] = 1
    params1[3][inp[0].array[3] - 1] = 1
    params2[0][inp[1].array[0] - 1] = 1
    params2[1][inp[1].array[1] - 1] = 1
    params2[2][inp[1].array[2] - 1] = 1
    params2[3][inp[1].array[3] - 1] = 1
    params3[0][inp[2].array[0] - 1] = 1
    params3[1][inp[2].array[1] - 1] = 1
    params3[2][inp[2].array[2] - 1] = 1
    params3[3][inp[2].array[3] - 1] = 1
    result = params1 + params2 + params3
    
    if not (result == 2).any():
        
        print('is a set')
        print('1st card: ')
        print('Number: {n} | Shape: {s} | Color: {c} | Filling: {f}'
              .format(c=inp[0].color, f=inp[0].fill, s=inp[0].shape, n=inp[0].amount))
        print('2nd card: ')
        print('Number: {n} | Shape: {s} | Color: {c} | Filling: {f}'
              .format(c=inp[1].color, f=inp[1].fill, s=inp[1].shape, n=inp[1].amount))
        print('3rd card: ')
        print('Number: {n} | Shape: {s} | Color: {c} | Filling: {f}'
              .format(c=inp[2].color, f=inp[2].fill, s=inp[2].shape, n=inp[2].amount))
        return True
    else:
        return False

def find_sets(board):
    
    assert isinstance(board, list) or isinstance(board, np.ndarray)

    list_of_sets = []
    
    board = np.array(board)
    
    indices = [i for i in range(len(board))]
    
    for three_indices in it.combinations(indices, 3):
        three = board[list(three_indices)]
        
        if is_set(three):
            list_of_sets.append(tuple(three_indices))
    
    return list_of_sets


example1 = [Card([3, 1, 1, 1]), Card([3, 1, 1, 2]), Card([3, 1, 1, 3])]
example2 = [Card([3, 1, 1, 1]), Card([3, 1, 1, 2]), Card([3, 1, 1, 2])]
is_set(example2)


        