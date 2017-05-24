import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from config import data_directory
from eeg_session import EEGSession
import preprocessing as prep
from embedding import Embedding


class Patient(object):
    def __init__(self, pid):
        """
        loads data for a patient and given a string which represents the patient id (which is a number).
        for example, file 1a.raw represents raw measurements from the first session for patient 1.
        Stores results as instance varibles of this object.

        IMPORTANT: Requires that you set the 'data_directory' variable in config.py

        :param pid: identifier of patient (a number)
        :type pid: string
        """
        self.pid = str(pid)
        self.pre_test = None
        self.post_test = None
        self.intermediate_tests = []
        self.n_concussions = 0
        self.columns = ["fp1", "fp2", "f3", "f4", "f7", "f8", "c3", "c4", "p3", "p4", "o1", "o2", "t3", "t4", "t5", "t6", "fz", "cz", "pz"]
        self.load_all(self.pid)

    def load_all(self, pid):
        """
        Loads all files associated with a particular patient, starts with pid + 'a' and goes until a letter
        doesn't exist. Stores results as instance variables
        :param pid: identifier of patient (a number)
        :type pid: string

        """
        if not os.path.exists(os.path.join(data_directory, pid + "a.raw")):
            print("First file: {0}a.raw not found, not loading.".format(pid))
            return
        # load each patient session
        let = "a"
        i = 0
        while os.path.exists(os.path.join(data_directory, pid + let + ".raw")):
            if let == "a":
                # first file is beginning of season
                self.pre_test = self.load_session(pid + let, pid + "_pretest")
            else:
                # middle files are cuncussive events
                self.intermediate_tests.append(self.load_session(pid + let, "_interm_" + str(i)))
                i += 1
            let = chr(ord(let) + 1)  # next letter

        # last file is end of season
        if len(self.intermediate_tests) > 0:
            self.post_test = self.intermediate_tests[-1]
            if self.post_test is not None:
                self.post_test.id = pid + "_post_test"
                self.intermediate_tests = self.intermediate_tests[:-1]
        # count number of concussions
        self.n_concussions = len(self.intermediate_tests)

    def load_session(self, filename, id):
        """
        :param filename: file prefix, as in: <prefix>.raw and <prefix>.art
        :type filename: string
        :param id: id of the eeg session
        :type id: string
        :return: an EEGSession object which has a pandas data frame for each of Session.raw and Session.art
        :rtype: EEGSession
        """
        try:
            raw = pd.read_csv(os.path.join(data_directory, filename + ".raw"), names=self.columns, dtype=np.float64)
            raw["time"] = pd.Series([i/256. for i in range(len(raw.index))])
        except:
            print("Can't load data file: {}".format(filename + ".raw"))
            return None
        try:
            artifacts = pd.read_csv(os.path.join(data_directory, filename + ".art"), names=self.columns, dtype=np.float64)
        except:
            print("Can't load data file: {}".format(filename + ".art"))
            return None
        return EEGSession(id, raw, artifacts)


def main():
    """
    test method for this class, takes a patient ID as the first cmd line argument and prints out lengths of each session
    that was loaded
    """
    pid = sys.argv[1]
    patient = Patient(pid)
    if patient.pre_test is not None:
        print("season start: {}".format(len(patient.pre_test.raw)))
        for i in range(len(patient.intermediate_tests)):
            print("concussion {}: {}".format(i, len(patient.intermediate_tests[i].raw)))
        print("season end: {}".format(len(patient.post_test.raw)))
    prep.stft(patient.pre_test)
    examples = patient.pre_test.get_examples()
    emb = Embedding("pca")
    emb.train(examples)
    emb_examples = emb.embed(examples)

    #patient.season_start.extract_windows()
    #patient.season_start.plot_windows(windows=np.arange(10), channels=["c3", "cz", "c4", "p3", "pz", "p4"])
    prep.extractWaves(patient.pre_test, n=4001, samplingRate=256, wave='alpha')
    patient.pre_test.extract_windows()
    patient.pre_test.plot_windows(windows=np.arange(10), channels=["c3", "cz", "c4", "p3", "pz", "p4"])
    #patient.season_start.plot_channels(channels=["c3", "cz", "c4", "p3", "pz", "p4"], end=256)
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    main()
