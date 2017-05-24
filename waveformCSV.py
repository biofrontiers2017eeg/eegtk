import patient
import preprocessing
import string
import os

def getLetter(i):
	return string.ascii_lowercase[i]

def printINFO(v, string):
	if (v):
		print("INFO: {}".format(string))

def SaveWave2csv(pid, v=False, extension='raw', inOneCSV=False):
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
		# Working in Progress !!
		# Currentlt the concatted data frames have nwaveforms of time columns
		# we want only one columns with time
		fname = "".join([pid,'a_waves.', extension])
		fpath = os.path.join(path,fname)
		tmp = list(p.season_start.waves.items())
		df = pd.concat(tmp, axis=1)
		printINFO(v,"Saving file: {}".format(fpath))
		df.to_csv(fpath, index=False)

		for i in range(len(p.concussions)):

			fname = "".join([pid, getLetter(i+1), '_waves.', extension])
			fpath = os.path.join(path,fname)
			printINFO(v,"Saving file: {}".format(fpath))
			tmp = list(p.concussions[i].waves.items())
			df = pd.concat(tmp, axis=1)
			printINFO(v,"Saving file: {}".format(fpath))
			df.to_csv(fpath, index=False)

		fname = "".join([pid, getLetter(i+2), '_waves.', extension])
		fpath = os.path.join(path,fname)
		tmp = list(p.season_end.waves.items())
		df = pd.concat(tmp, axis=1)
		printINFO(v,"Saving file: {}".format(fpath))
		df.to_csv(fpath, index=False)

	else:

		for wave in waves:
			fname = "".join([pid,'a_',wave,'.', extension])
			fpath = os.path.join(path,fname)
			printINFO(v,"Saving file: {}".format(fpath))
			p.season_start.waves[wave].to_csv(fpath, index=False)

			for i in range(len(p.concussions)):

				fname = "".join([pid, getLetter(i+1), '_', wave,'.', extension])
				fpath = os.path.join(path,fname)
				printINFO(v,"Saving file: {}".format(fpath))
				p.concussions[i].waves[wave].to_csv(fpath, index=False)

			fname = "".join([pid, getLetter(i+2), '_', wave,'.', extension])
			fpath = os.path.join(path,fname)
			printINFO(v,"Saving file: {}".format(fpath))
			p.season_end.waves[wave].to_csv(fpath, index=False)


if __name__ == '__main__':
	path = '../Data2'
	nfilterCoeff = 4001
	waves = ['delta', 'theta', 'alpha', 'beta', 'gamma']

	pid = '98'
	SaveWave2csv(pid, True, True)
