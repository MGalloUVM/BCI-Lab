#%% Part 1

data_directory = './BCIs_S24/P300Data'

subject = 3

data_file = f"{data_directory}/s{subject}.mat"

#%% Part 2

import numpy as np
from matplotlib import pyplot as plt
import BCIs_S24.loadmat as loadmat

# Load data, extract training data
data = loadmat.loadmat(data_file)
train_data = data[f"s{subject}"]['train']

#%% Part 3

# Time in seconds
eeg_time = np.array(train_data[0])
# Data in unknown units (assumed uV)
eeg_data = np.array(train_data[1:9])
# Int representing col or row, 1-12
rowcol_id = np.array(train_data[9], dtype=int)
# Int 0 or 1, converted to boolean
is_target = np.array(train_data[10], dtype=bool)

#%% Part 4

fig, axs = plt.subplots(3, 1, sharex=True)
fig.suptitle(f"P300 Speller subject {subject} Raw Data")
# Time Display Range
time_x_min = 48
time_x_max = 53

# Row/Col ID subplot
axs[0].plot(eeg_time, rowcol_id)
axs[0].set_xlabel('time (s)')
axs[0].set_ylabel('row/col ID')
axs[0].set_xlim(time_x_min, time_x_max)
axs[0].grid(True)

# IsTarget subplot
axs[1].plot(eeg_time, is_target)
axs[1].set_xlabel('time (s)')
axs[1].set_ylabel('Target ID')
axs[1].set_xlim(time_x_min, time_x_max)
axs[1].grid(True)

# EEG Data subplot
axs[2].plot(eeg_time, eeg_data.T)
axs[2].set_xlabel('time (s)')
axs[2].set_ylabel('Voltage (uV)')
axs[2].set_xlim(time_x_min, time_x_max)
axs[2].set_ylim(-25, 25)
axs[2].grid(True)

plt.tight_layout()

# Save plot to file
plt.savefig(f"P300_S{subject}_training_rawdata.png")

# Show plot
plt.show()

#%% Part 5

