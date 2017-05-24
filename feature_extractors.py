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

extractors = {
    "correlation": correlation,
    "coherence": coherence,
}
