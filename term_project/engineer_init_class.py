# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-02-18

This file initializes a model with the class engineer.

"""
import matplotlib as mp
import matplotlib.pyplot as plt
mp.use('TkAgg')

#import pylab as pl
import time
import math as mt
import numpy as np


def init(br_fac = 7):
    '''Initializes the model with the time, communication probability, and
    estimate preference offset global variables. It then initializes a set of
    agents given by the input to the function via a branching factor which
    defaults to 7, a estimate offset preference which defaults to 0, and a
    communication probability offset which defaults to 0.'''
    global comm_prob, offset, ag_net, a1, a2, a3, a4, a5, a6, a7, s1
    
    # Initialize global variables

    
def monte_carlo():
    '''Performs a Monte Carlo simulation on a network of engineer agents. This
    model sweeps the parameters 'offset' and 'comm_prob' for a given network
    configuration. The model executes 1000 times for each parameter combination
    using full factorial sampling.'''
    
    comm_prob = np.linspace(0,1,21) # Declare the universal probability of effective communication
    offset = np.linspace(-1,1,21) # Declare the universal offsets for the agents
    
    num_runs = 1000 # Number of runs for each parameter combination
    num_steps = 10 # Number of time steps to take in each model run
    
    # Create a matrix to store system values across runs
    sys_est = np.empty([len(comm_prob),len(offset),num_runs]) # system estimates
    sys_var = np.empty([len(comm_prob),len(offset),num_runs]) # system variance
    sys_util = np.empty([len(comm_prob),len(offset),num_runs]) # system utility
    
    # Perform num_runs number of runs for each combination of parameters
    start_time = time.time()
    per_comp = (len(comm_prob)*len(offset))
    run_num = 0
    for i in range(len(comm_prob)):
        for j in range(len(offset)):
            run_num += 1
            for k in range(num_runs):
                
                # Initialize the model for the run
                a1 = engineer(offset[j],comm_prob[i])
                a2 = engineer(offset[j],comm_prob[i])
                a3 = engineer(offset[j],comm_prob[i])
                a4 = engineer(offset[j],comm_prob[i])
                a5 = engineer(offset[j],comm_prob[i])
                a6 = engineer(offset[j],comm_prob[i])
                a7 = engineer(offset[j],comm_prob[i])
                s1 = engineer(offset[j],comm_prob[i],[a1,a2,a3,a4,a5,a6,a7]) 
                
                # Perform num_steps number of time steps during each model iteration
                for t in range(num_steps):
                    s1.give_est()
            
                # Save results of test to that spot in matrix
                #sub_var.append(np.var([a1.est_mean,a2.est_mean,a3.est_mean,a4.est_mean,a5.est_mean,a6.est_mean,a7.est_mean]))
                sys_est[i,j,k] = s1.est_mean[-1]
                sys_var[i,j,k] = s1.est_var[-1]
                sys_util[i,j,k] = s1.est_util[-1]
        
            lap_time = (time.time() - start_time)/60
            run_count = run_num
            print '%.2f minutes elapsed, %d of %d iterations complete' % (lap_time,run_count,per_comp)
        
    return [comm_prob,offset,sys_est,sys_var,sys_util]

################################################################################    
# This section defines the class engineer and its subfunctions.
#
#   class - engineer(offset=0,comm_prob=0,contributors=[])
#       def - init(self,offset=0,comm_prob=0,contributors=[])
#       def - repr(self)
#       def - calc_util(self,value)
#       def - adj_util()
#       def - gen_hist()
#       def - give_hist()
#       def - give_est()
#       def - update_est()
#    
################################################################################

class engineer(object):
    '''An agent who is an engineer in an organization.'''
    
    def __init__(self,offset = 0,comm_prob = 0,contributors = []):
        '''Initialize the engineer agent.'''
        
        ##### Network Properties #####
        self.contributors = contributors # List of contributors who provide estimates

        ##### Utility Properties #####
        self.util_offset = offset # Utility function mean offset from historical mean
        self.util_thresh = None # Utility function threshold of action,
            # defined with respect to the utility at the historical mean

        ##### Historical Information #####
        self.hist_mean = None # Mean of history
        self.hist_var = None # Variance of history
        self.gen_hist()
        
        ##### Estimate Information #####
        self.est_samples = [] # Estimate samples
        self.est_subsamples = [] # Estimate subsamples
            # Contains the list of samples provided by the contributors during
            # a given iteration of the model.
        self.est_mean = [] # Estimate mean
        self.est_var = [] # Estimate variance
        self.est_type = (np.random > comm_prob) # Estimate type
            # either current status (True) or predicted outcome (False)
        self.est_util = [] # Utility of the current estimate            
    
    def __repr__(self):
        return self.__class__.__name__
    
    def calc_util(self,value):
        '''Calculates the utility of an estimate.'''
        self.util = (1/mt.sqrt(2*mt.pi*self.hist_var)) \
            * mt.exp(-((value-(self.hist_mean + self.util_offset))**2/(2*self.hist_var)))
        return self.util
    
    def adj_util(self,value):
        '''If an agent's utility isn't producing good results, that agent
        instructs reporting agents to increase their thresholds.'''
        
        self.util_thresh = self.util_thresh*(1 + value)


    def gen_hist(self):
        '''Generate history for the agent, either by aggregation or generating
        new information from random sampling if the agent doesn't have any
        contributors to provide information for aggregation.'''
        
        if not(self.hist_mean):
            
            # If the agent doesn't have contributors, generate random historical mean and variance
            if not(self.contributors):
                
                self.hist_mean = np.random.normal(0,1) # Historical mean
                self.hist_var = np.random.chisquare(1) # Historical variance
            
            # Otherwise, total contributor historical values
            else: 
                
                self.sub_hist_mean = [] # List of contributor historical means
                self.sub_hist_var = [] # List of contributor historical variances
                
                # Cycle through contributors
                for agent in self.contributors: 
                    
                    # Request contributor mean and variance
                    hist_sample = agent.give_hist()
                    
                    # Assign contributor mean and variance, respectively
                    self.sub_hist_mean.append(hist_sample[0]) 
                    self.sub_hist_var.append(hist_sample[1])
                
                # Calculate own historical mean and variance, respectively
                self.hist_mean = sum(self.sub_hist_mean)
                self.hist_var = sum(self.sub_hist_var)
            
            # Calculate utility threshold
            self.util_thresh = self.calc_util(self.hist_mean)
        
        # Return the historical mean and variance
        return [self.hist_mean,self.hist_var]

    def give_hist(self):
        '''Provide historical mean when requested by another agent'''
        
        # If historical information doesn't already exist...
        if not(self.hist_mean):
            
            # ...generate the historical data
            self.gen_hist()
            
        # Return the historical mean and variance    
        return [self.hist_mean,self.hist_var]
    
    def give_est(self):
        '''Provide current estimate when requested by another agent'''
        
        # Update current estimate
        self.update_est()
        
        # Return estimate type
        if self.est_type:
            
            # Return the current mean
            return self.est_mean[-1]
        
        else:
            
            # Return the historical mean
            return self.hist_mean
            
        
    def update_est(self):
        '''Updates the estimate for the agent using children if they exist, and
        using own information from historical data if they don't exist. The
        estimate is updated if the utility of the agent's estimate is below the
        defined threshold, but is not updated if it is above the threshold.'''
        
        # Check if utility doesn't exist or is too low...
        if (not(self.est_util) or (self.est_util[-1] < self.util_thresh)):

            # ...then the estimate needs updating.
            update_utility = True
            
        # But if the utility exists and is high enough..
        else:
    
            # ...then the estimate doesn't need updating.
            update_utility = False
            
        # Increase reporting agents' thresholds if not meeting utility (and exists).
        if not(not(self.est_util)) and (self.est_util[-1] < self.util_thresh):
            
            # Iterate through reporting agents for those already meeting utility.
            for agent in self.contributors: 
                    
                # If agent is already meeting their threshold and their array exists...
                if (agent.est_util[-1] >= agent.util_thresh) and (len(agent.est_util)>0):
                    
                    # ...Increase their array.
                    agent.adj_util(0.1)
        
        # If estimate needs updating, update it in this section.
        if update_utility:
        
                # If contributors exist, use their estimates.
                if not(not(self.contributors)):
                
                    # Reinitialize the subsample list
                    self.est_subsamples = [] 
                
                    # Cycle through contributing agents
                    for agent in self.contributors: 
                    
                        # Append contributor estimates
                        self.est_subsamples.append(agent.update_est())
                    
                    # Sum contributor estimates    
                    update_value = sum(self.est_subsamples) 
            
                # If contributors don't exist, generate estimate from hist data
                else:
                
                    # Sample from historical data distribution
                    update_value = np.random.normal(self.hist_mean,np.sqrt(self.hist_var))
        
        # If estimate doesn't need updating, copy last entry.
        else:
            
            # Set last value as update value
            update_value = self.est_samples[-1]
        
        # Append updated values to list of estimate samples
        self.est_samples.append(update_value)
        
        # Update this agent's mean
        self.est_mean.append(np.mean(self.est_samples))
        
        # Update this agent's variance based on the number of samples
        if ((len(self.est_samples) < 2) or (self.est_util[0] == self.est_util[-1])):
            self.est_var.append(self.hist_var)
        else:
            self.est_var.append(np.var(self.est_samples))
            
        # Update this agent's utility
        self.est_util.append(self.calc_util(self.est_mean[-1]))
        
        # Return mean value
        return self.est_mean[-1]
        
################################################################################            

def return_vars(agent):
    '''Returns all the variable values for a specified agent'''    
    
    print('***** Returning variables for agent ' + str(agent) + ' *****')
    print('Contributors = ' + str(agent.contributors))
    print('Historical mean = ' + str(agent.hist_mean))
    print('Historical variance = ' + str(agent.hist_var))
    print('Estimate samples = ' + str(agent.est_samples))
    print('Estimate subsamples = ' + str(agent.est_subsamples))
    print('Estimate mean = ' + str(agent.est_mean))
    print('Estimate variance = ' + str(agent.est_var))
    print('Communication type = ' + str(agent.est_type))
    print('Estimate utility = ' + str(agent.est_util))
    print('Utility offset = ' + str(agent.util_offset))
    print('Utility threshold = ' + str(agent.util_thresh))

def agent_test(offset=0,comm_prob=0,show_sys=True,show_sub=False):
    '''Test the functionality of an agent'''
    num_runs = 25
    
    a1 = engineer(offset,comm_prob)
    a2 = engineer(offset,comm_prob)
    a3 = engineer(offset,comm_prob)
    a4 = engineer(offset,comm_prob)
    a5 = engineer(offset,comm_prob)
    a6 = engineer(offset,comm_prob)
    a7 = engineer(offset,comm_prob)
    s1 = engineer(offset,comm_prob,contributors=[a1,a2,a3,a4,a5,a6,a7])
    
    for i in range(num_runs):
        s1.give_est()

    if show_sub:
        return_vars(a1)
        return_vars(a2)
        return_vars(a3)
        return_vars(a4)
        return_vars(a5)
        return_vars(a6)
        return_vars(a7)    
    
    
    if show_sys:
        return_vars(s1)
        
    x_values = range(num_runs)
    if show_sub:
        plt.plot(x_values,a1.est_mean)
        plt.plot(x_values,a2.est_mean)
        plt.plot(x_values,a3.est_mean)
        plt.plot(x_values,a4.est_mean)
        plt.plot(x_values,a5.est_mean)
        plt.plot(x_values,a6.est_mean)
        plt.plot(x_values,a7.est_mean)
    if show_sys:
        plt.plot(x_values,s1.est_mean,linewidth=5)
    plt.show()
    
    if show_sub:
        plt.plot(x_values,a1.est_var)
        plt.plot(x_values,a2.est_var)
        plt.plot(x_values,a3.est_var)
        plt.plot(x_values,a4.est_var)
        plt.plot(x_values,a5.est_var)
        plt.plot(x_values,a6.est_var)
        plt.plot(x_values,a7.est_var)
    if show_sys:
        plt.plot(x_values,s1.est_var,linewidth=5)
    plt.show()       

def execute(os=0,cp=0):
    '''Run the model on the agents defined in this function.'''
    
    # Define number of model iterations
    num_turns = 25
    num_iter = 50
    
    # Create a matrix for saving results
    sys_est = []
    sub_var = []
    sys_var = []
    sys_util = []
    
    # iterate through offsets
    #for g in len(offset_vect):
    
        
    # iterate through model runs
    for i in range(num_iter):
        
        # Create agents
        a1 = engineer(offset=os,comm_prob=cp)
        a2 = engineer(offset=os,comm_prob=cp)
        a3 = engineer(offset=os,comm_prob=cp)
        a4 = engineer(offset=os,comm_prob=cp)
        a5 = engineer(offset=os,comm_prob=cp)
        a6 = engineer(offset=os,comm_prob=cp)
        a7 = engineer(offset=os,comm_prob=cp)
        s1 = engineer(offset=os,comm_prob=cp,contributors=[a1,a2,a3,a4,a5,a6,a7])
        
        # Iterate through turns of model and update estimate at each turn
        for j in range(num_turns):
            
            # Update estimate for system agent if needed
            s1.give_est()
            
        # Save results of test to that spot in matrix
        #sub_var.append(np.var([a1.est_mean,a2.est_mean,a3.est_mean,a4.est_mean,a5.est_mean,a6.est_mean,a7.est_mean]))
        sys_est.append(s1.est_mean[-1])
        sys_var.append(s1.est_var[-1])
        sys_util.append(s1.est_util[-1])
        
    return sys_est

def process_data(sys_est,sys_var,sys_util):
    
    # NOTE: First index is comm_prob
    #       Second index is offset
    #       Third index is trial number
    
    ## Calcuclate the mean and variance of each set of 1000 trials
    
    # Create matrices for each of the parameter combinations
    sys_est_mean = np.empty([21,21])
    sys_var_mean = np.empty([21,21])
    sys_util_mean = np.empty([21,21])
    sys_est_var = np.empty([21,21])
    sys_var_var = np.empty([21,21])
    sys_util_var = np.empty([21,21])   
    
    # Create vectors for single parameter averages
    sys_est_mean_comm = np.empty(21)
    sys_est_mean_off = np.empty(21)
    sys_var_mean_comm = np.empty(21)
    sys_var_mean_off = np.empty(21)
    sys_util_mean_comm = np.empty(21)
    sys_util_mean_off = np.empty(21)
    
    for i in range(21):
        for j in range(21):
            sys_est_mean[i,j] = np.mean(sys_est[i,j,:])
            sys_var_mean[i,j] = np.mean(sys_var[i,j,:])
            sys_util_mean[i,j] = np.mean(sys_util[i,j,:])
            sys_est_var[i,j] = np.var(sys_est[i,j,:])
            sys_var_var[i,j] = np.var(sys_var[i,j,:])
            sys_util_var[i,j] = np.var(sys_util[i,j,:])
    
    for i in range(21):
        sys_est_mean_comm[i] = np.mean(sys_est_mean[i,:])
        sys_est_mean_off[i] = np.mean(sys_est_mean[:,i])
        sys_var_mean_comm[i] = np.mean(sys_var_mean[i,:])
        sys_var_mean_off[i] = np.mean(sys_var_mean[:,i])
        sys_util_mean_comm[i] = np.mean(sys_util_mean[i,:])
        sys_util_mean_off[i] = np.mean(sys_util_mean[:,i])
    
    
    return [sys_est_mean,sys_var_mean,
            sys_util_mean,sys_est_var,
            sys_var_var,sys_util_var,
            sys_est_mean_comm,sys_est_mean_off,
            sys_var_mean_comm,sys_var_mean_off,
            sys_util_mean_comm,sys_util_mean_off];

def mc_contour(dataset,title='Monte Carlo Mean of Individual Trial Estimates'):
    
    # Plot the results
    plt.figure(dpi=300)
    plt.contourf(offset,comm_prob,dataset)
    plt.colorbar()
    plt.title(title)
    plt.xlabel('Utility offset')
    plt.ylabel('Communication type probability')
    
def mc_parameters(x_axis,y_axis,title,x_label,y_label):
    
    # Plot the results
    plt.figure(dpi=300)
    plt.plot(x_axis,y_axis)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)





