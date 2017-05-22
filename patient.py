import os
import sys
import pandas

from config import data_directory
from eeg_session import EEGSession


class Patient():
    def __init__(self, pid):
        self.season_start = None
        self.season_end = None
        self.concussions = []
        self.load_all(pid)

    def load_all(self, pid):
        """ Loads all files associated with a particular patient """
        ### load each file. the first is a traumatic brain injury ###
        let = "a"
        while os.path.exists(os.path.join(data_directory, pid + let + ".raw")):
            if let == "a":
                # first file is beginning of season
                self.season_start = self.load_session(pid + let)
            else:
                self.concussions.append(self.load_session(pid + let))
            let = chr(ord(let) + 1)

        # last file is end of season
        self.season_end = self.concussions[-1]
        self.concussions = self.concussions[:-1]

        # middle files are cuncussive events

    def load_session(self, filename):
        raw = pandas.read_csv(os.path.join(data_directory, filename + ".raw"))
        artifacts = pandas.read_csv(os.path.join(data_directory, filename + ".art"))
        return EEGSession(raw, artifacts)


def main():
    pid = sys.argv[1]
    patient = Patient(pid)
    print("season start: {}".format(len(patient.season_start.raw)))
    for i in range(len(patient.concussions)):
        print("concussion {}: {}".format(i, len(patient.concussions[i].raw)))
    print("season end: {}".format(len(patient.season_end.raw)))


if __name__ == "__main__":
    main()







