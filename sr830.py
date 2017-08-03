# Chris Tang
# sr830.py

import visa
import numpy as np

##################################################################################################
class SR830():
	def __init__(self, port):
		self.port = port
		self.inst = visa.ResourceManager().open_resource(port)

		self.inst.write("LOCL 1")		# Set remote and unlocked
		self.inst.write("OUTX 1")		# Output to GPIB 
		self.inst.write("SEND 0")		# 1-shot buffer mode
		self.inst.write("TSTR 0")		# Turn off trigger-start feature
		self.inst.write("DDEF 1,0,0")	# Set Channel 1 to display X
		self.inst.write("DDEF 2,0,0")	# Set Channel 2 to display Y

		# Optional printing
		print("\nConnecting SR 830 through address:\n%s" % port)
		print("Querying IDN:\n%s" % self.inst.query("*IDN?"))
	######################################################################################
	def setInputMode(self, mode, printSwitch=True):
		"""Sets the input mode to single-ended (A) or differential (A-B)

		Arguments:
			mode: input mode to select
				"single": single-ended input (A)
				"differential": differential input (A-B)
		"""

		if mode == "single":
			self.inst.write("IRSC 0")
			if printSwitch: print("SR 830: Input mode: SINGLE-ENDED")
		elif mode == "differential":
			self.inst.write("IRSC 1")
			if printSwitch: print("SR 830: Input mode: DIFFERENTIAL")
		else:
			raise ValueError("Invalid mode passed to sr830.setInputMode()")

	def setShieldGrounding(self, state, printSwitch=True):
		"""Sets the grounding of the input shield to ground (True) or float (False)

		Arguments:
			state: determines whether shield is grounded (True) or floating (False)
		"""

		if state:
			self.inst.write("IGND 1")
			if printSwitch: print("SR 830: Input shield: GROUNDED")
		else:
			self.inst.write("IGND 0")
			if printSwitch: print("SR 830: Input shield: GROUNDED")
		
	def setInputCoupling(self, coupling, printSwitch=True):
		"""Sets the input coupling to ac or dc

		Arguments:
			coupling: determines ac/dc coupling of input
		"""

		if coupling == "ac":
			self.inst.write("ICPL 0")
			if printSwitch: print("SR 830: Input coupling: AC")
		elif coupling == "dc":
			self.inst.write("ICPL 1")
			if printSwitch: print("SR 830: Input coupling: DC")
		else:
			raise ValueError("Invalid coupling passed to sr830.setInputCoupling()")

	def setAuxOutput(self, chan, volt, printSwitch=True):
		"""Sets the output voltage of aux chan (1,2,3,4) to volt in (Volts)

		Arguments:
			chan: selected aux channel
			volt: desired voltage to output
		"""

		self.inst.write("AUXV %d,%f" % (chan, volt))
		if printSwitch: print("SR 830: Aux channel %d outputting: %e V" % (chan, volt))

	def setReferenceSource(self, source, printSwitch=True):
		"""Selects the reference source for triggering ("ext"/"int")

		Arguments:
			source: reference source for triggering
				"ext": triggers off of external signal
				"int": triggers off of internal oscillator
		"""

		if source == "ext":
			self.inst.write("FMOD 0")
			if printSwitch: print("SR 830: Reference source: EXTERNAL")
		elif source == "int":
			self.inst.write("FMOD 1")
			if printSwitch: print("SR 830: Reference source: INTERNAL")
		else:
			raise ValueError("Invalid source passed to sr830.setReferenceSource()")

	def setSensitivity(self, sense, printSwitch=True):
		"""Sets the sensitivity of the input
		Note, it finds the nearest allowed sensitivity

		Arguments:
			sense: desired sensitivity in (V)
		"""

		senseIndex = sensitivityToIndex(sense)
		self.inst.write("SENS %d" % senseIndex)
		if printSwitch: print("SR 830: Sensitivity set to: %e uV" % 1e6*indexToSensitivity(senseIndex))

	def setReserve(self, mode, printSwitch=True):
		"""Sets the reserve mode to high/normal/low noise

		Arguments:
			mode: reserve mode ("high"/"normal"/"low")
		"""

		if mode == "high":
			self.inst.write("RMOD 0")
			if printSwitch: print("SR 830: Reserve mode set to: HIGH")
		if mode == "normal":
			self.inst.write("RMOD 1")
			if printSwitch: print("SR 830: Reserve mode set to: NORMAL")
		if mode == "low":
			self.inst.write("RMOD 2")
			if printSwitch: print("SR 830: Reserve mode set to: LOW NOISE")
		else:
			raise ValueError("Invalid mode passed to sr830.setReserve()")

	def setTimeConstant(self, tau, printSwitch=True):
		"""Sets the time constant in (sec)
		Note, it will round to the nearest allowed time constant

		Arguments:
			tau: time constant in (sec)
		"""

		tauIndex = timeConstantToIndex(tau)
		self.inst.write("OFLT %d" % tauIndex)
		if printSwitch: print("SR 830: Sensitivity set to: %e sec" % indexToTimeConstant(tauIndex))

	def setLowPassFilterSlope(self, slope, printSwitch=True):
		"""Sets the slope of the low-pass filter in (dB/oct)

		Arguments:
			slope: slope (6,12,18,24) of low-pass filter in (dB/oct)
		"""

		if slope in [6,12,18,24]:
			self.inst.write("OFSL %d" % (slope // 6 - 1))
			if printSwitch: print("SR 830: Low-Pass Filter Slope: %d dB/oct" % slope)
		else:
			raise ValueError("Invalid slope passed to sr830.setLowPassFilterSlope()")
	
	def setAutoGain(self, printSwitch=True):
		"""Turns on the auto-gain function"""

		self.inst.write("AGAN")
		if printSwitch: print("SR 830: Auto-Gain turned ON")
	
	def setSampleRate(self, rate, printSwitch=True):
		"""Sets the sample rate in (Hz)
		Note, finds the nearest allowed rate

		Arguments:
			rate: sample rate in (Hz)
		"""

		sampleIndex = sampleRateToIndex(rate)
		self.inst.write("SRAT %d" % sampleIndex)
		if printSwitch: print("SR 830: Sample rate set to: %.4f Hz" % indexToSampleRate(sampleIndex))

	def getSampleRate(self, printSwitch=True):
		"""Reads the sample rate

		Return Values:
			rate: current sample rate in (Hz)
		"""

		rate = indexToSampleRate(int(self.inst.query("SRAT?")))
		if printSwitch: print("SR 830: Sample Rate is currently: %e Hz" % rate)
		return rate

	def startDataStorage(self, printSwitch=True):
		"""Starts data storage"""

		self.inst.write("STRT")
		if printSwitch: print("SR 830: Data storage started.")

	def stopDataStorage(self, printSwitch=True):
		"""Pauses data storage"""

		self.inst.write("PAUS")
		if printSwitch: print("SR 830: Data storage paused.")

	def resetDataBuffer(self, printSwitch=True):
		"""Resets the data buffer"""

		self.inst.write("REST")
		if printSwitch: print("SR 830: Data buffer reset.")

	def readSnapshot(self, printSwitch=True):
		"""Reads the instantaneous value of x and y in (Volt)

		Return Values:
			x: in-phase amplitude in (Volt)
			y: out-of-phase amplitude in (Volt)
		"""

		valList = self.inst.query("SNAP? 1,2")
		x = float(valList[0])
		y = float(valList[1])
		if printSwitch: print("SR 830: Reading instantaneous measurement\nX: %e V\nY: %e V" % (x, y))
		return x, y

	def readDataBuffer(self, chan, printSwitch=True):
		"""Reads the buffer of a given display channel

		Arguments:
			chan: channel to read (1=x, 2=y)
		Return Values:
			arr: array of 4-byte IEEE binary floating point numbers
		"""

		if chan != 1 and chan != 2: raise ValueError("Invalid channel passed to sr830.readBuffer()")
		if printSwitch: print("SR 830: Reading buffer on display channel %d" % chan)
		numDataPts = int(self.inst.query("SPTS?"))
		self.inst.write("TRCB? %d,%d,%d" % (chan, 0, numDataPts))
		data = np.fromstring(self.inst.read_raw(), dtype='<f4')
		return data

	######################################################################################
	######################################################################################
	######################################################################################
	######################################################################################
	######################################################################################
	######################################################################################

	######################################################################################
	
	######################################################################################

##################################################################################################
def indexToSampleRate(index):
	"""Converts an index to the corresponding sample rate in (Hz)
	Note, does not support external triggering as of yet (14)

	Arguments:
		index: sr 830 sample rate index (0 -> 13)
	Return Values:
		rate: sample rate in (Hz)
	"""

	if index in np.arange(14):
		return 2 ** (index - 4)
	else:
		raise ValueError("Invalid index passed to sr830.indexToSampleRate()")

def sampleRateToIndex(rate):
	"""Converts a sample rate in (Hz) to the corresponding programming index command

	Arguments:
		rate: sample rate in (Hz)
	Return Values:
		index: sr 830 sample rate index
	"""

	return np.abs(np.array([indexToSampleRate(index) for index in np.arange(14)]) - rate).argmin()
##################################################################################################
def indexToTimeConstant(index):
	"""Converts an index to the corresponding time constant in (sec)

	Arguments:
		index: sr 830 time constant int (0 -> 19)
	Return values:
		tau: time constant in (sec)
	"""

	if index in np.arange(20):
		if index % 2 == 0: return 1 * 10**(index // 2 - 5)
		if index % 2 == 1: return 3 * 10**(index // 2 - 5)
	else:
		raise ValueError("Invalid index passed to sr830.indexTotimeConstant()")

def timeConstantToIndex(tau):
	"""Converts a time constant in (sec) to the corresponding programming index command

	Arguments:
		tau: time constant in (sec)
	Return Values:
		index: sr 830 time constant index
	"""

	return np.abs(np.array([indexToTimeConstant(index) for index in np.arange(20)]) - tau).argmin()
##################################################################################################
def indexToSensitivity(index):
	"""Converts a sensitivity switch index to a physical sensitivity in (V)

	Arguments:
		index: sr 830 sensitivity index (0 -> 26)
	Return Values:
		sensitivity: physical sensitivity of the lock-in in (V)
	"""
	if index in np.arange(27):
		if index % 3 == 0: return 2 * (10**(index // 3 - 9))
		if index % 3 == 1: return 5 * (10**(index // 3 - 9))
		if index % 3 == 2: return 10 * (10**(index // 3 - 9))
	else:
		raise ValueError("Invalid index passed to sr830.indexToSensitivity()")

def sensitivityToIndex(sense):
	"""Takes a sensitivity in (V) and returns the corresponding programming index

	Arguments:
		sense: sensitivity in (V), needs a specific allowed value
	Return Values:
		index: int that corresponds to the desired sensitivity
	"""

	return np.abs(np.array([indexToSensitivity(index) for index in np.arange(27)]) - sense).argmin()
##################################################################################################
# def checkValidAuxChan(chan):
# 	"""Checks validity of auxiliary channel (1,2,3,4)"""
# 	if chan != 1 and chan != 2 and chan != 3 and chan != 4: raise ValueError("Invalid auxiliary channel")
# def checkValidAuxVolt(volt):
# 	"""Checks validity of auxiliary voltage (-10.5 < volt < +10.5) in (Volts)"""
# 	if abs(volt) > 10.5: raise ValueError("Invalid auxiliary output voltage")

# def inputCoupingToInt(coupling):
# 	"""Converts an input coupling ("AC"/"DC") to an int"""
# 	checkValidInputCoupling(coupling)
# 	if coupling == "AC": return 0
# 	if coupling == "DC": return 1
# def checkValidInputCoupling(coupling):
# 	"""Checks validity of input coupling ("AC"/"DC")"""
# 	if coupling != "AC" and coupling != "DC": raise ValueError("Invalid input coupling")

# def groundingModeToInt(mode):
# 	"""Converts a grounding mode string ("FLOAT"/"GROUND") string to int"""
# 	checkValidGroundingMode(mode)
# 	if mode == False: return 0
# 	if mode == True: return 1
# def checkValidGroundingMode(mode):
# 	"""Checks validity of grounding mode"""
# 	if mode != True and mode != False: raise ValueError("Invalid grounding mode")

# def inputModeToInt(mode):
# 	"""Converts an input mode string ("A"/"A-B") to the corresponding int"""
# 	checkValidInputMode(mode)
# 	if mode == A: return 0
# 	if mode == "A-B": return 1
# def checkValidInputMode(mode):
# 	"""Checks validity of input mode"""
# 	if mode != "A" and mode != "A-B": raise ValueError("Invalid input mode")
##################################################################################################

