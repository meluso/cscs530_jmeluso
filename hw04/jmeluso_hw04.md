# Model Proposal for Simulating Miscommunication in Complex Engineered System Design

John Meluso

* Course ID: CMPLXSYS 530,
* Course Title: Computer Modeling of Complex Systems
* Term: Winter, 2018

## 1. Introduction
### 1.1. Goal 
*****

The objective of this model is to simulate the effects of networked miscommunication between members of a design team on the resulting complex engineered system's performance. The model will simulate miscommunication between team members about the definition of a design parameter's "estimate" -- a phenomena identified through more than 100 interviews with practicing engineers in a real-world complex engineered system design context -- and the resulting value of that parameter at the end of the system design process.

&nbsp;  
### 1.2. Justification
****

Systems engineering methods generally apply top-down approaches to system technical design and organization management. But while systems methods effectively manage the technical systems, they incorrectly assume that organizations of people function as unbiased actors thereby neglecting known cognitive heuristics and social dynamics. (Meluso & Austin-Breneman, 2017) One of the most effective ways to demonstrate to engineering researchers and practitioners that cognitive heuristics and social dynamics have costly effects on system performance is by modeling behavioral phenomena that those researchers and practitioners _know_ to be true from their own experiences. Agent-based modeling helps engineers link social behaviors to technical elements and shows the aggregate effects of those bottom-up behavioral phenomena on a system's technical performance.

&nbsp; 
### 1.3. Main Micro-level Processes and Macro-level Dynamics of Interest
****

This model will simulate the micro-level process of communication wherein individuals will receive requests for information and with some probability provide either the requested piece of information or a different piece of information. The model will then aggregate those micro-level decisions by representing those decisions as summed elements of a larger design process. At the system-level, I'm curious to see whether there are any phenomena associated with varying probabilities of communicative effectiveness and how they affect system performance, both absolute and variability.

## 2. Model Outline
****
&nbsp; 
### 2.1. Environment
*****
_Description of the environment in your model. Things to specify *if they apply*:_

* _Boundary conditions (e.g. wrapping, infinite, etc.)_
* _Dimensionality (e.g. 1D, 2D, etc.)_
* _List of environment-owned variables (e.g. resources, states, roughness)_
* _List of environment-owned methods/procedures (e.g. resource production, state change, etc.)_

This model does not include a spatial component as the phenomena of interest are related to behavioral decision making and sociological dynamics related to information exchange. Sections 2.2 (Agents) and 2.3 (Action and Interaction), respectively, will describe the model's characterization of these phenomena. However, there are still a handful of properties associated with the world such as the time, communication probability, network structure, etc. Those will be covered further in the following sections.

```python
# Include first pass of the code you are thinking of using to construct your environment
# This may be a set of "patches-own" variables and a command in the "setup" procedure, a list, an array, or Class constructor
# Feel free to include any patch methods/procedures you have. Filling in with pseudocode is ok! 
# NOTE: If using Netlogo, remove "python" from the markdown at the top of this section to get a generic code block
```

### 2.2. Agents
****
 _Description of the "agents" in the system. Things to specify *if they apply*:_
 
* _List of agent-owned variables (e.g. age, heading, ID, etc.)_
* _List of agent-owned methods/procedures (e.g. move, consume, reproduce, die, etc.)_

#### 2.2.1. The Engineer

The first type of agent in this model will be engineers in a design organization. Each engineer has a part for which they are responsible and which can be modeled jointly as a property of the agent to simplify the model. Then the agent will have several properties associated with the part, the first of which are the **historical mean** and **historical variance**. The agent will have two values representing historical information about previous parts which represent their knowledge of education, past designs, and previous work experience. To design a new part for the new system, the agent will sample from the historical distribution of the mean and variance as a random variable. The agent will populate a **current mean** and **current variance** representing the mean of all samples drawn for the current design and the variance of the samples drawn for the current design, respectively. The agent will also draw samples for a **predicted mean** by drawing from the same historical distribution.

The routines associated with the engineer are then to _**update current**_ estimate, _**update predicted**_ estimate, and to respond to a _**request value**_ made of them with the probability value mentioned in Section 2.1. Updating the current value will be to draw another value and calculate the mean and _population_ variance of the new set of samples. Likewise, updating the prediction will be to draw another value and calculate the mean and _sample_ variance of the new set of samples (using the sample to represent uncertainty bounds). When a value request is made from another agent, the engineer has a probability 

#### 2.2.2. The Integrator


#### 2.2.3. The Manager

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
