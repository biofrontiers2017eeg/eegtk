import patient
import preprocessing
import string
import os
import pandas as pd
import numpy as np
import argparse

waves = ['delta', 'theta', 'alpha', 'beta', 'gamma']

def getLetter(i):
    return string.ascii_lowercase[i]

def printINFO(v, string):
    if (v):
        print("INFO: {}".format(string))

def SaveWave2csv(pid, v=False, extension='raw', inOneCSV=False, nfilterCoeff=4001):
    printINFO(v, "Patient ID: {}".format(pid))
    
    p = patient.Patient(pid, '')

    if p.pre_test is not None:
        printINFO(v, "Extracting waves for pre_test!")
        preprocessing.extractWaves(p.pre_test, n=nfilterCoeff, samplingRate=256, wave='all')
    
    printINFO(v, "Extracting waves for intermediate_tests!")
    for i in range(len(p.intermediate_tests)):
        preprocessing.extractWaves(p.intermediate_tests[i], n=nfilterCoeff, samplingRate=256, wave='all')
    
    if p.post_test is not None:
        printINFO(v, "Extracting waves for post_test!")
        preprocessing.extractWaves(p.post_test, n=nfilterCoeff, samplingRate=256, wave='all')
    
    printINFO(v, "Saving extracting waves to files!")
    if (inOneCSV):
        if p.pre_test is not None:
            # Save pre_test to csv
            fname = "".join([pid,'a_waves.', extension])
            fpath = os.path.join(path,fname)
            tmp = list(p.pre_test.waves.values())
            
            for j in range(len(tmp)-1):
                tmp[j].drop('time', axis=1, inplace=True)
            
            df = pd.concat(tmp, axis=1)
            printINFO(v,"Saving file: {}".format(fpath))
            df.to_csv(fpath, index=False)

        # Save intermediate_tests to csv
        nintermediate = len(p.intermediate_tests)
        for i in range(nintermediate):

            fname = "".join([pid, getLetter(i+1), '_waves.', extension])
            fpath = os.path.join(path,fname)
            tmp = list(p.intermediate_tests[i].waves.values())
            
            for j in range(len(tmp)-1):
                tmp[j].drop('time', axis=1, inplace=True)
            
            df = pd.concat(tmp, axis=1)
            printINFO(v,"Saving file: {}".format(fpath))
            df.to_csv(fpath, index=False)

        if p.post_test is not None:
            # Save post_test to csv
            fname = "".join([pid, getLetter(nintermediate+1), '_waves.', extension])
            fpath = os.path.join(path,fname)
            tmp = list(p.post_test.waves.values())

            for j in range(len(tmp)-1):
                tmp[j].drop('time', axis=1, inplace=True)
            
            df = pd.concat(tmp, axis=1)
            printINFO(v,"Saving file: {}".format(fpath))
            df.to_csv(fpath, index=False)

    else:
        # Will create one csv file for each waveform
        for wave in waves:
            if p.pre_test is not None:
                # save pre_test to csv
                fname = "".join([pid,'a_',wave,'.', extension])
                fpath = os.path.join(path,fname)
                printINFO(v,"Saving file: {}".format(fpath))
                p.pre_test.waves[wave].to_csv(fpath, index=False)

            # save intermediate_tests to csv
            nintermediate = len(p.intermediate_tests)
            for i in range(len(p.intermediate_tests)):
                fname = "".join([pid, getLetter(i+1), '_', wave,'.', extension])
                fpath = os.path.join(path,fname)
                printINFO(v,"Saving file: {}".format(fpath))
                p.intermediate_tests[i].waves[wave].to_csv(fpath, index=False)

            if p.post_test is not None:
                # save post_end to csv
                fname = "".join([pid, getLetter(nintermediate+1), '_', wave,'.', extension])
                fpath = os.path.join(path,fname)
                printINFO(v,"Saving file: {}".format(fpath))
                p.post_test.waves[wave].to_csv(fpath, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", required=True, type=str, help="the folder path to save the csv's")
    parser.add_argument("-v", required=False, action="store_true", help="verbose option to print INFO")
    parser.add_argument("-extension", required=False, type=str, help="the file extension to be used, default is raw")
    parser.add_argument("-pid", required=False, type=int, help="the pid to be saved, if not given it will save for all the patients id's")
    parser.add_argument("-nfilterCoeff", required=False, type=int, help="number of filter coefficients")
    parser.add_argument("-csvPerWave", required=False, action="store_true", help="save each waveform to different csv file")

    args = parser.parse_args()
    
    path = args.path

    if args.nfilterCoeff:
        nfilterCoeff = args.nfilterCoeff
    else:
        nfilterCoeff = 4001

    if args.extension:
        extension = args.extension
    else:
        extension = 'raw'
    
    if args.nfilterCoeff:
        nfilterCoeff = args.nfilterCoeff

    if args.pid:
        pid = [args.pid]
    else:
        pid = np.arange(55, 99)
    
    for i in pid:
        SaveWave2csv(str(i), v=args.v, inOneCSV=not(args.csvPerWave), extension=extension, nfilterCoeff=nfilterCoeff)
