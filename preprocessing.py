import pandas as pd
from scipy import signal
import numpy as np

ignore_columns = ["time", "window"]

def stft(session, **kwargs):
    """
    performs
    :param session: session of eeg data with a raw instance variable containing a pandas data frame of channels
    :type ression: EEGSession
    :return:
    :rtype:
    """
    if not hasattr(session, "stft"):
        session.stft = {}
    columns = [col for col in session.raw.columns if col not in ignore_columns]
    for col in columns:
        session.stft[col] = signal.stft(session.raw[col])

def extractWaves(session, n=4001, samplingRate=256, wave='all'):
    """
    Extracts a given waveform from the EEG data.
    The available waveforms are:
    delta : 0-4 Hz
    theta : 4-8 Hz
    alpha : 8-13 Hz
    beta  : 13-20 Hz
    gamma : 20-40 Hz


    :param session: session of eeg data with a raw instance variable containing a pandas data frame of channels
           n            : The number of filter coefficients used to construct thge filter (Higher number gives a more accurate filter)
           samplingRate : The sampling rate of the EEG Data, to which the filter will be applied
           wave         : The waveform, defines the bands of the filter
    :type session: EEGSession
    :return: 0 if success, 1 if it failed
    :rtype: int
    """
   
    # Create a dictionary of filter coefficients, the keys are waveforms
    b = {}
    if (wave == 'all'):
        waves = ['delta', 'theta', 'alpha', 'beta', 'gamma']
        for i in waves:
            b[i] = FIR(n,samplingRate, i)
    else:
        b[wave] = FIR(n,samplingRate, wave)

    if not hasattr(session, "waves"):
        # create a dictionary of pandas dataframes
        session.waves = {}
    chop = int((n-1)/2)
    columns = [col for col in session.raw.columns if col not in ignore_columns]
    for key in b:
        df = pd.DataFrame()
        for col in columns:
            # apply filter, via convolution
            s = pd.Series(np.convolve(session.raw[col], b[key], mode='valid'))
            df['_'.join([col,key])] = s
        if 'window' in session.raw.columns:
            df['window'] = session.raw['window'][chop:-chop].reset_index(drop=True)
        df['time'] = session.raw['time'][chop:-chop].reset_index(drop=True)
        session.waves[key] = df
    return 0

def FIR(n=4001, samplingRate=256, wave='alpha'):
    """

    :param n            : The number of filter coefficients used to construct thge filter (Higher number gives a more accurate filter)
           samplingRate : The sampling rate of the EEG Data, to which the filter will be applied
           wave         : The waveform, defines the bands of the filter
    :return: filter coefficients, 1 if it failed
    :rtype: int
    """

    nyquest = samplingRate/2.0
    if wave == 'delta':
        # 0-4 Hz Band Filter
        f = 4/nyquest
        b = signal.firwin(n, f, pass_zero=True)
    elif wave == 'theta':
        # 4-8 Hz Band Filter
        f1 = 4/nyquest
        f2 = 8/nyquest
        b = signal.firwin(n, [f1, f2], pass_zero=False)
    elif wave == 'alpha':
        # 8-13 Hz Band Filter
        f1 = 8/nyquest
        f2 = 13/nyquest
        b = signal.firwin(n, [f1, f2], pass_zero=False)
    elif wave == 'beta':
        # 13-20 Hz Band Filter
        f1 = 13/nyquest
        f2 = 20/nyquest
        b = signal.firwin(n, [f1, f2], pass_zero=False)
    elif wave == 'gamma':
        # 20-40 Hz Band Filter
        f1 = 20/nyquest
        f2 = 40/nyquest
        b = signal.firwin(n, [f1, f2], pass_zero=False)
    else:
        print('ERROR: Wave option not available')
        return 1
    return b

