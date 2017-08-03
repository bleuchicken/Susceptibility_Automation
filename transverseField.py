# Chris Tang
# transverseField.py

import ips12010
import sr830
import math
import time

##################################################################################################
# Main Magnet Parameters

# Constant that converts main magnet current to field in units of (Tesla / Amp)
AMI_3_INCH_8_TESLA_SOLENOID_FIELD_PER_CURRENT = 0.10411
##################################################################################################
# Compensation Coil Parameters

# Constant that converts between input voltage and output current in (Amp / Volt)
COMP_COIL_CURRENT_PER_VOLTAGE = 2.08
# Constant that converts compensation coil magnet current to field in units of (Tesla / Amp)
COMP_COIL_FIELD_PER_CURRENT = None
# Aux channel on SR 830 lockin that's connected to compensation coil
COMP_COIL_CHAN = 1
# Tilt angle of sample to solenoid in (Rad)
TRANSVERSE_FIELD_TILT_ANGLE = None
##################################################################################################
# Software Tolerances/Delay Times

# Time to wait in (sec) for the S.C. switch to heat up after activating the heater
MAGNET_HEAT_TIME = 30
# Time to wait in (sec) for the S.C. switch to cool after deactivating the heater
MAGNET_COOL_TIME = 60
# Time to wait in (sec) between queries for the magnet to be at rest
MAGNET_REFRESH_TIME = 1
# Tolerance as a fraction of output current to check whether the output and persistent currents match
MAGNET_TOLERANCE = 0.05
##################################################################################################
def setTransverseField(magSupply, lockin, field):
	"""Sets the transverse field in (Tesla)
	Also drives the compensation coil for tilt-correction

	Arguments:
		magSupply: IPS12010 instance that's connected to the power supply you're using
		field: transverse field strength in (Tesla)
	"""

	# Initialize magnet supply
	magSupply.setInputMode(mode="remoteAndUnlocked")
	magSupply.setResolution(resolution="normal")

	# Turn switch heater off
	magSupply.setHeater(mode=False, heatTime=MAGNET_HEAT_TIME, coolTime=MAGNET_COOL_TIME)

	# Match output current to persistent current
	magSupply.setOutputCurrent(current=magSupply.getPersistentCurrent(), refreshTime=MAGNET_REFRESH_TIME)

	# IF THE OUTPUT CURRENT DOESN'T MATCH THE PERSISTENT CURRENT
	# WITH THE SWITCH HEATER ON, SOMETHING IS VERY WRONG
	magSupply.checkOutputPersistentMatchedCurrent(tolerance=MAGNET_TOLERANCE)

	# Turn switch heater on
	magSupply.setHeater(mode=True, heatTime=MAGNET_HEAT_TIME, coolTime=MAGNET_COOL_TIME)

	# Make sure heater is on
	time.sleep(5)
	if not magSupply.heaterIsOn(): raise Exception("Heater did not turn on successfully")

	# Set output current to new target
	magSupply.setOutputCurrent(current=(field / AMI_3_INCH_8_TESLA_SOLENOID_FIELD_PER_CURRENT), refreshTime=MAGNET_REFRESH_TIME)

	# Turn heater off to go back into persistent mode
	magSupply.setHeater(mode=False)

	# Output current on compensation coil to correct for tilt angle
	lockin.setAuxOutput(chan=COMP_COIL_CHAN, volt=transverseFieldToCompCoilVolt(transverseField, tiltAngle=TRANSVERSE_FIELD_TILT_ANGLE, compCoilFieldPerCurrent=COMP_COIL_FIELD_PER_CURRENT, compCoilCurrentPerVoltage=COMP_COIL_CURRENT_PER_VOLTAGE))

	# Ramp output current to zero and hold
	magSupply.rampToZero(refreshTime=MAGNET_REFRESH_TIME)
##################################################################################################
def transverseFieldToCompCoilVolt(transverseField, tiltAngle, compCoilFieldPerCurrent, compCoilCurrentPerVoltage):
	"""Converts a transverse field value to a required aux drive voltage

	Arguments:
		transverseField: value of main magnet transverse field in (Tesla)
		tiltAngle: value of the angle between the normal to the sample Ising axis and the transverse field in (Rad)
		compCoilFieldPerCurrent: constant of proportionality between coil field and current in (Tesla / Amp)
		compCoilCurrentPerVoltage: constant of proportionality between comp coil power supply voltage and current in (Amp / Volt)
	Return Values:
		volt: required output aux voltage in (Volts)
	"""

	compCoilField = math.sin(tiltAngle) * transverseField
	compCoilCurrent = compCoilField / compCoilFieldPerCurrent
	compCoilVolt = compCoilCurrent / compCoilCurrentPerVoltage
	return compCoilVolt
##################################################################################################
