#!/usr/bin/env python3
"""
Created on Wed Jan 17, 5:50pm 2024
@author: magallo

This module contains three functions:
    load_training_eeg(subject, data_directory): Loads training data from filename calculated with the subject number and given data_directory.
    plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target): Plots parameters on a 3x1 matplotlib display with subject being displayed in the title, eeg_time as the x-axis in each plot, and the remaining parameters (excluding subject) plotted on the y-axis for each graph.
    load_and_plot_all(data_directory, subjects): Loads training data from filename calculated with the subject number and given data_directory.
"""
#%%

import numpy as np
from matplotlib import pyplot as plt
import BCIs_S24.loadmat as loadmat


#%%
def load_training_eeg(subject, data_directory):
    """Loads training data from filename calculated with the subject number and given data_directory.
    Args:
        subject (int): integer representing the subject number.
        data_directory (string): string representing the file path from script directory execution to data files.
    
    Returns:
        np.array: array containing the time marker for each datapoint.
        np.array: array containing a list of multiple eeg inputs for each datapoint.
        np.array <int>: array of integers representing the flashed row/column identifier being flashed for each datapoint.
        np.array <bool>: array of booleans representing whether or not the flashed row/column contains the target letter for each datapoint""" 
    # Load data, extract training data
    data_file = f"{data_directory}/s{subject}.mat"
    data = loadmat.loadmat(data_file)
    train_data = data[f"s{subject}"]['train']
    # Time in seconds
    eeg_time = np.array(train_data[0])
    # Data in unknown units (assumed uV)
    eeg_data = np.array(train_data[1:9])
    # Int representing col or row, 1-12
    rowcol_id = np.array(train_data[9], dtype=int)
    # Int 0 or 1, converted to boolean
    is_target = np.array(train_data[10], dtype=bool)
    
    return eeg_time, eeg_data, rowcol_id, is_target


def plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target):
    """Plots parameters on a 3x1 matplotlib display with subject being displayed in the title, eeg_time as the x-axis in each plot, and the remaining parameters (excluding subject) plotted on the y-axis for each graph.
    Args:
        subject (int): integer representing the subject number.
        eeg_time (np.array): array containing the time marker for each datapoint.
        eeg_data (np.array): array containing a list of multiple eeg inputs for each datapoint.
        rowcol_id (np.array <int>): array of integers representing the flashed row/column identifier being flashed for each datapoint.
        is_target (np.array <bool>): array of booleans representing whether or not the flashed row/column contains the target letter for each datapoint""" 
    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.suptitle(f"P300 Speller subject {subject} Raw Data")
    
    # Scope the ranges displayed on the x-axis (eeg_time)
    time_x_min = 48
    time_x_max = 53

    # Row/Col ID subplot
    axs[0].plot(eeg_time, rowcol_id)
    axs[0].set_xlabel('time (s)')
    axs[0].set_ylabel('row/col ID')
    # Scope x-axis
    axs[0].set_xlim(time_x_min, time_x_max)
    axs[0].grid(True)

    # IsTarget subplot
    axs[1].plot(eeg_time, is_target)
    axs[1].set_xlabel('time (s)')
    axs[1].set_ylabel('Target ID')
    # Scope x-axis
    axs[1].set_xlim(time_x_min, time_x_max)
    axs[1].grid(True)

    # EEG Data subplot
    axs[2].plot(eeg_time, eeg_data.T)
    axs[2].set_xlabel('time (s)')
    axs[2].set_ylabel('Voltage (uV)')
    # Scope our plot
    axs[2].set_xlim(time_x_min, time_x_max)
    axs[2].set_ylim(-25, 25)
    axs[2].grid(True)
    
    plt.tight_layout()

    # Save plot to file
    plt.savefig(f"P300_S{subject}_training_rawdata.png")

    # Show plot
    plt.show()
  

#%%

def load_and_plot_all(data_directory, subjects):
    """Loads training data from filename calculated with the subject number and given data_directory.
    Args:
        data_directory (string): string representing the file path from script directory execution to data files.
        subject (List <int>): integer representing the subject number.
    Returns:
        None"""
    # Iterate through each subject
    for subject in subjects:
        # Load training data into variables from passing our subject and data directory into load_training_eeg()
        eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)
        # Use our plotting function and our new variables to plot the variables
        plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target)
    
