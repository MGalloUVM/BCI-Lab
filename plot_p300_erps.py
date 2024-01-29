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