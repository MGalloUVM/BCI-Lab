# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 10:17:04 2024

@author: nicho
"""
#%%
# Part A
from eeg_analysis import prepare_epoch_data

# Define subject number
subject_number = 3

# Prepare epoch data
target_erp, nontarget_erp, erp_times, target_epochs, nontarget_epochs = prepare_epoch_data(subject_number)


#%%
# Part B
from eeg_analysis import plot_confidence_intervals

# Plot ERPs with confidence intervals
plot_confidence_intervals(target_erp, nontarget_erp, erp_times, target_epochs, nontarget_epochs)
