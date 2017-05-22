import numpy as np
import pandas as pd


class EEGSession():
    def __init__(self, raw, artifacts):
        self.raw = raw
        self.artifacts = artifacts

    def remove_artifacts(self, color="red"):
        pass

    def extract_windows(self, window_size="256"):
        """
        :param window_size: number of frames in a window
        :type window_size: string
        :return: dataframe with "window" column
        :rtype: Pandas dataframe
        """
        # create numbers which will be window size
        window_size = int(window_size)
        window = []
        for i in range(int(len(self.raw)/window_size + 1)):
            window.extend([i] * window_size)
        window = np.array(window)
        self.raw['window'] = pd.Series(window[:len(self.raw)], index=self.raw.index)
        self.raw.set_index('window')
