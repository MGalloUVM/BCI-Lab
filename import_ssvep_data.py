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
    
    ##### (CH=num_channels, T=num_time_samples, E=num_events or num_epochs, ET=num_time_samples_in_epoch)

    Parameters:
    ----------
    subject <int>
        Subject number, as shown in file title (Ex: SSVEP_S1, 1 is the subject number)
    data_directory <str>
        Path from execution directory to folder containing ssvep data files.

    Returns:
    -------
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(CH,T), dtype=float>
            Raw EEG data in Volts, ordered by channel.
            CH : EEG channel index
            T : Time index (every 1 index = 1ms of time)
        'channels' <np.ndarray, shape=(CH) dtype=str>
            Corresponding channel names from dataset.
            CH : EEG channel index
        'fs' <np.ndarray, shape=(), dtype=float>
            (0-dimensional array)
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(E) dtype=int>
            The sample index at which each event occurred.
            E : Event number/index
        'event_durations' <np.ndarray, shape=(E) dtype=int>
            The duration, in samples, over which the event takes place
            E : Event number/index
        'event_types' <np.ndarray, shape=(E), dtype=str>
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            E : Event number/index
    '''
    # Load information from np file into dictionary
    data = np.load(f'{data_directory}/SSVEP_S{subject}.npz', allow_pickle=True)
    data_dict = {key: data[key] for key in data.files}
    return data_dict

#%% Part 2

def plot_raw_data(data_dict, subject, channels_to_plot):
    '''
    Plots the raw EEG data to determine its quality and see timing of events.

    ##### (CH=num_channels, ET=num_time_samples_in_epoch)

    Parameters:
    ----------
    data <np.ndarray, shape=(CH,ET), dtype=float>
        Raw EEG data in Volts, ordered by channel.
        CH : EEG channel index
        ET : Time index (every 1 index = 1ms of time)
    subject <int>
        Subject number, necessary for plot labels!
    channels_to_plot <np.ndarray, shape=(CH) dtype=str>
        Channel names to plot in different subplots.
        CH : EEG channel index

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

    ##### (CH=num_channels, T=num_time_samples, E=num_events or num_epochs, ET=num_time_samples_in_epoch)

    Parameters:
    ----------
    data_dict <dict>
        Dictionary containing the following keys:
        'eeg' <np.ndarray, shape=(CH,T), dtype=float>
            Raw EEG data in Volts, ordered by channel.
            CH : EEG channel index
            T : Time index (every 1 index = 1ms of time)
        'channels' <np.ndarray, shape=(CH) dtype=str>
            Channel names, represented in <str> format.
            CH : EEG channel index
        'fs' <np.ndarray, shape=(), dtype=float>
            (0-dimensional array)
            The sampling frequency, in Hz, represented as <float> in a 0-dimensional array
        'event_samples' <np.ndarray, shape=(E) dtype=int>
            The sample index at which each event occurred.
            E : Event number/index
        'event_durations' <np.ndarray, shape=(E) dtype=int>
            The duration, in samples, over which the event takes place
            E : Event number/index
        'event_types' <np.ndarray, shape=(E), dtype=str>
            The frequency of flickering checkerboard that starts flashing for each event. (Either '12hz' or '15hz' <str>)
            E : Event number/index
    epoch_start_time <float>
        Desired start time of epoch relative to the event, in seconds.
    epoch_end_time <float>
        Desired end time of epoch relative to the event, in seconds.

    Returns:
    -------
    eeg_epochs <np.array, shape=(E, CH, ET), dtype=float>
        EEG data in each epoch (in uV).
        E : Epoch index
        CH : Channel index
        ET : Time index in epoch (every 1 index = 1ms of time)
    epoch_times <np.array, shape=(ET), dtype=float>
        The time in seconds (relative to the event) of each time point in eeg_epochs.
        ET : Time index in epoch
    is_trial_15Hz <np.array, shape=(E), dtype=boolean>
        Array of booleans telling whether each trial was/was not a 15Hz trial.
        E : Epoch index
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

    # Assign bool value to each epoch/trial depending on the flashing target's hz value
    is_trial_15Hz = data_dict['event_types'] == '15hz'

    return eeg_epochs, epoch_times, is_trial_15Hz

#%% Part 4

def get_frequency_spectrum(eeg_epochs,fs):
    '''
    Compute and return the Fast Fourier Transform for each epoch and channel in the EEG data to convert 
    the signal from the time domain to the frequency domain. 

    ##### (E=num_epochs, CH=num_channels, ET=num_time_samples_in_epoch, FFT=num_frequency_bins[ET//2+1])

    Parameters:
    ----------
    eeg_epochs <np.array, shape(E, CH, ET), dtype=float>
        EEG data in each epoch (in uV).
        E : Epoch index
        CH : Channel index
        ET : Time index in epoch (every 1 index = 1ms of time)
    fs : float
        Sampling frequency (Hz)
    
    Returns:
    -------
    eeg_epochs_fft <np.array, shape=(E, CH, FFT), dtype=complex>
        The FFT for each epoch and channel, providing the frequency domain representation of the EEG signal.
        E : Epoch index
        CH : Channel index
        FFT : Frequency index (the number of unique frequency components)
    fft_frequencies <np.array, shape=(FFT), dtype=float>
        The array of frequency bins corresponding to the FFT output, indicating the frequencies represented in eeg_epochs_fft.
        FFT : Frequency index (the number of unique frequency components)
    '''
    # Get number of epochs, channels, and samples through eeg_epochs's shape
    num_epochs, num_channels, num_samples = eeg_epochs.shape
    # Initialize array for holding frequency, as result will be symmetric we divide num_samples
    eeg_epochs_fft = np.zeros((num_epochs, num_channels, num_samples // 2 + 1), dtype=complex)

    # Apply real fast fourier transform across the samples axis in all epochs/channels
    eeg_epochs_fft = np.fft.rfft(eeg_epochs, axis=2)

    # Calculate the frequencies corresponding to the FFT output
    fft_frequencies = np.fft.rfftfreq(num_samples, d=1.0/fs)

    return eeg_epochs_fft, fft_frequencies

#%% Part 5

def plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, channels, channels_to_plot, subject):
    '''
    This function calculates the mean power spectra for the specified channels, each in their own subplot.

    ##### (E=num_epochs, CH=num_channels, FFT=num_frequency_bins[ET//2+1])

    Parameters:
    ----------
    eeg_epochs_fft <np.array, shape=(E, CH, FFT), dtype=complex>
        The FFT for each epoch and channel, providing the frequency domain representation of the EEG signal.
        E : Epoch index
        CH : Channel index
        FFT : Frequency index (the number of unique frequency components)
    fft_frequencies <np.array, shape=(FFT), dtype=float>
        The array of frequency bins corresponding to the FFT output, indicating the frequencies represented in eeg_epochs_fft.
        FFT : Frequency index (the number of unique frequency components)
    is_trial_15Hz <np.array, shape=(E), dtype=boolean>
        Array of booleans telling whether each trial was/was not a 15Hz trial.
        E : Epoch index
    channels <np.ndarray, shape=(CH) dtype=str>
        Channel names from dataset.
        CH : EEG channel index
    channels_to_plot <np.ndarray, shape=(CH) dtype=str>
        Corresponding channel names to plot in different subplots.
        CH : EEG channel index
    subject <int>
        Subject number, necessary for plot labels!
    
    Returns:
    -------
    spectrum_db_12Hz <>
        DESCRIPTION
    spectrum_db_15Hz <>
        DESCRIPTION
    '''
    pass
