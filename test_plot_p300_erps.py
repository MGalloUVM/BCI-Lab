#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides functions for loading and extracting P300 data, plotting the resulting data for multiple subjects,
and printing participants spelling and word count.

Functions contain utility for extracting and slicing data from a data file, creating subplots with shared x axes,
looping through and plotting multiple instances, and predicting desired letters based on an RC speller.

@author: Aiden Pricer-Coan
@author: mike

file: test_plot_p300_erps.py
BME 6710 - Jangraw
Lab Two: Event_Related Potentials
"""

# import statements
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

# Get mean ERPs for target and non-target events
target_erp, nontarget_erp = plot_p300_erps.get_erps(eeg_epochs, is_target_event)

# Plot ERPs of the subject
plot_p300_erps.plot_erps(target_erp, nontarget_erp, erp_times)
