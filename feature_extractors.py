import numpy as np
import scipy as sp


def correlation(raw_matrix):
    """
    Calculates pairwise correlations between columns of the matrix
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    corr = np.corrcoef(np.transpose(raw_matrix))
    return corr[np.triu_indices(corr.shape[0], k=1, m=corr.shape[1])]


def coherence(raw_matrix):
    """
    Calculates the pairwise coherence values of the matrix
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    coherences = []
    for i in range(raw_matrix.shape[1]):
        for j in range(i + 1):
            coherences.append(sp.signal.coherence(raw_matrix[:, i], raw_matrix[:, j])[0])
    return np.hstack(coherences)


def rms(raw_matrix):
    """
    Calculates the root mean square value of a time series
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    rmsValues = []
    for i in range(raw_matrix.shape[1]):
        x = raw_matrix[:, i]
        rmsValues.append(np.sqrt(np.mean(x ** 2)))
    return np.hstack(rmsValues)


def meanAbs(raw_matrix):
    """
    Calculates the mean of absolute values
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    meanAbsValues = []
    for i in range(raw_matrix.shape[1]):
        x = raw_matrix[:, i]
        meanAbsValues.append(np.mean(np.abs(x)))
    return np.hstack(meanAbsValues)


def std(raw_matrix):
    """
    standard deviation of a time series
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    stdValues = []
    for i in range(raw_matrix.shape[1]):
        x = raw_matrix[:, i]
        stdValues.append(np.std(x))
    return np.hstack(stdValues)


def subBandRatio(raw_matrix, nBands=6):
    """
    The ratio of the mean of absolute values, between adjacent columns
    Note: This measure was used in a paper where the columns of the matrix represent the
    frequency bands
    :param raw_matrix: data matrix where rows are examples and columns are raw features
    :type raw_matrix: ndarray
    :return: feature matrix where rows are examples and columns are calculated features
    :rtype: ndarray
    """
    ratio = []
    channel = int(raw_matrix.shape[1]/nBands)
    for i in range(channel):
        x = raw_matrix[:, i*nBands:(i+1)*nBands]
        for j in range(x.shape[1]-1):
            ratio.append(np.mean(np.abs(x[:,j])) / np.mean(np.abs(x[:,j+1])))
    return np.hstack(ratio)

extractors = {
    "correlation": correlation,
    "coherence": coherence,
    "rms": rms,
    "meanAbs": meanAbs,
    "std": std,
    "subBandRatio": subBandRatio,
}
