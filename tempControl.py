# Chris Tang
# tempControl.py

import lakeshore372

##################################################################################################
# Mixing-Chamber Thermometer Parameters

# Channel for mixing chamber thermometer
MC_THERM_CHAN = None
# Calibration curve number for mixing chamber thermometer
MC_THERM_CALIBRATION_CURVE_NUM = None
# Excitation frequency for mixing chamber thermometer in (Hz)
MC_THERM_EXC_FREQ = None
# Excitation current for mixing chamber thermometer in (Amp)
MC_THERM_EXC_CURRENT = None
##################################################################################################
# Cold-Finger Thermometer Parameters

# Channel for cold finger thermometer
COLD_FINGER_THERM_CHAN = None
# Calibration curve number for cold finger thermometer
COLD_FINGER_THERM_CALIBRATION_CURVE_NUM = None
# Excitation frequency for mixing chamber thermometer in (Hz)
COLD_FINGER_THERM_EXC_FREQ = None
# Excitation current for cold finger thermometer in (Amp)
COLD_FINGER_THERM_EXC_CURRENT = None
##################################################################################################
def setTempControl(tempController, temp):
	raise NotImplementedError
##################################################################################################
def readColdFingerTemp(tempController):
	return tempController.readTemp(COLD_FINGER_THERM_CHAN)
##################################################################################################
def readMCTemp(tempController):
	raise NotImplementedError
##################################################################################################
def initializeTempController(tempController):
	"""Initialize the temperature controller"""

	raise NotImplementedError

	# Set the calibration curve numbers
	tempController.setCalibrationCurve(MC_THERM_CHAN, MC_THERM_CALIBRATION_CURVE_NUM)
	tempController.setCalibrationCurve(COLD_FINGER_THERM_CHAN, COLD_FINGER_THERM_CALIBRATION_CURVE_NUM)

	# Set the excitation frequencies
	# tempController.setExcFreq(MC_THERM_CHAN, MC_THERM_EXC_FREQ)
	# tempController.setExcFreq(COLD_FINGER_THERM_CHAN, COLD_FINGER_THERM_EXC_FREQ)

	# Set filter parameters
	tempController.setFilter()

	# Set the excitation currents
	tempController.setExcCurrent(MC_THERM_CHAN, MC_THERM_EXC_CURRENT)
	tempController.setExcCurrent(COLD_FINGER_THERM_CHAN, COLD_FINGER_THERM_EXC_CURRENT)
##################################################################################################
##################################################################################################
##################################################################################################