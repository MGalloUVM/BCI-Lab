# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

@author: Tynan Gacy
"""

#%% Part 1

import numpy as np
import matplotlib as plt
import scipy.fft

def load_ssvep_data(subject,data_directory):
    data_dict = "the dictionary of information about the dataset, as described in the README for this dataset"
    return data_dict
    

# Load dictionary
data = np.load('SSVEP_S1.npz')
eeg = data['eeg']
channels = data['channels']
fs = ...


#%% Part 2

# loop with plt.plot([start_time,end_time],[event_type,event_type]) 
# plot_raw_data(data, subject, channels_to_plot)