#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:13:18 2024

@author: mike
"""
#%% Part 1
from load_p300_data import load_training_eeg

subject = 3
data_directory = './P300Data/'
eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)

#%% Part 2
import plot_p300_erps

event_sample, is_target_event = plot_p300_erps.get_events(rowcol_id, is_target)

# Method used to find number of samples per second of data
def num_samples_in_sec(eeg_time):
    first_time = eeg_time[0]
    time_index = 1
    while eeg_time[time_index] - first_time != 1:
        print("time passed", eeg_time[time_index] - first_time)
        time_index += 1
    print(f"Number of elements within 1s of data: {time_index}")
    return time_index
