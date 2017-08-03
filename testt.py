# Chris Tang
# testt.py

import numpy as np
from matplotlib import pyplot as plt
import visa
import time

import agilent33500
import sr830
import ips12010
import lakeshore372

import transverseField
import lockinData
import tempControl

import fileio

##################################################################################################
# Define Parameters Here

# Agilent 33500B Function Generator
AGILENT_33500_FUNCTION_GENERATOR_PORT = "GPIB0::x::INSTR"
# IPS 120-10 Main Magnet Power Supply
IPS_12010_MAGNET_POWER_SUPPLY_PORT = "GPIB0::5::INSTR"
# Lakeshore 372 Temperature Controller
LAKESHORE_372_TEMPERATURE_CONTROLLER_PORT = "GPIB0::x::INSTR"
# SR 830 Lock-In Amplifier (Pick-up Coil)
PICKUP_COIL_LOCKIN_AMP_PORT = "GPIB0::9::INSTR"
# SR 830 Lock-In Amplifier (Drive Coil)
DRIVE_COIL_LOCKIN_AMP_PORT = "GPIB0::10::INSTR"
# SR 830 Lock-In Amplifier (Empty Coil)
EMPTY_COIL_LOCKIN_AMP_PORT = "GPIB0::11::INSTR"

def createInstClassInstances():
	"""Creates and returns instrument class instances based on defined constants in this script"""

	fnGen = agilent33500.Agilent33500(AGILENT_33500_FUNCTION_GENERATOR_PORT)
	magSupply = ips12010.IPS12010(IPS_12010_MAGNET_POWER_SUPPLY_PORT)
	tempController = lakeshore372.Lakeshore372(LAKESHORE_372_TEMPERATURE_CONTROLLER_PORT)
	pickupCoilockin = sr830.SR830(PICKUP_COIL_LOCKIN_AMP_PORT)
	driveCoilLockin = sr830.SR830(DRIVE_COIL_LOCKIN_AMP_PORT)
	emptyCoilLockin = sr830.SR830(EMPTY_COIL_LOCKIN_AMP_PORT)

	return fnGen, magSupply, tempController, pickupCoilLockin, driveCoilLockin, emptyCoilLockin
##################################################################################################
##################################################################################################
def singleExperiment(transverseField, pumpFreq, pumpAmp, probeFreq, probeAmp, dataPath, fnGen, magSupply, tempController, pickupCoilLockin, driveCoilLockin, emptyCoilLockin):
	"""Takes raw data for a single probe frequency and point in parameter-space

	Arguments:
		transverseField: Transverse field in (Tesla)
		pumpFreq: Pump frequency in (Hz)
		pumpAmp: Pump amplitude in (Tesla)
		probeFreq: Probe frequency in (Hz)
		probeAmp: Probe frequency in (Tesla)
		dataPath: path to which to save the data
		fnGen: instance of Agilent 33500 class
		magSupply: instance of IPS 12010 class
		tempController: instance of Lakeshore 372 class
		pickupCoilLockin: instance of SR 830 class connected to pickup coil (thru transformer)
		driveCoilLockin: instance of SR 830 class connected to shunt resistor of drive coil
		emptyCoilLockin: instance of SR 830 class connected to the empty half of the pickup coil
	"""

	timeStamp = time.time()
	temp = tempControl.readColdFingerTemp(tempController)
	pickupX, pickupY = pickupCoilLockin.readSnapshot()
	driveX, driveY = driveCoilLockin.readSnapshot()
	emptyX, emptyY = emptyCoilLockin.readSnapshot()
##################################################################################################
def main():
	# Create instrument class instances
	# fnGen, magSupply, tempController, pickupCoilLockin, driveCoilLockin, emptyCoilLockin = createInstClassInstances()

	testArr = np.zeros(2)

	pumpFreq = 202.
	pumpAmp = 0.6e-4
	transverseField = 0.4

	for i in np.arange(1):
		probeDeltaFreq = 3 * 1e-3
		for j in np.arange(1):
			np.savetxt(fileio.trialPath(pumpFreq, pumpAmp, transverseField, probeDeltaFreq), testArr, delimiter=',')

##################################################################################################
main()

