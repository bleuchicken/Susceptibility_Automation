# Chris Tang
# fileio.py

import glob
import os

# ffff_AAAA_HHHH/dddd_xxx.csv:
# pumpFreq = fff.f (Hz)
# pumpAmp = A.AAA (Oe)
# transverseField = H.HHH (Tesla)
# deltaFreqProbe = ddd.d (mHz)
# trialNum (for multiple identical runs): xxx

##################################################################################################
# Paths

# Top-level folder where all of the programs/data are stored
PROGRAM_HOME_FOLDER = "/Users/ct/Documents/PyBin/Susceptibility_Automation/"
# Sub-folder where raw data is to be stored
RAW_DATA_FOLDER = PROGRAM_HOME_FOLDER + "Raw_Data/"
# Sub-folder where processed data is to be stored
PROCESSED_DATA_FOLDER = PROGRAM_HOME_FOLDER = "Processed_Data/"
##################################################################################################
def trialPath(pumpFreq, pumpAmp, transverseField, probeDeltaFreq):
	"""Returns the appropriate filename to create for a given set of parameters

	Arguments:
		pumpFreq: Pump frequency in (Hz)
		pumpAmp: Pump amplitude in (Tesla)
		transverseField: Transverse field in (Tesla)
		probeDeltaFreq: Difference between pump and probe frequencies in (Hz)
	Return Values:
		path: appropriate path
	"""

	parameterDir = RAW_DATA_FOLDER + parametersToDir(pumpFreq, pumpAmp, transverseField)
	if not os.path.isdir(parameterDir): os.mkdir(parameterDir)

	for i in range(1000):
		path = parameterDir + deltaFreqToStr(probeDeltaFreq) + "_" + str(i).zfill(3) + ".csv"
		if not os.path.exists(path): return path
##################################################################################################
# Convert values to appropriate strings for directory/file names

def pumpFreqToStr(freq):
	"""Converts a pump frequency in (Hz) to the format: fff.f (Hz)"""
	return ("%.1f" % freq).zfill(5).replace(".", "")
def strToPumpFreq(freqStr):
	"""Back-converts from string to pump frequency in (Hz)"""
	return float(freqStr) * 1e-1

def pumpAmpToStr(amp):
	"""Converts a pump amplitude in (T) to the format: A.AAA (Oe)"""
	return ("%.3f" % (amp * 1e4)).zfill(5).replace(".", "")
def strToPumpAmp(ampStr):
	"""Back-converts from string to pump amplitude in (T)"""
	return float(ampStr) * 1e-7

def transverseFieldToStr(field):
	"""Converts a pump amplitude in (T) to the format: A.AAA (Oe)"""
	return ("%.3f" % field).zfill(5).replace(".", "")
def strToTransverseField(fieldStr):
	"""Back-converts from string to pump amplitude in (T)"""
	return float(fieldStr) * 1e-3

def parametersToDir(pumpFreq, pumpAmp, transverseField):
	"""Converts a point in parameter space to a folder name


	Arguments:
		pumpFreq: Pump frequency in (Hz)
		pumpAmp: Pump amplitude in (Tesla)
		transverseField: Transverse field strength in (Tesla)
	Return Values:
		dir: directory string for these parameters
	"""

	return pumpFreqToStr(pumpFreq) + "_" + pumpAmpToStr(pumpAmp) + "_" + transverseFieldToStr(transverseField) + "/"
def dirToParameters(parameterDir):
	"""Back-converts a directory to the appropriate parameters

	Arguments:
		parameterDir: directory string
	Return Values:
		pumpFreq: Pump frequency in (Hz)
		pumpAmp: Pump amplitude in (Tesla)
		transverseField: Transverse field strength in (Tesla)
	"""

	pumpFreq = strToPumpFreq(parameterDir[0:4])
	pumpAmp = strToPumpAmp(parameterDir[5:9])
	transverseField = strToTransverseField(parameterDir[10:14])
	return pumpFreq, pumpAmp, transverseField

def deltaFreqToStr(deltaFreq):
	"""Converts a frequency in (Hz) to the format fff.f (mHz)"""
	return ("%.1f" % (deltaFreq * 1e3)).zfill(5).replace(".", "")
def strToDeltaFreq(deltaFreqStr):
	"""Back-converts from string to probe delta frequency (Hz)"""
	return float(deltaFreqStr) * 1e-4
##################################################################################################
##################################################################################################
##################################################################################################
def listFilesRecursively(dir, ext=".csv"):
	"""Returns a list of all files with given extension in a directory recursively
	
	Arguments:
		dir (string): path to directory to search
		ext (string): extension of acceptable files
	Return:
		fileList (list of strings): list of full paths to all files
	"""

	return [file for file in glob.glob(dir + '**/*' + ext, recursive=True)]
##################################################################################################
