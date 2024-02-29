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
    return data_dict


#%% Part 2

def plot_raw_data(data, subject, channels_to_plot):
    '''
    FUNCTION DESCRIPTION
    Inputs:
     - data <> : DESCRIPTION
     - subject <int> : Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
     - channels_to_plot <list/array> : DESCRIPTION 
    Outputs:
     - None (Plots figures)
    '''
    # loop with plt.plot([start_time,end_time],[event_type,event_type]) 
    # plot_raw_data(data, subject, channels_to_plot)
    pass

#%% Part 3

def epoch_ssvep_data(data_dict, epoch_start_time=0, epoch_end_time=20):
    '''
    FUNCTION DESCRIPTION
    Inputs:
     - data_dict <> : DESCRIPTION
     - epoch_start_time <float> : Desired start time of epoch relative to the event, in seconds.
     - epoch_end_time <float> : Desired end time of epoch relative to the event, in seconds.
    Outputs:
     - eeg_epochs[x, y, z] <np.array> : EEG data after each epoch (in uV)
        x[] <> : trials
        y[] <> : channels
        z[] <> : time
     - epoch_times[x] <> : The time in seconds (relative to the event) of each time point in eeg_epochs
        x : DESCRIBE
     - is_trial_15Hz <> : DESCRIBE
    '''
    # loop with plt.plot([start_time,end_time],[event_type,event_type]) 
    # plot_raw_data(data, subject, channels_to_plot)
    pass

#%% Part 4

def get_frequency_spectrum(eeg_epochs,fs):
    '''
    FUNCTION DESCRIPTION
    Inputs:
     - eeg_epochs <array>: [trials, size, time]
     - fs <float> : sampling frequency (Hz)
    Outputs:
     - eeg_epochs_fft <array> : [trials, size, frequency]
     - fft_frequencies <array> : [frequency for each column in FFT]
    '''
    pass

#%% Part 5

def plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, channels, channels_to_plot, subject):
    '''
    DESCRIPTION
    Inputs:
     - eeg_epochs_fft <> : DESCRIPTION
     - fft_frequencies <> : DESCRIPTION
     - is_trial_15Hz <> : DESCRIPTION
     - channels <> : DESCRIPTION
     - channels_to_plot <> : DESCRIPTION
     - subject <> : DESCRIPTION
    Outputs:
     - spectrum_db_12Hz <> : DESCRIPTION
     - spectrum_db_15Hz <> : DESCRIPTION
    '''
    pass