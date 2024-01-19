"""
Created on Wed Jan 17, 5:50pm 2024
@author: magallo

This module has 3 cells, which implement methods created in sibling file `load_p300_data.py`:
    Cell 1: Tests our functions for handling of loading raw data, then plotting raw data.
    Cell 2: Tests our function for handling of loading raw data, then plotting raw data for multiple subjects.
    Cell 3: Contains my solution for determining the word that the test subjects were told to spell.
"""
#%% Cell 1

from load_p300_data import load_training_eeg, plot_raw_eeg

data_directory = './BCIs_S24/P300Data'
subject = 3

# Load training data into variables from passing our subject and data directory into load_training_eeg()
eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)
# Use our plotting function and our new variables to plot the variables
plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target)

#%%

from load_p300_data import load_and_plot_all

data_directory = './BCIs_S24/P300Data'
# Create our subjects list of ints 3-10
subjects = range(3,11)
# Load all of our subjects' data and plot them
load_and_plot_all(data_directory, subjects)

#%%

