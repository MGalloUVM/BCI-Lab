#%%

from load_p300_data import load_training_eeg, plot_raw_eeg

# Define our 'magic numbers'
data_directory = './BCIs_S24/P300Data'
subject = 3

eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)
plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target)