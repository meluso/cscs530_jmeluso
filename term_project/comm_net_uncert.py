# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-02-18
"""
import matplotlib as mp
mp.use('TkAgg')

import pylab as pl
import networkx as nx
import random as rd
import math as mt
import statistics as st

def init():
    global time, comm_prob, network
    
    # Initialize model time
    time = 0
    
    # Declare the universal probability of effective communication
    comm_prob = rd.random()
    
    # Create the network of agents
    network = nx.balanced_tree(7,6)


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
        
        













