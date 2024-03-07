# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:14:55 2024

FileName
----------
test_import_ssvep_data.py

Description
-------------
This script utilizes the methods written in `import_ssvep_data.py` to analyze 
SSVEP EEG data. It loads data, plots raw EEG signals, epochs the data, 
computes Fourier transforms, and visualizes the frequency-power spectrum.

Authors
---------
Michael Gallo, Tynan Gacy

Collaborators & Sources
-------------------------
 - ChatGPT - used for improving grammar and descriptions.
 - Nayak, C. S., & Anilkumar, A. C. (2024). EEG Normal Waveforms. In StatPearls. 
 StatPearls Publishing. http://www.ncbi.nlm.nih.gov/books/NBK539805/
 - Garcia-Rill, E., D’Onofrio, S., Luster, B., Mahaffey, S., Urbano, F. J., & Phillips, C. 
 (2016). The 10 Hz Frequency: A Fulcrum For Transitional Brain States. Translational Brain 
 Rhythmicity, 1(1), 7–13.

Discussion Questions
---------------------
1. The brain signals responsible for the observed peaks at 12Hz and 15Hz during the respective 
trials are Steady-State Visually Evoked Potentials (SSVEPs). These signals are most prominent 
in the visual cortex, located in the occipital lobe of the brain, which is the primary center 
for visual processing. The occipital lobe (particularly the primary visual cortex), responds 
to visual stimuli, and that activity can be recorded. When visual stimuli (e.g., a screen flashing) 
at 12Hz are shown to the subject, recordings from the subject's visual cortex and occipital lobe 
show matching frequencies. The central parietal lobe also shows some activity in the trials' 
frequencies, which suggests further processing after the SSVEP originates in the occipital lobe. 
This demonstrates that these brain regions are active during visual stimulation.

2. These peak frequencies occur when the peaks of high Hz frequencies overlap themselves, creating 
smaller peaks at multiples of these frequencies. These smaller peaks are called harmonics and 
emerge when there is strong representation of their associated high Hz frequencies. Because of this, 
they might be visible in data when a frequency is particularly strong, like the 50Hz electrical 
noise artifact causing smaller peaks at 100Hz and 150Hz.  

3. Although it is only supposed to pick up brain activity, the sensitive EEG machines also pick up 
extraneous wavelengths from the environment and other regions of the body. The peak at 50Hz in the 
spectra is most likely caused by electrical line noise as this is the standard frequency of 
alternating current (AC) power supplies in Europe and other regions and is a common EEG artifact.

4. The upward bump around 10 Hz is likely alpha rhythm, a background brain wave that is not a SSVEP. 
It was found on most abundantly on channels C3, Cz, C4, CP1, CP2, P3, Pz, P4, O1, Oz, and O2, 
indicating that it was recorded primarily from the occipital and parietal lobes as well as the 
precentral motor cortex. The occipital and parietal lobe activity are consistent with occipital 
alpha rhythms known to occur when these brain regions are “idle” or not actively being stimulated. 
The activity in the precentral motor cortex (C3, Cz, C4) may be mu rhythms that occur when this 
region is at rest (i.e., not performing a motor action). 

"""

#%% Part 0 - Setup
import import_ssvep_data

subject_num = 1
data_directory = './SsvepData'

#%% Part 1 - Load information
data_dict = import_ssvep_data.load_ssvep_data(subject_num, data_directory)

#%% Part 2 - Plot raw EEG in uV
import_ssvep_data.plot_raw_data(data_dict, subject_num, channels_to_plot=['Fz','Oz'])

#%% Part 3 - Separate data into Epochs
eeg_epochs, epoch_times, is_trial_15Hz = import_ssvep_data.epoch_ssvep_data(data_dict)

#%% Part 4 - Get fourier transformations
eeg_epochs_fft, fft_frequencies = import_ssvep_data.get_frequency_spectrum(eeg_epochs, data_dict['fs'])

#%% Part 5 - Plot frequency-power spectrum data
import_ssvep_data.plot_power_spectrum(eeg_epochs_fft, fft_frequencies, is_trial_15Hz, data_dict['channels'], subject_num, channels_to_plot=['Fz','Oz'])
