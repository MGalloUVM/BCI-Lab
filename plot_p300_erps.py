#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:12:14 2024

@author: mike
"""

#%% Part 1
import numpy as np
import matplotlib.pyplot as plt

#%% Part 2

def get_events(rowcol_id, is_target):
    """
    Loads training data from filename calculated with the subject number and 
    given data_directory.
    
    Args:
        rowcol_id (np.array <int>): array of integers representing the flashed row/column identifier being flashed for each datapoint.
        is_target (np.array <bool>): array of booleans representing whether or not the flashed row/column contains the target letter for each datapoint
    
    Returns:
        np.array <int>: indices where every new event begins.
        np.array <bool>: array where each element indicates whether an event was a target event or not.
    """
    # Calculate the difference between rowcol_id vals
    diff_rowcol_id = np.diff(rowcol_id)
    
    # Find each index before where the value increases from 0
    #   Add 1, because we don't need the value BEFORE change...
    event_sample = np.where(diff_rowcol_id > 0)[0] + 1
    
    # Create array to denote whether is_target for each event
    is_target_event = is_target[event_sample]
    
    # Return the indices of event start and whether those events are target events
    return event_sample, is_target_event

#%% Part 3 - Exploratory Data Analysis:
    
def num_samples_in_sec(eeg_time):
    """
    Used to find the number of samples per second of data.
    
    Args:
        eeg_time (np.array): array of floats representing the time value in seconds at each index.
    
    Returns:
        int: number of elements within 1s of data
    """
    first_time = eeg_time[0]
    time_index = 1
    while eeg_time[time_index] - first_time != 1:
        print("time passed", eeg_time[time_index] - first_time)
        time_index += 1
    print(f"Number of elements within 1s of data: {time_index}")
    return time_index

#%% Part 3
SAMPLES_PER_SECOND = 256
NUM_CHANNELS = 8

def epoch_data(eeg_time, eeg_data, event_sample, epoch_start_time=-0.5, epoch_end_time=1):
    """
    Loads our data into epoch blocks for further analysis.
    
    Args:
        eeg_time (np.array): array of floats representing the time value in seconds at each index.
        eeg_data (np.array <np.array>): 2d array with EEG values for each channel at every data point in the experiment data.
        event_sample (np.array <int>): indices where every new event begins.
        epoch_start_time <float>: start time offset from start point of each epoch, can be + or -
        epoch_end_time <float>: end time offset from start point of each epoch, should be > epoch_start_time

    Returns:
        eeg_epochs (np.array <np.array...>): 3d array representing an epoch for each event in our data
            - eeg_epochs[i][j][k], where i represents the i(th) epoch, 
                                         j represents the j(th) sample in the epoch,
                                         k represents the k(th) channel of data in the epoch.
    """
    # Calculate # of seconds in a single epoch
    seconds_per_epoch = epoch_end_time - epoch_start_time
    # Calculate # of samples in a single epoch
    samples_per_epoch = int(SAMPLES_PER_SECOND * seconds_per_epoch)
    
    # Number of epochs...
    num_epochs = len(event_sample)
    
    # Create a 3D array of zeros with correct shape
    eeg_epochs = np.zeros([num_epochs, samples_per_epoch, NUM_CHANNELS])
    
    # UNIMPLEMENTED
    print(eeg_epochs.shape)
    
    return eeg_epochs
    
    
