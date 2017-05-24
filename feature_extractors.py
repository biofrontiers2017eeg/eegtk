import numpy as np
import scipy as sp


def correlation(raw_matrix):
    corr = np.corrcoef(np.transpose(raw_matrix))
    return corr[np.triu_indices(corr.shape[0], k=1, m=corr.shape[1])]


def coherence(raw_matrix):
    coherences = []
    for i in range(raw_matrix.shape[1]):
        for j in range(i+1):
            coherences.append(sp.signal.coherence(raw_matrix[:, i], raw_matrix[:, j])[0])
    return np.hstack(coherences)

def rms(raw_matrix):
	"""
	Calculates the root mean square value of a time series
	"""
	rmsValues = []
	for i in range(raw_matrix.shape[1]):
		x = raw_matrix[:,i]
		rmsValues.append(np.sqrt(np.mean(x**2)))
	return  np.hstack(rmsValues)

extractors = {
    "correlation": correlation,
    "coherence": coherence,
    "rms" : rms,
}
