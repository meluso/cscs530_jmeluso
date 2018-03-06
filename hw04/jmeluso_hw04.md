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

The routines associated with the engineer are then to update the current estimate, update the predicted estimate, and to respond to a request for an estimate with the probability value mentioned in Section 2.1. Updating the current value, _**update current**_, will be to draw another value and calculate the mean and _population_ variance of the new set of samples. Likewise, updating the prediction, _**update predicted**_, will be to draw another value and calculate the mean and _sample_ variance of the new set of samples (using the sample to represent uncertainty bounds). When a value request, _**request estimate**_, is made from another agent, the engineer has a probability of delivering either the current or the predicted estimate (which I've seen in practice).

```python
class engineer():
    """An agent who is an engineer in an organization. S/he has a historical
    distribution of data, a current estimate, and a predicted estimate."""
    
    def __init__(self,hist_mean,hist_var):
        '''Initialize the engineer agent.'''
        
        # Historical mean and variance
        self.hist_mean = hist_mean
        self.hist_var = hist_var
        
        # Current samples, mean, and variance
        self.curr_samples = []
        self.curr_mean = []
        self.curr_var = []
        
        # Predicted samples, mean, and variance
        self.pred_samples = []
        self.pred_mean = []
        self.pred_var = []
        
        # Pick a random number to set the type of communication
        self.comm_type = rd.random()
        
    def update_current(self):
        '''Updates the agent's current estimate.'''
        
        # Draw a new sample from the historical distribution
        self.curr_samples.append(rd.gauss(self.hist_mean,self.hist_var))
        
        # Calculate the mean and variance of the samples
        self.curr_mean = st.mean(self.curr_samples)
        self.curr_var = st.pvariance(self.curr_samples)
        
    def update_predicted(self):
        '''Updates the agent's predicted estimate.'''
        
        # Draw a new sample from the historical distribution
        self.pred_samples.append(rd.gauss(self.hist_mean,self.hist_var))
        
        # Calculate the mean and variance of the samples
        self.pred_mean = st.mean(self.pred_samples)
        self.pred_var = st.variance(self.pred_samples,self.pred_mean)

    def request_estimate(self):
        
        # Return a value based on the communication probability
        if comm_prob > self.comm_type:
            return self.curr_mean
        else:
            return self.pred_mean
```

#### 2.2.2. The Integrator

The second type of agent is an integrator role. Their responsibilities are to pass the request for information from a superior to their direct reports, and to aggregate the responses of those direct reports to pass to their supperior. So the routines herein are to _**receive request**_ and _**make request**_. The variables for the agent are then a list of **children** (nodes) which report to this integrator, a **received estimates** list containing the estimates that the agent receives, and an **aggregate estimate** variable which is a sum of the received estimates to pass upward.

```python
class integrator():
    """An agent who is responsible for passing communication from superiors
    to inferiors and who is then responsible for receiving and aggregating
    the estimates passed to it by its inferior agents."""
    
    def __init__(self,children):
        '''Initialize the integrator agent'''
        
        # Contains list of child nodes
        self.children = children
        
        # Estimate list and aggregated value
        self.est_list = []
        self.est_agg = []
        
        
    def receive_request(self):
        '''Receive estimate request from from superior and return the
        estimate value.'''
        
        # Reset estimate list
        self.est_list = []
        
        # Now that a request has been received, place a request to children
        self.est_list = self.request_estimates

        # Sum elements of estimate list
        self.est_agg = sum(self.est_list)        
                
        # Return the aggregated estimate
        return self.est_agg

        
    def request_estimates(self):
        '''Pass communication request to inferior'''

        # Place request of child nodes
        for ch in self.children:
            self.est_list.append(ch.request_estimate)
```

#### 2.2.3. The Manager

The final agent type is a manager. The manager is a special type of integrator who only _**places request**_ for communiation and _**aggregates estimates**_. Its variables are just the a **received estimates** list containing the estimates that the agent receives and an **aggregate estimate** variable which is a sum of the received estimates.

```python
class manager():
    """An agent who is responsible for placing requests to inferiors
    and who is then responsible for receiving and aggregating
    the estimates passed to it by its inferior agents."""
    
    def __init__(self,children):
        '''Initialize the integrator agent'''
        
        # Contains list of child nodes
        self.children = children
        
        # Estimate list and aggregated value
        self.est_list = []
        self.est_agg = []
        
        
    def place_request(self):
        '''Receive estimate request from from superior and return the
        estimate value.'''
        
        # Reset estimate list
        self.est_list = []
        
        # Now that a request has been received, place a request to children
        self.est_list = self.request_estimates

        # Sum elements of estimate list
        self.est_agg = sum(self.est_list)        
                
        # Return the aggregated estimate
        return self.est_agg

        
    def request_estimates(self):
        '''Pass communication request to inferior'''

        # Place request of child nodes
        for ch in self.children:
            self.est_list.append(ch.receive_request)
```

&nbsp; 

### 2.3. Action and Interaction 
*****
 
**_Interaction Topology_**

_Description of the topology of who interacts with whom in the system. Perfectly mixed? Spatial proximity? Along a network? CA neighborhood?_
 
**_Action Sequence_**

_What does an agent, cell, etc. do on a given turn? Provide a step-by-step description of what happens on a given turn for each part of your model_

1. Step 1
2. Step 2
3. Etc...

&nbsp; 
### 2.4. Model Parameters and Initialization
*****

_Describe and list any global parameters you will be applying in your model._

_Describe how your model will be initialized_

_Provide a high level, step-by-step description of your schedule during each "tick" of the model_

&nbsp; 

### 2.5. Assessment and Outcome Measures
*****

_What quantitative metrics and/or qualitative features will you use to assess your model outcomes?_

&nbsp; 

### 2.6. Parameter Sweep
*****

_What parameters are you most interested in sweeping through? What value ranges do you expect to look at for your analysis?_
