# Chris Tang
# agilent33500.py

import visa

##################################################################################################
class Agilent33500():
	def __init__(self, port):
		self.comPort = port
		self.inst = visa.ResourceManager().open_resource(port)

		# Initialize chans to sine waves
		self.setFunc(1, "SIN")
		self.setFunc(2, "SIN")

		# Initialize sync output
		self.setSyncSource(constants.fnGenOutputChan())
		self.setSyncState(True)
		
		self.setDisplay(False)		# Turn off display

		# Optional printing
		print("\nConnecting Agilent 33500 through address:\n%s" % port)
		print("Querying IDN:\n%s" % self.inst.query("*IDN?"))
	######################################################################################
	def setFunc(self, chan, func, printSwitch=True):
		"""Sets chan (1 or 2) to output waveform func"""

		checkValidChan(chan, "agilent33500.setFunc()")
		checkValidFunc(func, "agilent33500.setFunc()")

		if printSwitch: print("Output on chan %d set to: %s" % (chan, func))
		self.inst.write("SOUR%d:FUNC %s" % (chan, func))

	def setOutputState(self, chan, state, printSwitch=True):
		"""Turns output of specified chan (1 or 2) on (True) or off (False)"""

		checkValidChan(chan, "agilent33500.setOutputState()")
		checkValidState(state, "agilent33500.setOutputState()")

		if printSwitch: print("Output %d set to %s" % (chan, boolToStr(state)))
		self.inst.write("OUTP%d %s" % (chan, boolToStr(state)))
	
	def setLoad(self, chan, load, printSwitch=True):
		"""Sets the output load of chan (1 or 2) in (ohms)"""

		checkValidChan(chan, "agilent33500.setLoad()")
		checkValidLoad(load, "agilent33500.setLoad()")

		if load == "INF":
			if printSwitch: print("Output load (chan %d) set to INF" % chan)
			self.inst.write("OUTP%d:LOAD INF" % chan)
		else:
			if printSwitch: print("Output load (chan %d) set to %e" % (chan, load))
			self.inst.write("OUTP%d:LOAD %e" % (chan, load))
	
	def setFreq(self, chan, freq, printSwitch=True):
		"""Sets frequency of chan (1 or 2) to freq in (Hz)"""

		checkValidChan(chan, "agilent33500.setFreq()")
		checkValidFreq(freq, "agilent33500.setFreq()")

		if printSwitch: print("Frequency on chan %d set to: %e Hz" % (chan, freq))
		self.inst.write("SOUR%d:FREQ %e" % (chan, freq))
	
	def setAmp(self, chan, amp, printSwitch=True):
		"""Sets peak-to-peak amplitude of chan (1 or 2) to amp in (Volts)"""

		checkValidChan(chan, "agilent33500.setAmp()")
		checkValidAmp(amp, "agilent33500.setAmp()")

		if printSwitch: print("Vpp on chan %d set to: %e V" % (chan, amp))
		self.inst.write("SOUR%d:VOLT %e" % (chan, amp))
	
	def setOffset(self, chan, offset, printSwitch=True):
		"""Sets DC offset of chan (1 or 2) to offset in (Volts)"""

		checkValidChan(chan, "agilent33500.setOffset()")
		checkValidOffset(offset, "agilent33500.setOffset()")

		if printSwitch: print("DC Offset on chan %d set to: %e V" % (chan, offset))
		self.inst.write("SOUR%d:VOLT:OFFS %e" % (chan, offset))

	def setSyncState(self, state, printSwitch=True):
		"""Turns the sync output on (True) or off (False)"""

		checkValidState(state, "agilent33500.setTrigState()")

		if printSwitch: print("Sync turned %s" % boolToStr(state))
		self.inst.write("OUTP:SYNC %s" % boolToStr(state))

	def setSyncSource(self, chan, printSwitch=True):
		"""Sets the sync to trigger off of channel (1 or 2)"""

		checkValidChan(chan, "agilent33500.setSyncSource()")

		if printSwitch: print("Sync source set to: %d" % chan)
		self.inst.write("OUTP:SYNC:SOUR CH%d" % chan)
	
	def combineChan(self, chan, printSwitch=True):
		"""Combines both channels into the primary chan (1 or 2)"""

		checkValidChan(chan, "agilent33500.combineChan()")

		if printSwitch: print("Channels combined onto primary channel: %d" % chan)
		self.inst.write("SOUR%d:COMB:FEED CH%d" % (chan, (chan % 2) + 1))
	
	def setDisplay(self, state, printSwitch=True):
		"""Turns the display of the function generator on (True) or off (False)"""

		checkValidState(state, "agilent33500.setDisplay()")

		if printSwitch: print("Display turned %s" % boolToStr(state))
		self.inst.write("DISP %s" % boolToStr(state))
	def setSine(self, chan, freq, amp, offset=0, printSwitch=True):
		"""Sets a sine wave on chan (1 or 2) with given:
			frequency in (Hz)
			Vpp amplitude in (Volts)
			dc offset in (volts)
		"""

		checkValidChan(chan, "agilent33500.outputSine()")
		checkValidFreq(freq, "agilent33500.outputSine()")
		checkValidAmp(amp, "agilent33500.outputSine()")
		checkValidOffset(offset, "agilent33500.outputSine()")

		if printSwitch: print("")
		self.setFreq(chan, freq)
		self.setAmp(chan, amp)
		self.setOffset(chan, offset)

		# if printSwitch: print("chan %d outputting Sine Wave:\nFreq: %e Hz\nVpp: %e Volts\nDC Offset: %e Volts" % (chan, freq, amp, offset))
		# self.inst.write("SOUR%d:APPL:SIN %e,%e,%e" (chan, freq, amp, offset))
	######################################################################################

##################################################################################################
def boolToStr(val):
	"""Converts booleans to the strings "ON"/"OFF" """
	if val == True:
		return "ON"
	elif val == False:
		return "OFF"
##################################################################################################
def checkValidChan(chan, methodStr):
	"""Checks validity of chan input (1 or 2)"""
	if chan != 1 and chan != 2: raise ValueError("Invalid chan passed to %s" % methodStr)

def checkValidState(state, methodStr):
	"""Checks validity of state (ON/OFF)"""
	# if False: raise ValueError("Invalid state passed to %s" % methodStr)
	pass

def checkValidFreq(freq, methodStr):
	"""Checks validity of frequency input NOT YET IMPLEMENTED"""
	# if False: raise ValueError("Invalid frequency passed to %s" % methodStr)
	pass

def checkValidAmp(amp, methodStr):
	"""Checks the validity of an amplitude NOT YET IMPLEMENTED"""
	# if False: raise ValueError("Invalid amplitude passed to %s" % methodStr)
	pass

def checkValidOffset(offset, methodStr):
	"""Checks the validity of an offset NOT YET IMPLEMENTED"""
	# if False: raise ValueError("Invalid offset passed to %s" % methodStr)
	pass

def checkValidFunc(func, methodStr):
	"""Checks validity of waveform
	FOR NOW, ONLY PERMITS SINE WAVE
	"""

	if func != "SIN": raise ValueError("Invalid function passed to %s" % methodstr)

def checkValidLoad(load, methodStr):
	"""Checks validity of load NOT YET IMPLEMENTED"""
	# if False: raise ValueError("Invalid load provided to: %s" % methodStr)
	pass

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################


