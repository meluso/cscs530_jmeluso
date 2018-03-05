# Model Proposal for Simulating Miscommunication in Complex Engineered System Design

John Meluso

* Course ID: CMPLXSYS 530,
* Course Title: Computer Modeling of Complex Systems
* Term: Winter, 2018

## 1. Introduction
### 1.1. Goal 
*****
 
_Provide a short, 1-3 sentence description of the goal of your model_

The objective of this model is to simulate the effects of networked miscommunication between members of a design team on the resulting complex engineered system's performance. The model will simulate miscommunication between team members about the definition of a design parameter's "estimate" -- a phenomena identified through more than 100 interviews with practicing engineers in a real-world complex engineered system design context -- and the resulting value of that parameter at the end of the system design process.

&nbsp;  
### 1.2. Justification
****
_Short explanation on why you are using ABM_

Systems engineering methods generally apply top-down approaches to system technical design and organization management. But while systems methods effectively manage the technical systems, they incorrectly assume that organizations of people function as unbiased actors thereby neglecting known cognitive heuristics and social dynamics. (Meluso & Austin-Breneman, 2017) One of the most effective ways to demonstrate to engineering researchers and practitioners that cognitive heuristics and social dynamics have costly effects on system performance is by modeling behavioral phenomena that those researchers and practitioners _know_ to be true from their own experiences. Agent-based modeling helps engineers link social behaviors to technical elements and shows the aggregate effects of those bottom-up behavioral phenomena on a system's technical performance.

&nbsp; 
### 1.3. Main Micro-level Processes and Macro-level Dynamics of Interest
****

_Short overview of the key processes and/or relationships you are interested in using your model to explore. Will likely be something regarding emergent behavior that arises from individual interactions_

This model will simulate the micro-level process of communication wherein individuals will receive requests for information and with some probability provide either the requested piece of information or a different piece of information. The model will then aggregate those micro-level decisions by representing those decisions as summed elements of a larger design process. At the system-level, I'm curious to see whether there are any phenomena associated with varying probabilities of communicative effectiveness and how they affect system performance, both absolute and variability.

#### 1.3.1. Micro-level Processes

The micro-level processes of this model will be those of decision making within an agent and how the agent exchanges information with other agents. Agents will have a reporting structure through which they will receive requests for information. When they receive a request for information, the agent will have a (parameter-determined and -swept) probability of interpreting the request in one of two possible formsI'm interested in exploring the spread of design estimate uncertainty resulting from system miscommunication and reduction in system performance consequential to 

## 2. Model Outline
****
&nbsp; 
### 2.1. Environment
_Description of the environment in your model. Things to specify *if they apply*:_

* _Boundary conditions (e.g. wrapping, infinite, etc.)_
* _Dimensionality (e.g. 1D, 2D, etc.)_
* _List of environment-owned variables (e.g. resources, states, roughness)_
* _List of environment-owned methods/procedures (e.g. resource production, state change, etc.)_

This model does not include a spatial component as the phenomena of interest are related to behavioral decision making and sociological dynamics related to information exchange. Sections 2.2 (Agents) and 2.3 (Action and Interaction), respectively, will describe the model's characterization of these phenomena.

```python
# Include first pass of the code you are thinking of using to construct your environment
# This may be a set of "patches-own" variables and a command in the "setup" procedure, a list, an array, or Class constructor
# Feel free to include any patch methods/procedures you have. Filling in with pseudocode is ok! 
# NOTE: If using Netlogo, remove "python" from the markdown at the top of this section to get a generic code block
```

### 2.2. Agents
 
 _Description of the "agents" in the system. Things to specify *if they apply*:_
 
* _List of agent-owned variables (e.g. age, heading, ID, etc.)_
* _List of agent-owned methods/procedures (e.g. move, consume, reproduce, die, etc.)_

The first type of agent in this model will be engineers in a design organization. Each engineer has a part for which they are responsible and which can be modeled jointly as a property of the agent to simplify the model. Then the agent will have several properties associated with the part, the first of which is a *Historical mean*: The agent will have a value representing historical information about previous parts of that 

The second type of agent is a manager. 

the model will include an external element, the "program manager", who will make regular requests for information and aggregate the agents' information into a system.

```python
# Include first pass of the code you are thinking of using to construct your agents
# This may be a set of "turtle-own" variables and a command in the "setup" procedure, a list, an array, or Class constructor
# Feel free to include any agent methods/procedures you have so far. Filling in with pseudocode is ok! 
# NOTE: If using Netlogo, remove "python" from the markdown at the top of this section to get a generic code block
```

&nbsp; 

### 2.3. Action and Interaction 
 
**_Interaction Topology_**

_Description of the topology of who interacts with whom in the system. Perfectly mixed? Spatial proximity? Along a network? CA neighborhood?_
 
**_Action Sequence_**

_What does an agent, cell, etc. do on a given turn? Provide a step-by-step description of what happens on a given turn for each part of your model_

1. Step 1
2. Step 2
3. Etc...

&nbsp; 
### 2.4. Model Parameters and Initialization

_Describe and list any global parameters you will be applying in your model._

_Describe how your model will be initialized_

_Provide a high level, step-by-step description of your schedule during each "tick" of the model_

&nbsp; 

### 2.5. Assessment and Outcome Measures

_What quantitative metrics and/or qualitative features will you use to assess your model outcomes?_

&nbsp; 

### 2.6. Parameter Sweep

_What parameters are you most interested in sweeping through? What value ranges do you expect to look at for your analysis?_
