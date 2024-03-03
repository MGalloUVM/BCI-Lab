# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

@authors: Michael Gallo, Tynan Gacy
"""

#%% Part 1

import numpy as np
import matplotlib.pyplot as plt
import scipy.fft

def load_ssvep_data(subject, data_directory):
    '''
    Loads EEG data from a specified subject and directory, returning a dictionary with EEG signals, channel names, sampling frequency, event samples, and event types for an SSVEP experiment.
    
    Parameters:
    ----------
    subject <int>
        Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
    data_directory <str>
        Path from execution directory to folder containing ssvep data files.

    Returns:
    -------
    (a=num_channels, b=num_samples, c=num_events/num_trials)
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(a,b)> : float
            Raw EEG data in Volts, ordered by channel.
            - a : EEG channel index
            - b : Data sample index
        'channels' <np.ndarray, shape=(a,)> : str
            Channel names, represented in <str> format.
            - a : EEG channel index
        'fs' <np.ndarray, shape=()> : int
            (0-dimensional array)
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(c,)> : int
            The sample index at which each event occurred.
            - c : Event number/index
        'event_durations' <np.ndarray, shape=(c,)> : int
            The duration, in samples, over which the event takes place
            - c : Event number/index
        'event_types' <np.ndarray, shape=(c,)> : str
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            - c : Event number/index
    '''
    # Load information from np file into dictionary
    data = np.load(f'{data_directory}/SSVEP_S{subject}.npz', allow_pickle=True)
    data_dict = {key: data[key] for key in data.files}
    return data_dict

#%% Part 2

def plot_raw_data(data_dict, subject, channels_to_plot):
    '''
    Plots the raw EEG data to determine its quality and see timing of events.

    Parameters:
    ----------
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(a,b)> : float
            Raw EEG data in Volts, ordered by channel.
            - a : EEG channel index
            - b : Data sample index
        'channels' <np.ndarray, shape=(a,)> : str
            Channel names, represented in <str> format.
            - a : EEG channel index
        'fs' <np.ndarray, shape=()> : int
            (0-dimensional array)
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(c,)> : int
            The sample index at which each event occurred.
            - c : Event number/index
        'event_durations' <np.ndarray, shape=(c,)> : int
            The duration, in samples, over which the event takes place
            - c : Event number/index
        'event_types' <np.ndarray, shape=(c,)> : str
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            - c : Event number/index
   subject <int>
        Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
    channels_to_plot <np.ndarray, shape=(a,)> : <str>
        Channel names to plot in different subplots.
        - a : EEG channel index

    Returns:
    -------
    None (Plots figures)
    '''
    # Extract data
    eeg_data = data_dict['eeg'] * 1e6 # Converts V to uV
    fs = data_dict['fs']
    event_samples = data_dict['event_samples']
    event_durations = data_dict['event_durations']
    event_types = data_dict['event_types']
    channels = data_dict['channels']
    
    # Convert time to seconds for legend
    t_seconds = np.arange(len(eeg_data[0]))/fs
    
    # Create figure and subplots
    fig, axs = plt.subplots(2, 1, figsize=(9, 11), sharex=True)
    
    # Plot event start and end times and types
    for sample, duration, event_type in zip(event_samples, event_durations, event_types):
        start_time = sample / fs
        end_time = (sample + duration) / fs
        axs[0].plot(start_time, event_type, 'bo')  # Dot at the start time
        axs[0].plot(end_time, event_type, 'bo')    # Dot at the end time
        axs[0].plot([start_time, end_time], [event_type, event_type], color='b', linewidth=2) # Line between start/end
    axs[0].set_title(f'SSVEP Subject {subject} Raw Data')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Flash Frequency')
    axs[0].grid()
    
    # Plot raw data from specified channels
    for channel_name in channels_to_plot:
        channel_index = np.where(channels == channel_name)[0][0]
        axs[1].plot(t_seconds, eeg_data[channel_index], label=channel_name)
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (uV)')
    axs[1].grid()
    axs[1].legend()
    
    pass

#%% Part 3

def epoch_ssvep_data(data_dict, epoch_start_time=0, epoch_end_time=20):
    '''
    Divide the SSVEP data into epochs based on the event indices specified in `data_dict`'s event_samples.

    Parameters:
    ----------
    (a=num_channels, b=num_samples, c=num_events/num_trials)
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(a,b)> : float
            Raw EEG data in Volts, ordered by channel.
            - a : EEG channel index
            - b : Data sample index
        'channels' <np.ndarray, shape=(a,)> : str
            Channel names, represented in <str> format.
            - a : EEG channel index
        'fs' <np.ndarray, shape=()> : int
            (0-dimensional array)
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(c,)> : int
            The sample index at which each event occurred.
            - c : Event number/index
        'event_durations' <np.ndarray, shape=(c,)> : int
            The duration, in samples, over which the event takes place
            - c : Event number/index
        'event_types' <np.ndarray, shape=(c,)> : str
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            - c : Event number/index
    epoch_start_time <float>
        Desired start time of epoch relative to the event, in seconds.
    epoch_end_time <float>
        Desired end time of epoch relative to the event, in seconds.

    Returns:
    -------
    (a=num_epochs, b=num_channels, c=num_samples)
    eeg_epochs <np.array, shape=(a, b, c)> : float
        EEG data in each epoch (in uV).
        a : Epoch index
        b : Channel index
        c : Sample index
    epoch_times <np.array, shape=(c,)> : float
        The time in seconds (relative to the event) of each time point in eeg_epochs.
        c : Sample index
    is_trial_15Hz <np.array, shape=(a,)> : boolean
        Array of booleans telling whether each trial was/was not a 15Hz trial.
        a : Trial index
    '''
    event_samples = data_dict['event_samples']
    event_durations = data_dict['event_durations']
    
    num_epochs = len(event_samples)
    num_channels = len(data_dict['channels'])
    # Because array will be of fixed size, get the max duration
    max_samples_per_epoch = int(np.max(event_durations))
    # Create eeg_epochs array, fill temporarily with placeholder np.nan values
    eeg_epochs = np.full((num_epochs, num_channels, max_samples_per_epoch), np.nan)

    # Fill out data
    for event_number in range(num_epochs):
        # Calculate start+end indices of event block
        event_start_index = int(event_samples[event_number])
        event_end_index = int(event_start_index + event_durations[event_number])
        # Extract data within epoch sample bounds
        epoch_data_V = data_dict['eeg'][:, event_start_index:event_end_index]
        # Convert from V to uV
        epoch_data_uV = epoch_data_V * 1e6
        eeg_epochs[event_number] = epoch_data_uV

    # Fill out epoch_times
    epoch_times = np.zeros((max_samples_per_epoch))
    epoch_time_duration = epoch_end_time - epoch_start_time
    # Get the amount of time between each sample based on the frequency
    time_between_samples = epoch_time_duration * data_dict['fs'] / max_samples_per_epoch
    # Set the epoch time range
    epoch_times = np.arange(max_samples_per_epoch) * time_between_samples

    # Assign bool value to each epoch/trial depending on 
    is_trial_15Hz = data_dict['event_types'] == '15hz'

    return eeg_epochs, epoch_times, is_trial_15Hz

#%% Part 4

def get_frequency_spectrum(eeg_epochs,fs):
    '''
    FUNCTION DESCRIPTION

    Parameters:
    ----------
    (a=num_epochs, b=num_channels, c=num_samples)
    eeg_epochs <np.array, shape(a, b, c)>
        EEG data in each epoch (in uV).
        a : Epoch index
        b : Channel index
        c : Sample index
    fs : float
        Sampling frequency (Hz)
    
    Returns:
    -------
    (a=num_epochs, b=num_channels, c=frequency??)
    eeg_epochs_fft <np.array, shape=(a, b, c)>
        DESCRIPTION
        a : Epoch index
        b : Channel index
        c : frequency
    fft_frequencies <np.array, shape=c?>
        DESCRIPTION
        c : frequency
    '''
    pass

#%% Part 5

def plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, channels, channels_to_plot, subject):
    '''
    This function calculates the mean power spectra for the specified channels, each in their own subplot.

    Parameters:
    ----------
    eeg_epochs_fft <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    fft_frequencies <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    is_trial_15Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    channels <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    channels_to_plot <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    subject <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    
    Returns:
    -------
    spectrum_db_12Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    spectrum_db_15Hz <TYPE/SHAPE> : NESTED_VAL_TYPE
        DESCRIPTION
    '''
    pass
