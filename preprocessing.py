import pandas as pd
from scipy import signal


def stft(session):
    """
    performs
    :param session: session of eeg data with a raw instance variable containing a pandas data frame of channels
    :type ression: EEGSession
    :return:
    :rtype:
    """
    if not hasattr(session, "stft"):
        session.stft = {}
    for col in session.raw.columns:
        session.stft[col] = signal.stft(session.raw[col])
