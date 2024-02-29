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
    Loads EEG data from a specified subject and directory, returning a dictionary with EEG signals, channel names, sampling frequency, event samples, and event types for an SSVEP experiment.
    
    Parameters:
    ----------
    subject <int>
        Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
    data_directory <str>
        Path from execution directory to folder containing ssvep data files.

    Returns:
    -------
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(x,y)> : float
            Raw EEG data in uV, ordered by channel.
            - x : EEG channel index
            - y : Data sample index
        'channels' <np.ndarray, shape=(x,)> : str
            Channel names, represented in <str> format.
            - x : EEG channel index
        'fs' <np.ndarray, shape=()> : int
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(x,)> : int
            The sample index at which each event occurred.
            - x : Event number/index
        'event_types' <np.ndarray, shape=(x,)> : str
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            - x : Event number/index
    '''
    # Load information from np file into dictionary
    data = np.load(f'{data_directory}/SSVEP_S{subject}.npz')
    data_dict = {key: data[key] for key in data.files}
    print(data_dict['event_types'])
    return data_dict

#%% Part 2

def plot_raw_data(data, subject, channels_to_plot):
    '''
    FUNCTION DESCRIPTION

    Parameters:
    ----------
    data <np.ndarray, shape=(x,y)> : float
        Raw EEG data in uV, ordered by channel.
        - x : EEG channel index
        - y : Data sample index
    subject <int>
        Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
    channels_to_plot <np.ndarray, shape=(x,)> : <str>
        Channel names to plot in different subplots.
        - x : EEG channel index

    Returns:
    -------
    None (Plots figures)
    '''
    # loop with plt.plot([start_time,end_time],[event_type,event_type]) 
    # plot_raw_data(data, subject, channels_to_plot)
    pass

#%% Part 3

def epoch_ssvep_data(data_dict, epoch_start_time=0, epoch_end_time=20):
    '''
    FUNCTION DESCRIPTION

    Parameters:
    ----------
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(x,y)> : float
            Raw EEG data in uV, ordered by channel.
            - x : EEG channel index
            - y : Data sample index (uV)
        'channels' <np.ndarray, shape=(x,)> : str
            Channel names, represented in <str> format.
            - x : EEG channel index
        'fs' <np.ndarray, shape=()> : int
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(x,)> : int
            The sample index at which each event occurred.
            - x : Event number/index
        'event_types' <np.ndarray, shape=(x,)> : str
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            - x : Event number/index
    epoch_start_time <float>
        Desired start time of epoch relative to the event, in seconds.
    epoch_end_time <float>
        Desired end time of epoch relative to the event, in seconds.

    Returns:
    -------
    eeg_epochs <np.array, shape=(x, y, z)> : float
        EEG data in each epoch (in uV).
        x : Trial/Epoch index
        y : Channel index
        z : Time point??
    epoch_times <np.array, shape=(x,)> : float
        The time in seconds (relative to the event) of each time point in eeg_epochs.
        x : Epoch sample index
    is_trial_15Hz <np.array, shape=(x,)> : boolean
        Array of booleans telling whether each trial was/was not a 15Hz trial.
        x : Trial/Epoch index
    '''
    pass

#%% Part 4

def get_frequency_spectrum(eeg_epochs,fs):
    '''
    FUNCTION DESCRIPTION

    Parameters:
    ----------
    eeg_epochs <array> : TYPE, shape(trials, size, time)
        DESCRIPTION
    fs : float
        Sampling frequency (Hz)
    
    Returns:
    -------
    eeg_epochs_fft : np.array, shape(trials, size, frequency)
        DESCRIPTION
    fft_frequencies : np.array, shape(frequency for each column in FFT)
        DESCRIPTION
    '''
    pass

#%% Part 5

def plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, channels, channels_to_plot, subject):
    '''
    This function calculates the mean power spectra for the specified channels, each in their own subplot.

    Parameters:
    ----------
    eeg_epochs_fft <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    fft_frequencies <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    is_trial_15Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    channels <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    channels_to_plot <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    subject <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    
    Returns:
    -------
    spectrum_db_12Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    spectrum_db_15Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    '''
    pass