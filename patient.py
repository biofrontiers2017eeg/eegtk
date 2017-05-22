import os
import sys
import pandas

from config import data_directory
from eeg_session import EEGSession


class Patient():
    def __init__(self, pid):
        """
        loads data for a patient and given a string which represents the patient id (which is a number).
        for example, file 1a.raw represents raw measurements from the first session for patient 1.
        Stores results as instance varibles of this object.

        IMPORTANT: Requires that you set the 'data_directory' variable in config.py

        :param pid: identifier of patient (a number)
        :type pid: string
        """
        self.season_start = None
        self.season_end = None
        self.concussions = []
        self.n_concussions = 0
        self.load_all(pid)

    def load_all(self, pid):
        """
        Loads all files associated with a particular patient, starts with pid + 'a' and goes until a letter
        doesn't exist. Stores results as instance variables
        :param pid: identifier of patient (a number)
        :type pid: string

        """
        if not os.path.exists(os.path.join(data_directory, pid + "a" + ".raw")):
            print("First file: {0}a.raw not found, not loading.".format(pid))
            return
        # load each patient session
        let = "a"
        while os.path.exists(os.path.join(data_directory, pid + let + ".raw")):
            if let == "a":
                # first file is beginning of season
                self.season_start = self.load_session(pid + let)
            else:
                # middle files are cuncussive events
                self.concussions.append(self.load_session(pid + let))
            let = chr(ord(let) + 1)  # next letter

        # last file is end of season
        self.season_end = self.concussions[-1]
        self.concussions = self.concussions[:-1]
        # count number of concussions
        self.n_concussions = len(self.concussions)

    def load_session(self, filename):
        """

        :param filename: file prefix, as in: <prefix>.raw and <prefix>.art
        :type filename: string
        :return: an EEGSession object which has a pandas data frame for each of Session.raw and Session.art
        :rtype: EEGSession
        """
        raw = pandas.read_csv(os.path.join(data_directory, filename + ".raw"))
        artifacts = pandas.read_csv(os.path.join(data_directory, filename + ".art"))
        return EEGSession(raw, artifacts)


def main():
    """
    test method for this class, takes a patient ID as the first cmd line argument and prints out lengths of each session
    that was loaded
    """
    pid = sys.argv[1]
    patient = Patient(pid)
    if patient.season_start is not None:
        print("season start: {}".format(len(patient.season_start.raw)))
        for i in range(len(patient.concussions)):
            print("concussion {}: {}".format(i, len(patient.concussions[i].raw)))
        print("season end: {}".format(len(patient.season_end.raw)))


if __name__ == "__main__":
    main()







