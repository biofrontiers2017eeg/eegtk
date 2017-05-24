import patient
import preprocessing
import string
import os
import pandas as pd
import argparse

waves = ['delta', 'theta', 'alpha', 'beta', 'gamma']

def getLetter(i):
	return string.ascii_lowercase[i]

def printINFO(v, string):
	if (v):
		print("INFO: {}".format(string))

def SaveWave2csv(pid, v=False, extension='raw', inOneCSV=False, nfilterCoeff=4001):
	printINFO(v, "Patient ID: {}".format(pid))
	
	p = patient.Patient(pid)
	
	printINFO(v, "Extracting waves for season_start!")
	preprocessing.extractWaves(p.season_start, n=nfilterCoeff, samplingRate=256, wave='all')
	
	printINFO(v, "Extracting waves for concussion!")
	for i in range(len(p.concussions)):
		preprocessing.extractWaves(p.concussions[i], n=nfilterCoeff, samplingRate=256, wave='all')
	
	printINFO(v, "Extracting waves for season_end!")
	preprocessing.extractWaves(p.season_end, n=nfilterCoeff, samplingRate=256, wave='all')
	
	printINFO(v, "Saving extracting waves to files!")
	if (inOneCSV):
		# Save season_start to csv
		fname = "".join([pid,'a_waves.', extension])
		fpath = os.path.join(path,fname)
		tmp = list(p.season_start.waves.values())
		
		for j in range(len(tmp)-1):
			tmp[j].drop('time', axis=1, inplace=True)
		
		df = pd.concat(tmp, axis=1)
		printINFO(v,"Saving file: {}".format(fpath))
		df.to_csv(fpath, index=False)

		# Save concussian to csv
		for i in range(len(p.concussions)):

			fname = "".join([pid, getLetter(i+1), '_waves.', extension])
			fpath = os.path.join(path,fname)
			tmp = list(p.concussions[i].waves.values())
			
			for j in range(len(tmp)-1):
				tmp[j].drop('time', axis=1, inplace=True)
			
			df = pd.concat(tmp, axis=1)
			printINFO(v,"Saving file: {}".format(fpath))
			df.to_csv(fpath, index=False)

		# Save season_end to csv
		fname = "".join([pid, getLetter(i+2), '_waves.', extension])
		fpath = os.path.join(path,fname)
		tmp = list(p.season_end.waves.values())

		for j in range(len(tmp)-1):
			tmp[j].drop('time', axis=1, inplace=True)
		
		df = pd.concat(tmp, axis=1)
		printINFO(v,"Saving file: {}".format(fpath))
		df.to_csv(fpath, index=False)

	else:
		# Will create one csv file for each waveform
		for wave in waves:
			# save season_start to csv
			fname = "".join([pid,'a_',wave,'.', extension])
			fpath = os.path.join(path,fname)
			printINFO(v,"Saving file: {}".format(fpath))
			p.season_start.waves[wave].to_csv(fpath, index=False)

			# save concussion to csv
			for i in range(len(p.concussions)):

				fname = "".join([pid, getLetter(i+1), '_', wave,'.', extension])
				fpath = os.path.join(path,fname)
				printINFO(v,"Saving file: {}".format(fpath))
				p.concussions[i].waves[wave].to_csv(fpath, index=False)

			# save season_end to csv
			fname = "".join([pid, getLetter(i+2), '_', wave,'.', extension])
			fpath = os.path.join(path,fname)
			printINFO(v,"Saving file: {}".format(fpath))
			p.season_end.waves[wave].to_csv(fpath, index=False)


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
		pid = np.arange(1,99)
	
	for i in pid:
		SaveWave2csv(str(i), v=args.v, inOneCSV=not(args.csvPerWave), extension=extension, nfilterCoeff=nfilterCoeff)
