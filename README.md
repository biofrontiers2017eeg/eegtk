# EEG Data analysis

## Scope

## Tools
Python package to analyse EEG Data: https://martinos.org/mne/stable/index.html

## Waves in EEG

## Data

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


