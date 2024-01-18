"""
Created on Wed Jan 17, 5:50pm 2024

@author: magallo
"""
#%%

from load_p300_data import load_training_eeg, plot_raw_eeg

# Define our 'magic numbers'
data_directory = './BCIs_S24/P300Data'
subject = 3

# Load training data into variables from passing our subject and data directory into load_training_eeg()
eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)
# Use our predefined function and variables to plot the variables
plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target)