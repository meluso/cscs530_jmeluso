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


def init():
    global time, config, dx, dy, dir
    time = 0
    config = SP.zeros([height, width])
    dx = 25
    dy = 25
    dir = [0,1]

def draw():
    PL.cla()
    PL.pcolor(config, vmin = 0, vmax = 1, cmap = PL.cm.binary)
    PL.axis('image')
    PL.title('t = ' + str(time))

def step():
    global time, config, dx, dy, dir, state
    time += 1
    state = config[dy,dx]
    
    if state == 0:
        if dir == [0,1]:
           state = 1
           dx = (dx-1)%50
           dir = [-1,0]
           
        elif dir == [-1,0]:
           state = 1
           dy = (dy-1)%50
           dir = [0,-1]

        elif dir == [0,-1]:
           state = 1
           dx = (dx+1)%50
           dir = [1,0]
           
        else:
           state = 1
           dy = (dy+1)%50
           dir = [1,0]
           
    else:
        if dir == [0,1]:
           state = 0
           dx = (dx+1)%50
           dir = [1,0]
           
        elif dir == [-1,0]:
           state = 0
           dy = (dy+1)%50
           dir = [0,-1]
           
        elif dir == [0,-1]:
           state = 0
           dx = (dx-1)%50
           dir = [-1,0]
           
        else:
           state = 0
           dy = (dy-1)%50
           dir = [0,1]
        
        

    config[dy,dx] = state 
    print dx
    print dy
    print config[dy,dx]

import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
