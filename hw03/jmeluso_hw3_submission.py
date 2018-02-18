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
global size, width, height
size = 100
width = size
height = size

def init():
    '''Function which initializes the world for Langton's Ant using the world
    dimensions specified above.'''
    
    # Declare global variables
    # - time, the iteration of the model
    # - world, the current configuration of the world
    # - agent, the actor which will move through and act upon the world, in
    #     this case, the ant/turmite.
    # - direction, the vector specifying the direction in which the ant is
    #     facing during that turn and the direction in which the ant will step.
    global time, world, ant, ant2, direction
    
    # Initialize the world time
    time = 0
    
    # Initialize the world map with randomly distributed states
    world = SP.zeros([height, width])
    
    # Create the agent
    ant = agent([RD.randint(0,width),RD.randint(0,height)],0)
    ant2 = agent([RD.randint(0,width),RD.randint(0,height)],0)

class agent():    
    # Initialize the agent at the origin with its direction
    
    def __init__(self,position,orientation):
        """Initialize agent attributes"""
        self.x = position[0]
        self.y = position[1]
        self.orientation = orientation
        
    def execute(self,world):
        """Perform all of the steps for the agent: (1) change color of current 
        position, (2) change orientation based on color, and (3) move position
        on orientation."""
        world_next = self.change_color(world)
        self.turn(world)
        self.move_position()
        return world_next
        
    def change_color(self,world):
        """Change the color of the current position in the world to black if
        white and to white if black."""
        world_next = world
        if world[self.x,self.y] == 0:
            world_next[self.x,self.y] = 1
        else:
            world_next[self.x,self.y] = 0
        return world_next
    
    def turn(self,world):
        """If the cell is white/1, turn left. If the cell is black/0, turn
        right."""
        print(self.orientation)
        if world[self.x,self.y] == 1: # white
            if self.orientation == 0:
                self.orientation = 3
            else:
                self.orientation -= 1
        else: # black
            if self.orientation == 3:
                self.orientation = 0
            else:
                self.orientation += 1
    
    def move_position(self):
        """Move one in the direction of the current orientation."""
        if self.orientation == 0:
            # move East [0,1]
            self.y += 1
        elif self.orientation == 1:
            # move South [-1,0]
            self.x += -1
        elif self.orientation == 2:
            # move West [0,-1]
            self.y += -1
        else:
            # move North [1,0]
            self.x += 1
        
        # Wrap the world if values are above 50 or below 0.
        self.x = self.x % width
        self.y = self.y % height

def draw():
    PL.cla()
    PL.pcolor(world, vmin = 0, vmax = 1, cmap = PL.cm.binary)
    PL.axis('image')
    PL.title('t = ' + str(time))

def step():
    
    # Import global variables
    global time, world, ant, ant2
    
    # Increment time counter
    time += 1
    
    #   Perform ant actions:
    #   - if ant is on black, the ant turns right & changes cell to white
    #       elif ant is on black, the ant turns right & changes cell to black
    #   - ant moves forward one
    world = ant.execute(world)
    world = ant2.execute(world)


import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
