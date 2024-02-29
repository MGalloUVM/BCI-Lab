# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

@authors: Michael Gallo, Tynan Gacy
"""

#%% Part 1

import numpy as np
import matplotlib.pyplot as plt
import scipy.fft

def load_ssvep_data(subject, data_directory):
    '''
    FUNCTION DESCRIPTION
    Inputs:
     - subject <int> : Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
     - data_directory <str> : Path from execution directory to folder containing ssvep data files.
    Outputs:
     - data_dict <> :
    '''
    # Load information from np file into dictionary
    data_dict = np.load(f'{data_directory}/SSVEP_S{subject}.npz')
    dict = {}
    dict['eeg'] = data_dict['eeg']
    return data_dict


#%% Part 2

# loop with plt.plot([start_time,end_time],[event_type,event_type]) 
# plot_raw_data(data, subject, channels_to_plot)