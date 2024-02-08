#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides testing for splitting up P300 data for analysis of Event-Related Neuron Potentials
  and plotting the resulting data.

@author: Aiden Pricer-Coan
@author: Michael Gallo

file: test_plot_p300_erps.py
BME 6710 - Jangraw
Lab Two: Event_Related Potentials
"""

# import statements
#%% Part 1
from load_p300_data import load_training_eeg

subject = 3
data_directory = './P300Data/'
eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)

#%% Part 2
import plot_p300_erps

event_sample, is_target_event = plot_p300_erps.get_events(rowcol_id, is_target)

#%% Part 3

# Exploratory Data Analysis

# Find out how many samples there are per second in the dataset
# num_samples_in_sec(eeg_time)
# Find out the number of channels in our eeg data...
# print(eeg_data.shape)


eeg_epochs, erp_times = plot_p300_erps.epoch_data(eeg_time, eeg_data, event_sample)

# Get mean ERPs for target and non-target events
target_erp, nontarget_erp = plot_p300_erps.get_erps(eeg_epochs, is_target_event)

# Plot ERPs of the subject
plot_p300_erps.plot_erps(target_erp, nontarget_erp, erp_times)


"""
0. Important Notes on Findings:

Upon inspection of the EEG data from subject 4, notable scaling discrepancies were observed across all channels, 
with the exception of Channel 1 (Range 0-7). Some channels reported extreme voltage values, reaching as low as -28000 μV.
Subject 5's data also displayed scaling issues, with values seemingly inflated by a factor of 5. Additionally, Channel 4 
exhibited temporal stretching, suggesting an irregular sampling rate or processing error. A thorough review of the raw data 
confirmed these irregularities, which are inconsistent with the maximum recorded voltage of approximately 7.9 μV, as reported 
in associated documentation. The inconsistencies in data scaling and representation are indicative of potential corruption, 
possibly resulting from erroneous sensor placement or other data corruption.
My suspicion is that this data comes from someone attempting to recreate the experiment as described in the paper.
This suspicion can further be confirmed in the fact that the participants in the paper's experiment were told to 
write LUCAS, but the data shows that the participants wrote LUKAS. Perhaps this is a different experiment?

1. Why do we see repeated up-and-down patterns on many of the channels?

The observed up-and-down patterns across many channels can be attributed to excitatory and inhibitory postsynaptic 
potentials (EPSPs and IPSPs) occurring in the postsynaptic neuron. Larger observed peaks could be indicative of 
action potentials followed by subsequent hyperpolarization, although this interpretation may be an oversimplification 
when considering complex EEG data that typically does not reflect individual action potentials due to its more global 
nature. We also noted anomalous spikes in the target ERP prior to the flash event, which may be due to the fact that 
there are fewer target events to successfully average out anomalous brain data.

2. Why are they more pronounced in some channels but not others?

The variability in signal amplitude across channels is influenced by the cognitive functions of different brain 
regions and the corresponding electrode placement. Channels overlying areas associated with attention, memory, 
and vision are expected to capture more pronounced voltage patterns due to the localized brain activity. As such, 
differences in channel responses may reflect the heterogeneous nature of neural processing across various cortical areas.

3. Why does the voltage on some of the channels have a positive peak around half a
second after a target flash?

A consistent positive voltage peak was identified across multiple channels, occurring sometime between 300-500ms after 
the target flash. This peak is our event-related potential, which is associated with the recognition and cognitive 
processing of the visual stimulus, involving regions such as the occipital lobe for initial visual detection and the 
parietal lobe for subsequent recognition and classification. The peak is reflective of the engagement of attentional 
mechanisms and working memory in response to the cognitive task at hand.

4. Which EEG channels (e.g., Cz) do you think these (the ones described in the last question)
might be and why?

Channels such as Pz (Parietal midline) and Cz (Central midline) are most likely the channels presenting the previously 
discussed event-related potentials, which is consistent with the fact that typical observations of P300 waves present
themselves in the parietal and central regions. Also, channels like FCz and CPz may show related activity due to their 
proximity to these areas.
"""
