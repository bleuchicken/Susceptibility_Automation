# Chris Tang
# lockinData.py

import sr830
import time
import numpy as np

##################################################################################################
def takeData(lockin, sampleTime, printSwitch=True):
	"""Takes data for a given time

	Arguments:
		lockin: instance of sr830 class
		sampleTime: time to take data
	Return Values:
		t: time array with units of (sec)
		x: in-phase amplitude array with units of (Volt)
		y: out-of-phase amplitude array with units of (Volt)
	"""

	if printSwitch: print("Now taking lockin data for %d secs\nCurrent time:" % sampleTime)
	if printSwitch: print(time.asctime( time.localtime(time.time()) ))
	if printSwitch: print("Predicted finish time:")
	if printSwitch: print(time.asctime( time.localtime(time.time() + sampleTime) ))

	lockin.stopDataStorage()
	lockin.resetDataBuffer()
	lockin.startDataStorage()
	time.sleep(sampleTime)
	lockin.stopDataStorage()
	x = lockin.readDataBuffer(chan=1)
	y = lockin.readDataBuffer(chan=2)
	t = np.arange(len(x)) * (1 / lockin.getSampleRate())
	if printSwitch: print("%d data points acquired." % len(x))
	return t, x, y

##################################################################################################
##################################################################################################
##################################################################################################