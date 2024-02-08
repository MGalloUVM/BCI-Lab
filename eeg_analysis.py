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
