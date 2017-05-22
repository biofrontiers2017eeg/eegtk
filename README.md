# EEG Data analysis

## Scope

Is there a significat difference between the EEG data from the start of the Season and the end of the season if they had concussion during the season.

## Tools
Python package to analyse EEG Data: https://martinos.org/mne/stable/index.html

## Waves in EEG

## Data
Labelling of data:

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


