"""
Created on Wed Jan 17, 5:50pm 2024
@author: magallo

This module has 3 cells, which implement methods created in sibling 
file `load_p300_data.py`:
    
    Cell 1: Tests our functions for handling of loading raw data, then plotting 
        raw data.
        
    Cell 2: Tests our function for handling of loading raw data, then plotting 
        raw data for multiple subjects.
        
    Cell 3: Contains my solution for determining the 5-letter word that the test 
        subjects were told to spell, using functions from load_p300_data. Also 
        prints the characters-per-minute typed and other stats.
"""
#%%

from load_p300_data import load_training_eeg, plot_raw_eeg

data_directory = './P300Data'
subject = 3

# Load training data into variables from passing our subject and data directory into load_training_eeg()
eeg_time, eeg_data, rowcol_id, is_target = load_training_eeg(subject, data_directory)
# Use our plotting function and our new variables to plot the variables
plot_raw_eeg(subject, eeg_time, eeg_data, rowcol_id, is_target)

#%%

from load_p300_data import load_and_plot_all

data_directory = './P300Data'
# Create our subjects list of ints 3-10
subjects = range(3,11)
# Load all of our subjects' data and plot them
load_and_plot_all(data_directory, subjects)

#%%

"""
    '[...] the RC speller highlights each column or row for 100ms and is grey 
    for 60ms ([6 rows×160ms] + [6 columns×160ms×15] flashes=28.8s). This yields one 
    character every 28.8s'
        - Guger2009.pdf
        
a) The data documentation reads that the row/col testers (in subjects 3-10) 
    were told to type 'LUCAS', and the text above also confirms our readings of 
    approximately 2 characters per minute.
    
b) Confirmed with code:
    
    'Channel number 10 contains the flash ID [...] The columns are numbered
    from 1 to 6 starting with the very left row at 1. Then the rows are 
    numbered from 7 to 12 starting with the very up row at 7. Hence, 
    IDs between 1 and 12 are used.'
        - description.pdf
    
- I first made a 6x6 2d list to represent the alphabet used in the experiments.
- I used the image in Guger2009.pdf to exact which characters went where.
- After creating the array, I simply looped through the data, waiting for the 
    corresponding column/row ids (rowcol_id) to flash while the matching 
    is_target was 1 30 times.
    
    'After 15 highlights of each character or row/column, [...]'
        - Guger2009.pdf
    
- I did this because the documentation clearly states that each row/column will
    flash 15 times, resulting in 30 total flashes where is_target is 1 for each
    character typed. A significant 'annoyance' I faced was counting each flash
    more than one time, leading to strange results, which I fixed at the start 
    of my for loop.
- Finally, I printed the resulting message, which appeared to be LUKAS on all 
    test subjects. Is LUCAS a misspelling in the documentation?
    
    '[...] the RC speller highlights each column or row for 100ms and is grey 
    for 60ms ([6 rows×160ms] + [6 columns×160ms×15] flashes=28.8s). This yields one 
    character every 28.8s'
        - Guger2009.pdf
    
- I measured time by subtracting the first eeg_time (in sec) from the last time element.
    Next, I converted the resulting time into minutes. I divided the length of our message
    by the time period to get the # of characters typed per minute. My result of
    approx. 2.27 chars per minute and 26.33 seconds per char is similar to the 28.8s
    given in our documentation, which leads me to believe my findings are correct.
    
"""
from load_p300_data import analyze_subject, analyze_all_rc_subjects


# TESTING

data_directory = './P300Data'

# analyze_subject(3, data_directory)
analyze_all_rc_subjects(data_directory)
