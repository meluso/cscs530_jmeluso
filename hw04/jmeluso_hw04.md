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

&nbsp;  

## 2. Model Outline
### 2.1. Environment
*****

This model does not include a spatial component as the phenomena of interest are related to behavioral decision making and sociological dynamics related to information exchange. Sections 2.2 (Agents) and 2.3 (Action and Interaction), respectively, will describe the model's characterization of these phenomena. However, there are still a handful of properties associated with the world such as the time, communication probability, network structure, etc. Those will be covered further in the following sections.

&nbsp;  

### 2.2. Agents
****

_Note: In advance, I recognize that I will have to synchronize the functions for the agents so that agents can call the same function from different types of agents. I'm not there yet...but I'll get there._

#### 2.2.1. The Engineer

The first type of agent in this model will be engineers in a design organization. Each engineer has a part for which they are responsible and which can be modeled jointly as a property of the agent to simplify the model. Then the agent will have several properties associated with the part, the first of which are the **historical mean** and **historical variance**. The agent will have two values representing historical information about previous parts which represent their knowledge of education, past designs, and previous work experience. To design a new part for the new system, the agent will sample from the historical distribution of the mean and variance as a random variable. The agent will populate a **current mean** and **current variance** representing the mean of all samples drawn for the current design and the variance of the samples drawn for the current design, respectively. The agent will also draw samples for a **predicted mean** by drawing from the same historical distribution.

The routines associated with the engineer are then to update the current estimate, update the predicted estimate, and to respond to a request for an estimate with the probability value mentioned in Section 2.1. Updating the current value, _**update current**_, will be to draw another value and calculate the mean and _population_ variance of the new set of samples. Likewise, updating the prediction, _**update predicted**_, will be to draw another value and calculate the mean and _sample_ variance of the new set of samples (using the sample to represent uncertainty bounds). When a value request, _**request estimate**_, is made from another agent, the engineer has a probability of delivering either the current or the predicted estimate (which I've seen in practice) based on a randomly-determined **communication type** variable.

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

The interactions topology will be a balanced tree network using NetworkX with a height of 6 and down degree of 7 for each node prior to the 6th level. The 1st level (1 agent) will be an instance of the manager class (a class I'm developing for future potential of modeling different organizational structures). The next levels (2-5) will be integrators. The final level (6) will be all engineers.

**_Action Sequence_**

Each turn, the manager will place a request for information from the system integrators, who will go down to the next integrator, and the next integrator, and the next integrator, and finally down to the engineer. The engineer's information will then get passed back up the chain to the manager. At a more granular level:

1. Manager uses _**place_request**_ with each child node.
2. Integrators _**receive_request**_ from parent node
3. Integrators _**request_estimates**_ from each child node
4. Engineers receive _**request_estimate**_ command and return estimate (either current or prediction) as determined probabilistically.
5. Integrators finish _**receive request**_ by returning sum of inputs from child nodes.
6. Manager finishes _**place_request**_ by calculating sum of inputs from child nodes,. 

&nbsp;

### 2.4. Model Parameters and Initialization
*****

My global parameters will be a timer, a network structure as described above, and a random value **comm_prob** which will be the probability of the agents interpreting the request for communication as either a request for the currest value of the design or the predicted value of the design. The model will also initialize all of the agents (_this piece not yet created in code below_)

```python
def init():
    global time, comm_prob, network
    
    # Initialize model time
    time = 0
    
    # Declare the universal probability of effective communication
    comm_prob = rd.random()
    
    # Create the network of agents
    network = nx.balanced_tree(7,6)
```   
During each tick of the model, the engineers will all update their current and predicted estimates. The manager then requests estimates from all child agents, a request which cascades down through the integrators to the engineers, and back up with values via the integrators to the manager. The model will then store the system estimate at each point in time along with the statistics of all agents for later assessment, as discussed in Section 2.5 below.

&nbsp; 

### 2.5. Assessment and Outcome Measures
*****

The model will store the system estimate and variance, each agent's current estimate and variance, and predicted estimate and variance. As theoretical examples, pure current and predicted estimates (means and variances) will be calculated for each model iteration. The script will then subtract the modeled value from each of the current and predicted estimates individually to measure the difference between "perfect" and "imperfect" communication. I will also graphically plot the pure current, pure predicted, and actual returned estimate values at each iteration of the model to see if that reveals any other metrics I should use to assess the model's evolution. While my initial objective is to assess the degree to which different probabilities of binary options for miscommunication affect system performance, other characteristics may certainly emerge.

&nbsp; 

### 2.6. Parameter Sweep
*****

I'm interested in sweeping the **comm_prob** randomly-determined variable because it will vary the degree to which contributers provide current-valued estimates vs. prediction estimates. So at one probabilitiy extreme (eg. 0), the results should capture the design's fluctuations and uncertainty while at the other extreme (eg. 1) the results should capture the design's likely outcome including the sample variance as a more accurate measure of uncertainty. In my own studies, it appears that about 50% of the population is doing each method, so I'd like to see what happens at that point as well. My prediction is that there will be greater variance when both methods are used equally than with either pure method. All of that said, I plan to sweep **comm_prob** from 0 to 1 in increments either of 0.1 or 0.01 to see if there are any points at which the estimate significantly improves or degrades. I'll run a Monte Carlo simulation with 1000 runs for each probability value and calculate the mean and variance of results to assess the average system performance for different communication method probabilities.

&nbsp;  

## 3. Model Improvements & Next Steps

I'm aware that there's a lot left to be done for both documentation and building of the model. For one, I should probably find a way to either consolidate to a single agent class or a more universal set of agent routines at the very least. I'd also like to find a way to represent miscommunication at each step throughout the process. That may require creating current and predicted values for the integrators as well as the engineers to make the model more realistic. Also realistic is the clustering of knowledge, where certain branches of the tree may have one belief while others have different beliefs.

I'm also concerned that I haven't given enough autonomy to the agents, and that's something I'd like feedback on. While each individual agent technically uses a random value to determine communication strategy, I'm concerned that this model isn't representative enough of real contexts. Perhaps to be more specific, I'd love to build a platform which my lab and I can use for general application of social and engineering phenomena. As I work through this problem, I'm recognizing that a significant amount of work would need to go into constructing an accurate engineering model of a system in order for that to happen. I'd need to use a specific case like the canonical "FireSat" example from the "aerospace Bible", Space Mission Analysis & Design. I may try to make the final model more representative of such a system, but I'm not sure it will provide any advantages in terms of assessing the effects of social dynamics in organizations on organization or system performance which a more generic model couldn't achieve. More generic structures would also allow for greater flexibility with network structures, so I'm leaning toward a more generic model at this point.

&nbsp;
