# Neuro-ID
How reliable is EEG as a consistent identifier for individuals with Mild Traumatic Brain Injury (MTBI)?

## Scope
Pattern recognition and classification in time series data 

## Abstract
Raw brainwave data taken from an electroencephalogram (EEG) system has been shown to be unique for each individual.  Developing a machine learning algorithm to 
identify a specific person by their raw brainwave data can help to determine if a person’s brainwaves become unidentifiable after a concussion and therefore 
indicate changes in the brain.

## Methods
### <i> Tools </i>
Python package to analyse EEG Data: https://martinos.org/mne/stable/index.html

### <i> Subjects and Data Aquisition </i>
The 98 subjects included in the dataset were college aged males (18-24) Division I football players. Each player had a minimum 
of two EEG recording sessions. The first EEG measurements were recorded before the season began (baseline), and at the end of 
season (~6 months after). Some subjects had EEG retest sessions in order to record potential concussion, 20.4% of subjects indicated
concussion symptoms.  At the time of each measurement, the EEG was recorded for 4-15 minutes, the subjects were in an eye-closed 
resting state throughout the duration of the recording. During the recording sessions artifacts were identified and removed from 
the data analysis for accuracy. 

### <i> Biosignal Recording and EEG Parameterisation <i>
The EEG recordings were performed with electrodes secured at sites FP1, FP2, F7, F3, Fz, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz,
P4, T6, O1, O2 with 19-channel equipment (WAVi).  A headset containing the electrodes is placed on the patient. The electrodes are 
examined to ensure quality contact.  If contact is unacceptable, conductive gel can be added and the eSocs can be rubbed along 
the scalp to exfoliate the location of the electrode in order to assist in gaining proper contact.  Once contact is deemed 
acceptable, a auditory P300 Eyes Closed Protocol is run. The patient is instructed to avoid any synchronized motions and blinks 
during the P300 test as this will affect the quality of the data.   
![Image of 10-20 array](https://en.wikipedia.org/wiki/10-20_system_(EEG)#/media/File:21_electrodes_of_International_10-20_system_for_EEG.svg)


### <i> Data </i>
The subject data is anonymized with number labels, each number represents a different subject. The letters attached to the numbers
represent the session (i.e. a=first session, b=second session etc.). Each session has two files a .raw and a .art. 
The .raw files contain the raw waves  and the .art contain artifacting data for each session. Use both files to build raw waves. 
<br><u>.art file key </u>
Same dimensions as the raw data. Gives a coloring to the EEG data, that shows how reliability of the data. 
* 0= Reliable (black)
* 1= Not Reliable (red)
* 2= May or may not be reilable,to be used or discarded (blue)

### <i> Waves in EEG </i>
<b> Delta:</b> 0-4 Hz
<br><b> Theta:</b> 4-8 Hz
<br><b> Alpha:</b> 8-13 Hz
<br><b> Beta:</b> 13-20 Hz
<br><b> Gamma:</b> 20-40 Hz

<b> Data Files </b>
* 98 subjects
* 19 columns, ~61440 rows (256 s time step total of 4 minute data)

## Analysis
1. Extract (𝜶, 𝛽, 𝛾,𝜃) Waveform
2. Divide into 2s epochs
3. Features extraction using neural netork
4. FFT: static
5. Short-Time FFT: FFR with window
3. Compute static features for each epoch
4. Channel coherence (each wave)
5. Channel correlation Pearson (each wave)
6. Embedding a lower dimensional manifold 
7. Reduce dimensionality 
8. Reduce component analysis
9. Localized linear embedding (tSNE)
10. Wavelet
11. Analyse distances in reduced space between 2013 & 2014 baselines 

### Clustering

* Aggloremative
* k-means
* NNMF (Non Negative Matrix Factorization)

#### Measures

* Dynamics Time warping (Distance Meausure)

## Results
The data did not show siginificant differences in the channel cohernece in alpha frequency between concussed and non concussed subjects. Additional features need
to be analyzed in order to determine if EEG is a reliable identifier for a subject with mTBI.



