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

#%% Part 3

# Exploratory Data Analysis

# Find out how many samples there are per second in the dataset
# num_samples_in_sec(eeg_time)
# Find out the number of channels in our eeg data...
# print(eeg_data.shape)


eeg_epochs, erp_times = plot_p300_erps.epoch_data(eeg_time, eeg_data, event_sample)