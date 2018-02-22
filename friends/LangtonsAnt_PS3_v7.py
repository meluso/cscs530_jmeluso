# Simple CA simulator in Python
#
# *** Game of Life Rule ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

RD.seed()
width = 50
height = 50
directions = ["North","East","South","West"]
forward = [[0,1],[1,0],[0,-1],[-1,0]]
left = ["West","North","East","South"]
right = ["East","South","West","North"]


def init():
    global time, grid, x, y, dir, width, height
    time = 0
    dir = directions[0]
    grid = SP.zeros([height, width])
    x=width/2
    y=height/2

def draw():
    PL.cla()
    PL.pcolor(grid, vmin = 0, vmax = 1, cmap = PL.cm.binary)
    PL.axis('image')
    PL.title('t = ' + str(time))

def step():
    global time, grid, x, y, dir, state
    time += 1
    
    # Determine actions based on color
    if grid[y,x] == 1:
        
        # Change the direction ant is facing
        dir = left[directions.index(dir)]
        
        # Change cell from white to black
        grid[y,x] = 0
    
    else:
                
        # Change the direction ant is facing
        dir = right[directions.index(dir)]
        
        # Change cell from white to black
        grid[y,x] = 1
        
    # Move forward
    x += forward[directions.index(dir)][1]
    y += forward[directions.index(dir)][0]
    

import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
