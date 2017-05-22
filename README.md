# EEG Data analysis

## Scope


## Waves in EEG

## Data

Raw Data:

* 19 columns, ~61440 rows (256 s time step total of 4 minute data)
* 98 Subjects

Art file (Artifacts)
Same dimensions as the raw data

* 0 : Black 
* 1 : Red 
* 2 : Blue

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


