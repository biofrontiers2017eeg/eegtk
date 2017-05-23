import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


class EEGSession():
    def __init__(self, raw, artifacts):
        self.raw = raw
        self.artifacts = artifacts
        self.window_size = None
        self.n_windows = None

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
        self.window_size = int(window_size)
        window = []
        for i in range(int(len(self.raw)/self.window_size + 1)):
            window.extend([i] * self.window_size)
        window = np.array(window)
        self.raw['window'] = pd.Series(window[:len(self.raw)], index=self.raw.index)
        self.raw.set_index('window')
        self.n_windows = np.unique(self.raw['window'])

    def plot_channels(self, channels="all", end=-1):
        """
        plots the specified channels for this session up to frame "end"
        :param channels: list of strings that indicate which channels to plot or "all" to plot all channels
        :type channels: list or "all"
        :param end: last frame to plot, or -1 if plotting whole series
        :type end: int
        """
        if end == -1:
            end = len(self.raw)
        if channels == "all":
            channels == [col for col in self.raw.columns if col not in ["window"]]
        frames = range(end)
        f, axes = plt.subplots(len(channels))
        for i, axis in enumerate(axes):
            colname = channels[i]
            axis.plot(frames, self.raw[colname][:end], 'k')
            #axis.set_title(colname)
            axis.text(.5, .5, colname, horizontalalignment='center',
                      transform=axis.transAxes, bbox=dict(facecolor='white', alpha=0.5) )
        plt.show()

    def plot_windows(self, windows="all", channels="all", end=-1):
        """
        plots the specified windows on top of one another, for the specified channels up to frame end
        :param windows: list of windows to plot
        :type windows: int or "all"
        :param channels: list of strings that indicate which channels to plot or "all" to plot all channels
        :type channels: list or "all"
        :param end: last frame to plot, or -1 if plotting whole series
        :type end: int
        """
        if self.window_size is None:
            print("No windows extracted for this series, not plotting anything")
            return
        if end == -1:
            end = self.window_size
        if windows == "all":
            windows = np.unique(self.raw["window"])
        frames = range(end)
        alpha = 0.5 / np.log(len(windows)) if len(windows) > 1 else 1
        if channels == "all":
            channels = [col for col in self.raw.columns if col not in ["window"]]
        n_channels = len(channels)
        f, axes = plt.subplots(n_channels)
        for i, axis in enumerate(axes):
            colname = channels[i]
            channel = self.raw[colname]
            for window in windows:
                w = channel.loc[self.raw["window"] == window]
                axis.plot(frames[:len(w)], w, alpha=alpha, color='k')
        plt.show()
