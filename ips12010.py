# Chris Tang
# ips12010.py

import visa
import time

##################################################################################################
class IPS12010():
	def __init__(self, port):
		self.port = port
		self.inst = visa.ResourceManager().open_resource(port)

		self.setInputMode("remoteAndUnlocked")

		# Optional printing
		print("\nConnecting IPS 120-10 through address:\n%s" % port)
		print("Querying IDN:\n%s" % self.inst.query("*IDN?"))
	######################################################################################
	def setHeater(self, mode, heatTime, coolTime, printSwitch=True):
		"""Turns the switch heater on (True) or off (False) and waits for heater to heat/cool

		Arguments:
			mode: boolean that determines whether to turn the heater on (True) or off (False)
			heatTime: Time to wait for switch to heat up in (secs)
			coolTime: Time to wait for the switch to cool in (secs)
		"""

		if mode:
			self.inst.write("$H1") 		# Note: NEVER use command H2, which overrides the persistent/output current check
			if printSwitch: print("IPS 120-10: Switch heater turned ON\nNow waiting %d sec for S.C. switch to heat up ..." % heatTime)
			time.sleep(heatTime)
			if printSwitch: print("Wait time completed.")
		elif not mode:
			self.inst.write("$H0")
			if printSwitch: print("IPS 120-10: Switch heater turned OFF\nNow waiting %d sec for S.C. switch to cool ..." % coolTime)
			time.sleep(coolTime)
			if printSwitch: print("Wait time completed.")
		else:
			raise ValueError("Invalid mode passed to ips12010.setHeater()")

	def setOutputCurrent(self, current, refreshTime, printSwitch=True):
		"""Sets the output current to a target in (Amp), rAmp to that target, then waits for the action to be completed

		Arguments:
			current: target current to which to ramp in (Amp)
		"""

		self.inst.write("$I%.4f" % current)
		if printSwitch: print("IPS 120-10: Output current set point: %.4f Amp" % current)

		self.setRampRate(acceptableRampRate(current))

		self.inst.write("$A1")
		if printSwitch: print("IPS 120-10: Now ramping to set point...")

		self.waitUntilStable(refreshTime)

		self.inst.write("$A0")
		if printSwitch: print("IPS 120-10: Output mode: HOLD")
	
	def rampToZero(self, refreshTime, printSwitch=True):
		"""RAmp the magnet supply to zero, waits for it to be at rest, and then holds"""

		self.inst.write("$I0")
		if printSwitch: print("IPS 120-10: Output current set point: 0 Amp")

		self.inst.write("$A2")
		if printSwitch: print("IPS 120-10: Now ramping zero...")

		self.waitUntilStable(refreshTime)

		self.inst.write("$A0")
		if printSwitch: print("IPS 120-10: Output mode: HOLD")
	
	def setRampRate(self, rate, printSwitch=True):
		"""Sets the ramp rate of the magnet in (Amp / min)

		Arguments:
			rate: desired ramp rate in (Amp / min)
		"""

		self.inst.write("$S%.3f" % rate)
		if printSwitch: print("IPS 120-10: Ramp Rate set to: %.2f Amp/min" % rate)
	######################################################################################
	def setInputMode(self, mode):
		"""Sets the input mode

		Arguments:
			mode: input mode to be commanded 
				"remoteAndUnlocked": Sets IPS power supply to remote and unlocked mode
		"""

		if mode == "remoteAndUnlocked":
			self.inst.write("$C3")
			if printSwitch: print("IPS 120-10: Set to Remote and Unlocked")
		else:
			raise ValueError("Invalid mode passed to ips12010.setInputMode")

	def setResolution(self, resolution):
		"""Sets the resolution
		
		Arguments
			resolution: determines the resolution of the magnet field/current
				"normal": 0.001 Amp resolution
				"extended": 0.0001 Amp resolution
		"""

		if resolution == "normal":
			self.inst.write("$Q0")
			if printSwitch: print("IPS 120-10: Set to Normal Resolution")
		elif resolution == "extended":
			self.inst.write("$Q4")
			if printSwitch: print("IPS 120-10: Set to Extended Resolution")
		else:
			raise ValueError("Invalid resolution passed to ips12010.setResolution()")
	######################################################################################
	def getPersistentCurrent(self, printSwitch=True):
		"""Querys/returns the persistent current in (Amp) from the magnet power supply"""

		persistentCurrent = float(self.inst.query("R 16"))
		if printSwitch: print("IPS 120-10: Persistent current: %.4f Amp" % persistentCurrent)
		return persistentCurrent

	def getOutputCurrent(self, printSwitch=True):
		"""Querys/returns the output current in (Amp) from the magnet power supply"""

		outputCurrent = float(self.inst.query("R 2"))
		if printSwitch: print("IPS 120-10: Output current: %.4f Amp" % outputCurrent)
		return outputCurrent
	
	def heaterIsOn(self, printSwitch=True):
		"""Queries the heater status, and returns whether heater is on or off

		Return Values:
			status: True if heater is on, False otherwise
		"""

		statusStr = self.inst.query("X")
		heaterChar = statusStr[8]
		if heaterChar == '1':
			if printSwitch: print("IPS 120-10: Heater status: ON")
			return True
		else:
			if printSwitch: print("IPS 120-10: Heater status: OFF")
			return False
	######################################################################################
	def waitUntilStable(self, refreshTime, printSwitch=True):
		"""Periodically queries the magnet status until it is at rest

		Arguments:
			refreshTime: delay time in (sec) to wait between queries
		"""

		# IMPLEMENT TIMEOUT TIME???
		print("WARNING: Timeout not implemented for ips12010.waitUntilStable()")

		time.sleep(5)		# Wait a fixed time so that status can update to sweeping before querying

		while not self.isAtRest():
			time.sleep(refreshTime)

		if printSwitch: print("IPS 120-10: Power supply is AT REST")
		return True

	def isAtRest(self):
		"""Queries the magnet power supply status and returns True/False if the power supply is at rest or not"""

		statusStr = self.inst.query("X")			# Examine returns a string that must be parsed
		if statusStr[11] == '0': return True		# Parse the string for the magnet status
		return False
	######################################################################################
	def checkOutputPersistentMatchedCurrent(self, tolerance, printSwitch=True):
		"""Checks whether the output current and the persistent current match, to within the tolerance

		Arguments:
			tolerance: tolerance as a fraction of output current for deciding whether currents match
		"""

		outputCurrent = self.getOutputCurrent()
		persistentCurrent = self.getPersistentCurrent()

		if abs(outputCurrent - persistentCurrent) < tolerance * outputCurrent:
			if printSwitch: print("IPS 120-10: Output current matches persistent current to within %.2f %%" % tolerance*100)
			return True
		else:
			raise Exception("\nERROR ERROR ERROR ERROR\nMAGNET PERSISTENT CURRENT DOES NOT MATCH OUTPUT CURRENT\nERROR ERROR ERROR ERROR")
##################################################################################################
def acceptableRampRate(current):
	"""Returns an acceptable ramp rate in (Amp / min) for a given target current

	Arguments:
		field: target field in (Tesla)
	Return Values:
		rate: ramp rate in (Amp / min)
			1 Amp/min for current < 57 Amp (~6 Tesla)
			0.5 Amp/min for current >= 57 Amp (~6 Tesla)
	"""

	if abs(current) < 57: 
		return 1.
	else:
		return 0.5
##################################################################################################

