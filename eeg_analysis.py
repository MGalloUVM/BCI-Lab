"""
Created on Wed Jan 17, 5:50pm 2024
@authors: Michael Gallo, Nick Kent

FINISH WHEN FILE IS COMPLETE?
"""
import load_p300_data
import plot_p300_erps

#%% Part A
def prepare_epoch_data(subject_number, data_directory='./P300Data/'):
    """
        Prepare EEG data by splitting it into target and non-target epochs.
          Also calculates mean target/non-target epoch data.

        Parameters:
        - subject_number <int> : Subject ID as named on file
        - data_directory <str> : Path to directory where the EEG data files are located.

        Returns:
        - target_erp <np.array>[NUM_EPOCHS, NUM_CHANNELS] : ERPs for target events
        - nontarget_erp <np.array>[NUM_EPOCHS, NUM_CHANNELS] : ERPs for non-target events
        - erp_times <np.ndarray>[EPOCH_LENGTH] : time points relative to flashing onset.
        - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS] : individual epochs for target trials.
        - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS] : individual epochs for non-target trials.
    """
    # Load eeg experiment results into corresponding arrays
    #   - See function definition for types/dimensions
    eeg_time, eeg_data, rowcol_id, is_target = load_p300_data.load_training_eeg(subject_number, data_directory)
    # Get indices where rows/columns are flashed and
    #  whether they contain the target letter
    #   - See function definition for types/dimensions
    event_sample, is_target_event = plot_p300_erps.get_events(rowcol_id, is_target)
    # Load data from blocks around each flash event, create array
    #  to represent the time of each element in relation to the flash event.
    #   - See function definition for types/dimensions
    eeg_epochs, erp_times = plot_p300_erps.epoch_data(eeg_time, eeg_data, event_sample)
    # Combine all ERP data to two blocks--one with the average ERP from
    #  all target epochs, and one with the average ERP from all non-target epochs.
    #   - See function definition for types/dimensions
    target_erp, nontarget_erp = plot_p300_erps.get_erps(eeg_epochs, is_target_event)

    # Split the eeg_epochs into target and non-target epochs for further analysis
    target_epochs = eeg_epochs[is_target_event == 1]
    nontarget_epochs = eeg_epochs[is_target_event == 0]

    return target_erp, nontarget_erp, erp_times, target_epochs, nontarget_epochs


#%% Part B
def calculate_SE_Mean(epochs):
    """
    Calculate Standard Error of the Mean (SEM) for given data.

    Parameters:
    - data <np.array> : 2D array where rows are trials and columns are the time points time points.

    Returns:
    - sem <np.array> : SEM values for each time point across trials.
    """
    import numpy as np
    
    # Use numpy to calculate standard deviation for each time point
    std = np.std(epochs, axis=0)
    
    # Number of trials
    n = epochs.shape[0]
    
    # Calculate the standard error of the mean for confidence intervals
    se_mean = std / np.sqrt(n)
    
    # Return standard error of the epochs
    return se_mean

def plot_confidence_intervals(target_erp, nontarget_erp, erp_times, target_epochs, nontarget_epochs):
    """
        plot_confidence_intervals plots the ERPs on each channel for target and nontarget events.
         Plots confidence intervals as error bars around these ERPs. Also, shows error range for the
         ERPs.
         
         Params:
             - target_erp <np.array>[NUM_EPOCHS, NUM_CHANNELS] : ERPs for target events
             - nontarget_erp <np.array>[NUM_EPOCHS, NUM_CHANNELS] : ERPs for non-target events
             - erp_times <np.ndarray>[EPOCH_LENGTH] : time points relative to flashing onset.
             - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS] : individual epochs for target trials.
             - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS] : individual epochs for non-target trials.
             
         Returns: None
    """
    # Imports
    from matplotlib import pyplot as plt
    
    # Calculate se_mean for both target and nontarget ERPs
    target_se_mean = calculate_SE_Mean(target_epochs)
    nontarget_se_mean = calculate_SE_Mean(nontarget_epochs)
    
    # Determine the number of channels from the shape of the data
    num_channels = target_erp.shape[1]
    
    # Define the layout of the subplots. Adusts the number of rows based on the number of channels
    cols = 2
    rows = num_channels // cols + (num_channels % cols > 0)
    
    # Adjust the figure size as needed
    plt.figure(figsize=(10, rows * 3))
    
    # Iterates through all channels
    for channel_index in range(num_channels):
        # Create a subplot of all the channels for the current subject
        plt.subplot(rows, cols, channel_index + 1)
        
        # Selecting data for the current channel
        # Pulls target_erp, nontarget_erp, target_se_mean, and nontarget_se_mean for each channel
        # Grabs data up to teh current channel index for each variable
        target_erp_channel = target_erp[:, channel_index]
        nontarget_erp_channel = nontarget_erp[:, channel_index]
        target_se_mean_channel = target_se_mean[:, channel_index]
        nontarget_se_mean_channel = nontarget_se_mean[:, channel_index]
        
        # Plotting ERPs for the current channel
        # Use fill_between to display the confidence interval
        plt.plot(erp_times, target_erp_channel, label='Target ERP')
        plt.fill_between(erp_times, target_erp_channel - 2 * target_se_mean_channel, target_erp_channel + 2 * target_se_mean_channel, alpha=0.2)
        
        plt.plot(erp_times, nontarget_erp_channel, label='Non-Target ERP')
        plt.fill_between(erp_times, nontarget_erp_channel - 2 * nontarget_se_mean_channel, nontarget_erp_channel + 2 * nontarget_se_mean_channel, alpha=0.2)
        
        plt.xlabel('Time (ms)') # X axis label
        plt.ylabel('Amplitude (µV)') # Y axis label
        plt.title(f'Channel {channel_index + 1}') # Title
        plt.legend()
    
    # Show plot in a tight layout
    plt.tight_layout()
    plt.show()
