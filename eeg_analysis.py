"""
Created on Wed Jan 17, 5:50pm 2024
@authors: Michael Gallo, Nick Kent

FINISH WHEN FILE IS COMPLETE?
"""
from matplotlib import pyplot as plt
import numpy as np
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
         - target_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for target events
         - nontarget_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for non-target events
         - erp_times <np.ndarray>[SAMPLES_PER_EPOCH] : time points relative to flashing onset.
         - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is included in row/column.
         - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is NOT included in row/column.
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


def calculate_se_mean(epochs):
    """
        Calculate Standard Error of the Mean (SEM) for given data.
    
        Parameters:
         - epochs <np.array>[NUM_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS]: 3d array representing an epoch for each event in our data.
             ~ epochs[i][j][k], where i represents the i(th) epoch, 
                                     j represents the j(th) sample in the epoch,
                                     k represents the k(th) channel of data in the epoch.
        Returns:
        - se_mean <np.array>[] : SEM values for each time point across trials.
    """    
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
        Plots the ERPs on each channel for target and nontarget events.
        Plots confidence intervals as error bars around these ERPs.
        Shows error range for the ERPs.
         
        Params:
         - target_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for target events
         - nontarget_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for non-target events
         - erp_times <np.ndarray>[SAMPLES_PER_EPOCH] : time points relative to flashing onset.
         - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is included in row/column.
         - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is NOT included in row/column.
             
        Returns:
         - None
    """    
    # Calculate se_mean for both target and nontarget ERPs
    target_se_mean = calculate_se_mean(target_epochs)
    nontarget_se_mean = calculate_se_mean(nontarget_epochs)
    
    # Determine the number of channels from the shape of the data
    num_channels = target_erp.shape[1]
    
    # Define the layout of the subplots. Adusts the number of rows based on the number of channels
    cols = 3
    rows = num_channels // cols + (num_channels % cols > 0)
    
    plt.figure(figsize=(10, rows * 3))
    
    # Iterates through all channels
    for channel_index in range(num_channels):
        # Create a subplot of all the channels for the current subject
        plt.subplot(rows, cols, channel_index + 1)
        
        # Pulls target_erp, nontarget_erp, target_se_mean, and nontarget_se_mean for each channel
        target_erp_channel = target_erp[:, channel_index]
        nontarget_erp_channel = nontarget_erp[:, channel_index]
        target_se_mean_channel = target_se_mean[:, channel_index]
        nontarget_se_mean_channel = nontarget_se_mean[:, channel_index]
        
        # Plot target/nontarget ERPs for the current channel
        plt.plot(erp_times, target_erp_channel, label='Target ERP')        
        plt.plot(erp_times, nontarget_erp_channel, label='Non-Target ERP')
        
        # Fill in 95% confidence interval by adding/subtracting 2*SEM to/from mean ERP.
        plt.fill_between(erp_times, target_erp_channel - 2 * target_se_mean_channel, target_erp_channel + 2 * target_se_mean_channel, alpha=0.2, label='Target +/- 95% CI')
        plt.fill_between(erp_times, nontarget_erp_channel - 2 * nontarget_se_mean_channel, nontarget_erp_channel + 2 * nontarget_se_mean_channel, alpha=0.2, label='Non-Target +/- 95% CI')
        
        plt.xlabel('Time (ms)') # X axis label
        plt.ylabel('Amplitude (µV)') # Y axis label
        plt.title(f'Channel {channel_index}') # Title
        
        if (channel_index == num_channels - 1):
            plt.legend()
    
    # Show plot in a tight layout
    plt.tight_layout()
    plt.show()


#%% Part C


def bootstrap_p_values(target_epochs, nontarget_epochs, num_iterations=3000):
    """
        Calculate p-values for each time point and channel using bootstrapping.
    
        Parameters:
         - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is included in row/column.
         - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is NOT included in row/column.
         - num_iterations <int> : number of bootstrapping iterations
    
        Returns:
         - p_values: np.array, shape (SAMPLES_PER_EPOCH, NUM_CHANNELS), p-values for each time point and channel
    """
    # Combine target and nontarget epochs
    combined_epochs = np.concatenate((target_epochs, nontarget_epochs), axis=0)
    
    # Calculate the observed difference between target and nontarget means
    observed_diff = np.mean(target_epochs, axis=0) - np.mean(nontarget_epochs, axis=0)
    
    # Initialize an array to hold the bootstrap differences
    bootstrap_diffs = np.zeros((num_iterations, *observed_diff.shape))
    
    num_targets = target_epochs.shape[0]
    num_nontargets = nontarget_epochs.shape[0]
    
    for i in range(num_iterations):
        # Resample with replacement to create new target and nontarget groups
        bootstrap_sample = np.random.choice(range(combined_epochs.shape[0]), size=combined_epochs.shape[0], replace=True)
        bootstrap_targets = combined_epochs[bootstrap_sample[:num_targets]]
        bootstrap_nontargets = combined_epochs[bootstrap_sample[num_targets:num_targets+num_nontargets]]
        
        # Calculate difference between bootstrapped target and nontarget means
        bootstrap_diffs[i] = np.mean(bootstrap_targets, axis=0) - np.mean(bootstrap_nontargets, axis=0)
    
    # Calculate p-values: proportion of bootstrap differences as extreme as the observed difference
    p_values = np.mean(np.abs(bootstrap_diffs) >= np.abs(observed_diff[None, :, :]), axis=0)
    
    return p_values


#%% Part D


from mne.stats import fdr_correction

def plot_confidence_intervals_with_significance(target_erp, nontarget_erp, erp_times, target_epochs, nontarget_epochs, p_values):
    """
        Plots the ERPs on each channel for target and nontarget events, including confidence intervals and significant differences marked with dots.

        Parameters:
         - target_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for target events
         - nontarget_erp <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : ERPs for non-target events
         - erp_times <np.ndarray>[SAMPLES_PER_EPOCH] : time points relative to flashing onset.
         - target_epochs <numpy.ndarray>[NUM_TARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is included in row/column.
         - nontarget_epochs: <numpy.ndarray>[NUM_NONTARGET_EPOCHS, SAMPLES_PER_EPOCH, NUM_CHANNELS] : List of epochs where target letter is NOT included in row/column.
         - p_values: <np.array>[SAMPLES_PER_EPOCH, NUM_CHANNELS] : p-values for each time point and channel
         - subject_number <int> : identifier for the subject (used for saving the plot)
         - data_directory <str> : optional path for saving plots
        
        Returns:
         - None
    """
    # Adjust the function to calculate and plot as before
    target_se_mean = calculate_se_mean(target_epochs)
    nontarget_se_mean = calculate_se_mean(nontarget_epochs)
    num_channels = target_erp.shape[1]

    cols = 3
    rows = num_channels // cols + (num_channels % cols > 0)
    plt.figure(figsize=(10, rows * 3))

    # FDR correction
    _, corrected_p_values = fdr_correction(p_values, alpha=0.05)

    for channel_index in range(num_channels):
        plt.subplot(rows, cols, channel_index + 1)
        target_erp_channel = target_erp[:, channel_index]
        nontarget_erp_channel = nontarget_erp[:, channel_index]
        target_se_mean_channel = target_se_mean[:, channel_index]
        nontarget_se_mean_channel = nontarget_se_mean[:, channel_index]

        # Plot target/nontarget ERPs for the current channel
        plt.plot(erp_times, target_erp_channel, label='Target ERP')        
        plt.plot(erp_times, nontarget_erp_channel, label='Non-Target ERP')
        
        
        # Mark significant differences with dots
        significant_times = erp_times[corrected_p_values[:, channel_index] < 0.05]
        # Flag to ensure we only add the p_value label once
        first_time_labeling_flag = True
        for time in significant_times:
            if first_time_labeling_flag:
                plt.plot(time, 0, 'ko', label='p_FDR < 0.05')  # 'ko' for black dots
                first_time_labeling_flag = False
            else:
                plt.plot(time, 0, 'ko')  # 'ko' for black dots
        
        # Fill in 95% confidence interval by adding/subtracting 2*SEM to/from mean ERP.
        plt.fill_between(erp_times, target_erp_channel - 2 * target_se_mean_channel, target_erp_channel + 2 * target_se_mean_channel, alpha=0.2, label='Target +/- 95% CI')
        plt.fill_between(erp_times, nontarget_erp_channel - 2 * nontarget_se_mean_channel, nontarget_erp_channel + 2 * nontarget_se_mean_channel, alpha=0.2, label='Non-Target +/- 95% CI')
        
        # Add reference lines at x=0 and y=0
        plt.axhline(0, color='black', linestyle='dotted')
        plt.axvline(0, color='black', linestyle='dotted')

        plt.xlabel('Time (ms)')
        plt.ylabel('Amplitude (µV)')
        plt.title(f'Channel {channel_index}')
        
        if (channel_index == num_channels - 1):
            plt.legend()

    plt.tight_layout()

    # Save the plot
    #plt.savefig(f'{data_directory}subject_{subject_number}_ERP_significance.png')
    #plt.close()  # Close the plot explicitly after saving

