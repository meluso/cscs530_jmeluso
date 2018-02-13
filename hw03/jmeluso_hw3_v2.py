###############################################################################
# Assignment:   Homework 3
# Author:       John Meluso
# Date:         2018-02-13
# Source:       Based on "Simple CA simulator in Python" by Hiroki Sayama,
#               Copyright 2008-2012 Hiroki Sayama, sayama@binghamton.edu.
# Description:  
#
#
###############################################################################


# Import libraries

    #Import matplotlib
    import matplotlib
    matplotlib.use('TkAgg')
    
    # Import pylab, random, and scipy
    import pylab as PL
    import random as RD
    import scipy as SP

# Initialize random seed
RD.seed()

# Specify world dimensions
width = 50
height = 50

def init():
    '''Function which initializes the world for Langton's Ant using the world
    dimensions specified above.'''
    
    # Declare global variables
    # - time, the iteration of the model
    # - config, the current configuration of the world
    # - nextConfig, the configuration of the world for the upcoming iteration
    #     of the simulation
    global time, config, nextConfig

    # Initialize model time
    time = 0
    
    # Initialize the state of the world
    config = SP.zeros([height, width])
    for x in xrange(width):
        for y in xrange(height):
            if RD.random() < initProb:
                state = 1
            else:
                state = 0
            config[y, x] = state

    nextConfig = SP.zeros([height, width])

def draw():
    PL.cla()
    PL.pcolor(config, vmin = 0, vmax = 1, cmap = PL.cm.binary)
    PL.axis('image')
    PL.title('t = ' + str(time))

def step():
    global time, config, nextConfig

    time += 1

    for x in xrange(width):
        for y in xrange(height):
            state = config[y, x]
            numberOfAlive = 0
            for dx in xrange(-1, 2):
                for dy in xrange(-1, 2):
                    numberOfAlive += config[(y+dy)%height, (x+dx)%width]
            if state == 0 and numberOfAlive == 3:
                state = 1
            elif state == 1 and (numberOfAlive < 3 or numberOfAlive > 4):
                state = 0
            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config

import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
