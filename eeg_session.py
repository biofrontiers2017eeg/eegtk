import os
import numpy as np
import pandas as pd
import scipy as sp
from feature_extractors import extractors
from preprocessing import extractWaves


from matplotlib import pyplot as plt
from config import feature_directory


plot_ignore_columns = ["window", "time"]


class EEGSession(object):
    """
    This class represents an EEG session that has a "raw" file and an "artifact" file. The raw file contains channel
    measurements for each time step (rows are time steps and columns are channels) where there are 256 time steps per
    second
    """
    def __init__(self, id, raw, artifacts, artifact_remove_mode="normal"):
        self.id = str(id)
        self.raw = raw
        self.artifacts = artifacts
        self.window_size = None
        self.n_windows = None
        self.examples = None
        try:
            self.remove_artifacts(artifact_remove_mode)
        except:
            pass

    def remove_artifacts(self, mode="normal"):
        """
        for each channel, replaces artifact frames from the raw data frame. artifacts are indicated by 1's in self.artifacts for the same frame/channel
        :param mode: specifies what to do when replacing artifacts. options are:
            "zero": replace with zeros (these sections have zero variance and will mess up correlation features)
            "normal": replace with data from a random normal distribution with the same mean and variance as all
                non-artifact data in that channel
        :type mode: string
        """
        cols = [col for col in self.raw.columns if col not in plot_ignore_columns]
        # replace each colums with zeros where the artifacts matrix is 1's:
        for i, col in enumerate(cols):
            # make sure the artifacts file is the same length as the raw file. this is not true for some datasets
            if len(self.artifacts.as_matrix()[:, i]) == len(self.raw[col].as_matrix()):
                if mode == "zero":
                    replacements = np.zeros_like(self.raw[col].as_matrix())
                elif mode == "normal":
                    # mean of everything that is not anomalous
                    chan_mean = np.mean(self.raw[col].as_matrix()[[np.where(self.raw[col].as_matrix())]])
                    chan_std = np.std(self.raw[col].as_matrix()[[np.where(self.raw[col].as_matrix())]])
                    replacements = np.random.normal(chan_mean, chan_std, size = self.raw[col].as_matrix().shape)
                self.raw[col] = pd.Series(np.where(self.artifacts[col].as_matrix() == 1, replacements, self.raw[col].as_matrix()), dtype=np.float64)
                if np.any(pd.isnull(self.raw[col])):
                    print("{}: NaNs exist after artifact removal, setting raw to 'None'".format(self.id))
                    self.raw = None
                    return

    def extract_windows(self, window_size="256"):
        """
        adds a "windows" column to pandas in order to plot several windows on top of one another. the value in this
        column increments by 1 ever <window_size> time steps
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
            channels == [col for col in self.raw.columns if col not in plot_ignore_columns]
        frames = range(end)
        f, axes = plt.subplots(len(channels))
        for i, axis in enumerate(axes):
            colname = channels[i]
            axis.plot(frames/256., self.raw[colname][:end], 'k')
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
            channels = [col for col in self.raw.columns if col not in plot_ignore_columns]
        n_channels = len(channels)
        f, axes = plt.subplots(n_channels)
        for i, axis in enumerate(axes):
            colname = channels[i]
            channel = self.raw[colname]
            for window in windows:
                w = channel.loc[self.raw["window"] == window]
                axis.plot(frames[:len(w)]/256., w, alpha=alpha, color='k')
        plt.show()

    def plot_dataframe(self, df_name, channels=""):
        pass

    def get_examples(self, feature_args, epoch_size="all", channels="all", filtered_waves=True):
        """
        generates data examples from this session. time series are split up into epochs and static features are
        computed for each epoch. Each epoch is treated as a separate example from this session
        :param feature_args: a list of tuples that specifies the features to calculate. the first element of each tuple
            is a string which corresponds to the feature being calculated. the second element of the tuple is a list of
            positional arguments which will be passed to the feature generation function
        :type feature_args: list
        :param epoch_size: size of epoch or "all"
        :type epoch_size: int or string
        :param channels: list of strings which specify which columns to use to calculate features. corresponds to
            columns in the pandas data array
        :type channels: list
        :param filtered_waves: indicates whether to calculate features based on the raw features or the filtered (alpha,
            beta, ...) versions of those waves.
        :type filtered_waves: bool
        :return: data matrix where rows are examples and colums are calculated features
        :rtype: np.ndarray
        """
        if self.examples is not None:
            return self.examples
        if channels == "all":
            channels = [col for col in self.raw.columns if col not in plot_ignore_columns]
        if filtered_waves:
            extractWaves(self)
            if epoch_size == "all":
                epoch_size = list(self.waves.values())[0].shape[0]
            n_epochs = int(list(self.waves.values())[0].shape[0] / epoch_size)
            examples = []
            wave_matrices = {k: v[channels].as_matrix() for k, v in self.waves.items()}
            for i in range(n_epochs):
                feature_list = []
                for wave_name, wave_matrix in wave_matrices.items():
                    raw_epoch = wave_matrix[i*epoch_size:(i+1)*epoch_size].astype(np.float64)
                    # extract alpha, beta, waves etc.
                    for extractor, args in feature_args:
                        extractor = extractors[extractor]
                        feature_list.append(extractor(raw_epoch, *args))

                # create feature array for this exmaple
                features = np.hstack(feature_list)

                examples.append(features)
            # create numpy array for all these features
            self.examples = np.vstack(examples)
            print("features for {} have {} NaN values".format(self.id, np.sum(np.isnan(self.examples))))
        else:
            if epoch_size == "all":
                epoch_size = self.raw.shape[0]
            n_epochs = int(self.raw.shape[0] / epoch_size)
            examples = []
            raw_matrix = self.raw[channels].as_matrix()
            for i in range(n_epochs):
                feature_list = []

                raw_epoch = raw_matrix[i*epoch_size:(i+1)*epoch_size].astype(np.float64)
                # extract features for each feature argument
                for extractor, args in feature_args:
                    extractor = extractors[extractor]
                    feature_list.append(extractor(raw_epoch, *args))

                # create feature array for this exmaple
                features = np.hstack(feature_list)

                examples.append(features)
            # create numpy array for all these features
            self.examples = np.vstack(examples)
            print("features for {} have {} NaN values".format(self.id, np.sum(np.isnan(self.examples))))

        return self.examples

    def save_examples(self, subfolder):
        """
        Saves examples to the feature folder with .csv extension
        """
        if self.examples is not None:
            np.savetxt(os.path.join(feature_directory, subfolder, self.id + ".csv"), self.examples, delimiter=",")
        else:
            print("Examples has not been computed yet, not saving anything")

    def load_examples(self, subfolder):
        """
        loads examples from the feature folder
        :return:
        :rtype:
        """
        if os.path.exists(os.path.join(feature_directory, subfolder, self.id + ".csv")):
            self.examples = np.loadtxt(os.path.join(feature_directory, subfolder, self.id + ".csv"), delimiter=",", dtype=np.float64)
            if np.any(np.isnan(self.examples)):
                self.examples = None
        else:
            print("Examples file not found, loading nothing")
            self.examples = None
        return self.examples
