John Meluso, HW 3, Due 2/20/18

# Homework 3 writeup

## Problem 1
For this problem, please see the code "jmeluso_hw3_submission.py". The source file, based on the game of life PyCX file, is "jmeluso_hw3_source.py", but is not the code I actually created for the class. I also used some of the logic from the ants-abm in PyCX, too.

I implemented the model using the agent-based method rather than the grid-based method. I began using the grid-based method via the game of life PyCX model, but eventually decided that it would be easier to just embed the functions in the agent/ant/termite itself to create a world and sequence of events which executed upon an input world. The ant then returned an output world (variable "world_next") which updates the world displayed on the board. I chose not to graphically display the ant because I figured it was more trouble than it was worth when the most important thing for me personally was understanding not the graphical display in the world but correctly creating the class of the agent and the functions for the agent. My own models will tend not to incorporate spatial distributions as they're more network-centered.

Here's an example of the model I created with a board size of 50:

![Board of 50 before 10000](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig1.png)

I knew there would be constraints on the formation of the "highway" after 10,000 steps--like when the ant ran back into its own path when wrapping around in such a small world--so it wasn't surprising that upon reaching 10,000 steps, rather than seeing the formation of a highway, it continued to create "random" (not random, but not visibly ordered, either) paths. The next image shows an example post-10,000 steps:

![Board of 50 after 10000](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig2.png)

I set the board to wrap using the "position mod width" method we saw in class a few lessons ago because, again unsurprisingly, the model stopped running and threw an error when the ant reached and tried to go off the edge of the board. The matrix containing the 1's and 0's of the board is a fixed size of non-negative integers, so setting a negative position didn't make sense. Adding the mod feature cleared that up. I haven't played with it much, but it seems like creating fixed edges to the board will require more logic changes to the code and decisions about how the agent should respond.

I was able to get the highway to form when I expanded the board to 100, shown in the image below. When I expanded the board to 250, PyCX and Spyder would freeze, though, presumably due to computational complexity. I'd have to find a way to simplify the model if I wanted to keep generating it at larger scales while displaying live.

![Board of 100 after 10000](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig3.png)

## Problems 2 & 3

Part of my choice to use agents instead of the grid-method was in anticipation of this problem, because creating new instances of agents in OO programming is easy enough. The image below shows an example with 2 ants on the 100-size board:

![2 agents before 10000](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig4.png)

Both agents started to create paths which were symmetric to one another, as expected from a model which uses identical rules. When the agents started far enough apart from each other, both began to create highways:

![2 agents after 10000](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig5.png)

In this particular run, they both ran into each other and began to retrace the highways they'd created! Shown here:

![2 agents retrace](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig6.png)

When the agents started closer together, they ran into each other before they could begin to create their "10,000 highways":

![2 agents collide early](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig7.png)

In this case, they didn't create highways. However, they did begin to retrace their steps exactly at one point and eventually returned to their original positions after undoing everything they'd done:

![2 agents collide later on](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig8.png)
![2 agents collide a lot later on](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig9.png)

Perhaps a property of these two-agent examples is that after colliding, they eventually retrace their steps back to the original position and start again. From all of the models I've run so far, that seems to be the case, an emergent oscillating behavior which depends on when the agents interact with each other's path. In the case I showed before, they eventually performed a 180-degree rotated version of what they'd done previously and presumably would continue in these oscillatory patterns thereafter.

![2 agents collide way, way later](https://github.com/meluso/cscs530_jmeluso/blob/master/hw03/hw3_images/jmeluso_hw3_fig10.png)
