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

## Problem 2

