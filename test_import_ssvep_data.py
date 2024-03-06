# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

@authors: Michael Gallo, Tynan Gacy
"""

import import_ssvep_data

subject_num = 1
data_directory = './SsvepData'

#%% Part 1
data_dict = import_ssvep_data.load_ssvep_data(subject_num, data_directory)

#%% Part 2
import_ssvep_data.plot_raw_data(data_dict, subject_num, channels_to_plot=['Fz','Oz'])

#%% Part 3
eeg_epochs, epoch_times, is_trial_15Hz = import_ssvep_data.epoch_ssvep_data(data_dict)

#%% Part 4
eeg_epochs_fft, fft_frequencies = import_ssvep_data.get_frequency_spectrum(eeg_epochs, data_dict['fs'])