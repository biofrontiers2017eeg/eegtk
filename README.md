# Neuro-ID

## Scope

Is EEG test-retest data consistent enough to identify an individual? Do mTBI and concussive events change the effectiveness of the algorithm due to brainwave changes?

## Abstract
Raw brainwave data taken from an electroencephalogram (EEG) system has been shown to be unique for each individual.  Developing a machine learning algorithm to 
identify a specific person by their raw brainwave data can help to determine if a person’s brainwaves become unidentifiable after a concussion and therefore 
indicate changes in the brain.

## Methods
### Tools
Python package to analyse EEG Data: https://martinos.org/mne/stable/index.html

### Waves in EEG
<b> Delta:</b> 0-4 Hz
<br><b> Theta:</b> 4-8 Hz
<br><b> Alpha:</b> 8-13 Hz
<br><b> Beta:</b> 13-20 Hz
<br><b> Gamma:</b> 20-40 Hz

### <i> Subjects and Data Aquisition </i>
The 98 subjects included in the dataset were college aged males (18-24) Division I football players. Each player had a minimum 
of two EEG recording sessions. The first EEG measurements were recorded before the season began (baseline), and at the end of 
season (~6 months after). Some subjects had EEG retest sessions in order to record potential concussion, 20.4% of subjects indicated
concussion symptoms.  At the time of each measurement, the EEG was recorded for 4-15 minutes, the subjects were in an eye-closed 
resting state throughout the duration of the recording. During the recording sessions artifacts were identified and removed from 
the data analysis for accuracy. 

### Biosignal Recording and EEG Parameterisation 
The EEG recordings were performed with electrodes secured at sites FP1, FP2, F7, F3, Fz, F4, F8, T3, C3, Cz, C4, T4, T5, P3, Pz,
P4, T6, O1, O2 with 19-channel equipment (WAVi).  A headset containing the electrodes is placed on the patient. The electrodes are 
examined to ensure quality contact.  If contact is unacceptable, conductive gel can be added and the eSocs can be rubbed along 
the scalp to exfoliate the location of the electrode in order to assist in gaining proper contact.  Once contact is deemed 
acceptable, a auditory P300 Eyes Closed Protocol is run. The patient is instructed to avoid any synchronized motions and blinks 
during the P300 test as this will affect the quality of the data.   



### Data
Data were measured in multiple times per subject, once at the start of the season, once at the end of the season and everytime the subject had a concussion.
the data is labeled alphabetically from starting from a to represent the EED data collection for different times.

**Ex/**

if a subject has data labeled as:

* a : measurement beginning of the season
* b : measurement after the first concussion
* c : measurement after the second concussion
* d : measurement the end of the season

Note Some subject may not had any concussions, or may have missing data where they did not show up at the beginning of the season.

**Raw EEG Data:**

* 19 columns, ~61440 rows (256 s time step total of 4 minute data)
* 98 Subjects

**Art file (Artifacts)**
Same dimensions as the raw data. Gives a coloring to the EEG data, that shows how reliable that data is.

* 0 : Black (reliable)
* 1 : Red (Not reliable)
* 2 : Blue (May or May not be reliable)

**P300 Data**

The subjects are hearing a beep sound at a specific pitch at regular interval. Than randomly a high pitch sound is exposed to the subject, which creates a spike in the subjects EEG data.

Each subject is exposed to 40 of these high pitch sounds at a random time frame.

More speficially the change of the EEG Data with regard to the high pitch sound is an amplitude increase. The amplitude increase is observed in any frequency band (depends at which frequency band the subject's EEG data is at the time of hearing the high pitch sound).

## Analysis
Feature Extraction
→data cleaning
→sessions split into epochs  → 2 seconds

Do below for each epoch 
-Brainwaves (delta, theta, alpha, beta, gamma) 
→ channel coherence
→channel correlation Pearson 

Embedding a lower dimensional manifold 
-reduce dimensionality 
→reduce component analysis
→Localized linear embedding (tSNE)

-Look at distances in reduced space between 2013 & 2014 baselines 

### PreProccessing
* Seperate out Different waves
* Features extraction using neural network
* FFT : static
* Short-Time FFT  : FFT with window
* Wavelet

### Clustering

* Aggloremative
* k-means
* NNMF (Non Negative Matrix Factorization)

#### Measures

* Dynamics Time warping (Distance Meausure)

### Prediction Model


