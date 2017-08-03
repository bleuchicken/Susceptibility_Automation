# Chris Tang
# pumpProbe.py

import agilent33500

##################################################################################################
# Parameters

# Pump frequency in (Hz)
PUMP_FREQ = 202

# Susceptometer Impedance in (Ohm)
SUSCEPTOMETER_IMPEDANCE = None

# Pump Channel
PUMP_CHAN = 1
# Probe Channel
PROBE_CHAN = 2
##################################################################################################
def setPumpFreq(fnGen, freq):
	"""Sets the pump frequency in (Hz)

	Arguments:
		fnGen: instance of Agilent33500 class
		freq: frequency in (Hz)
	"""

	fnGen.setFreq(chan=PUMP_CHAN, freq=freq)

def setProbeFreq(fnGen, freq, printSwitch=True):
	"""Sets the probe frequency in (Hz)

	Arguments:
		fnGen: instance of Agilent33500 class
		freq: frequency in (Hz)
	"""

	fnGen.setFreq(chan=PROBE_CHAN)
##################################################################################################
def setPumpAmp(fnGen, amp):
	"""Sets the peak-to-peak amplitude of the pump in (Volt)

	Arguments:
		fnGen: instance of Agilent33500 class
		amp: peak-to-peak amplitude in (Volt)
	"""

	fnGen.setAmp(chan=PUMP_CHAN, amp=amp)

def setProbeAmp(fnGen, amp):
	"""Sets the peak-to-peak amplitude of the probe in (Volt)

	Arguments:
		fnGen: instance of Agilent33500 class
		amp: peak-to-peak amplitude in (Volt)
	"""

	fnGen.setAmp(chan=PROBE_CHAN, amp=amp)
##################################################################################################