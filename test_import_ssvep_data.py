# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

FileName
----------
test_import_ssvep_data.py

Description
-------------
This script utilizes the methods written in `import_ssvep_data.py` to analyze 
SSVEP EEG data. It loads data, plots raw EEG signals, epochs the data, 
computes Fourier transforms, and visualizes the frequency-power spectrum.

Authors
---------
Michael Gallo, Tynan Gacy

Collaborators & Sources
-------------------------
ChatGPT - used for improving grammar and descriptions.
"""

#%% Part 0 - Setup
import import_ssvep_data

subject_num = 1
data_directory = './SsvepData'

#%% Part 1 - Load information
data_dict = import_ssvep_data.load_ssvep_data(subject_num, data_directory)

#%% Part 2 - Plot raw EEG in uV
import_ssvep_data.plot_raw_data(data_dict, subject_num, channels_to_plot=['Fz','Oz'])

#%% Part 3 - Separate data into Epochs
eeg_epochs, epoch_times, is_trial_15Hz = import_ssvep_data.epoch_ssvep_data(data_dict)

#%% Part 4 - Get fourier transformations
eeg_epochs_fft, fft_frequencies = import_ssvep_data.get_frequency_spectrum(eeg_epochs, data_dict['fs'])

#%% Part 5 - Plot frequency-power spectrum data
import_ssvep_data.plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, data_dict['channels'], subject_num, channels_to_plot=['Fz','Oz'])