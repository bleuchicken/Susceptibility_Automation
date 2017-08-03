# Chris Tang
# lakeshore372.py

import visa

##################################################################################################
class Lakeshore372():
	def __init__(self, port):
		self.port = port
		self.inst = visa.ResourceManager().open_resource(port)

		# self.setLedState(False)			# Turn off front panel LEDs

		# Optional printing
		print("\nConnecting Lakeshore 372 through address:\n%s" % port)
		print("Querying IDN:\n%s" % self.inst.query("*IDN?"))

	######################################################################################
	def setCalibrationCurve(self, chan, curveNum, printSwitch=True):
		"""Sets the calibration curve for a given channel

		Arguments:
			chan: channel to configure 
				0: control input
				1-16: measurement inputs
			curveNum: calibration curve number
		"""

		if chan == 0:
			self.inst.write("INCRV A,%d" % curveNum)
			if printSwitch: print("Lakeshore 372: Calibration curve #%d set to input channel: A" % curveNum)
		else:
			self.inst.write("INCRV %d,%d" % (chan, curveNum))
			if printSwitch: print("Lakeshore 372: Calibration curve #%d set to input channel: %d" % (chan, curveNum))

	# NEED TO DO
	def setExcFreq(self, chan, freq, printSwitch=True):
		"""Sets the excitation frequency of a given channel"""
		raise NotImplementedError

	def setFilter(self, chan, state, settleTime, window, printSwitch=True):
		"""Sets the filter parameters for a given channel

		Arguments:
			chan: input channel (1-16 = measurements, or 0 = control)
			state: boolean that turns filter on (True) or off (False)
			settleTime: filter settle time in (sec) (1-200 acceptable range)
			window: % of full scale window in (%)
		"""

		if chan == 0:
			self.inst.write("FILTER A,%d,%d,%d" % (boolToInt(state), settleTime, window))
			if printSwitch: 
				if state: 
					print("Lakeshore 372: Filter on channel A turned ON")
				else:
					print("Lakeshore 372: Fitler on channel A turned OFF")
		else:
			self.inst.write("FILTER %d,%d,%d,%d" % (chan, boolToInt(state), settleTime, window))
			if printSwitch: 
				if state: 
					print("Lakeshore 372: Filter on channel %d turned ON" % chan)
				else:
					print("Lakeshore 372: Fitler on channel %d turned OFF" % chan)

	# NEED TO DO
	def setInput(self, chan, excMode, excRange, autoRange, range, shunt, units, printSwitch=True):
		"""Configures an input

		Arguments:
			chan: 
			excMode: 
			excRange: 
			autoRange: 
			range: 
			shunt: 
			units: 
		"""
		raise NotImplementedError

	def setTemp(self, output, temp, printSwitch=True):
		"""Sets a temperature setpoint in (K)

		Arguments:
			output: selects sample heater (0) or warm-up heater (1)
			temp: desired temperature setpoint in (K)
		"""

		self.inst.write("SETP %d,%e" % (output, temp))
		if printSwitch: 
			if output == 0:
				print("Lakeshore 372: Sample heater setpoint: %e K" % temp)
			elif output == 1:
				print("Lakeshore 372: Warm-up heater setpoint: %e K" % temp)
	
	def setPid(self, output, p, i, d, printSwitch=True):
		"""Sets the parameters for the PID loop

		Arguments:
			output: chooses sample heater (0) or warm-up heater (1)
			p: proportional gain parameter (0 -> 1e3)
			i: integral reset parameter (0 -> 1e4)
			d: derivative rate parameter (0 -> 2500)
		"""

		self.inst.write("PID %d,%d,%d,%d" % (output, int(p), int(i), int(d)))
		if printSwitch: 
			if output == 0:
				print("Lakeshore 372: PID parameters set on sample heater:\nP: %d\nI: %d\nD: %d" (int(p), int(i), int(d)))
			elif output == 1:
				print("Lakeshore 372: PID parameters set on warm-up heater:\nP: %d\nI: %d\nD: %d" (int(p), int(i), int(d)))

	def readTemp(self, chan):
		"""Reads the temperature value in (K) from a given channel

		Arguments:
			chan: channel to read (1-16 = measurement, 0 = control)
		Return Values:
			temp: measured temperature in (Kelvin)
		"""

		if chan == 0:
			temp = self.inst.query("KRDG?A")
			if printSwitch: print("Lakeshore 372: Temperature of channel A: %e K" % temp)
			return temp
		else:
			temp = self.inst.query("KRDG?%d" % chan)
			if printSwitch: print("Lakeshore 372: Temperature of channel %d: %e K" % (chan, temp))
			return temp

	######################################################################################

##################################################################################################
def checkValidBooleanMode(mode):
		"""Checks validity of on/off mode"""
		if mode != True and mode != False: raise ValueError("Invalid (boolean) mode passed")
def boolToInt(val):
	"""Converts a boolean to appropriate integer"""
	checkValidBooleanMode(mode)
	if val == True:
		return 1
	if val == False:
		return 0
##################################################################################################

##################################################################################################