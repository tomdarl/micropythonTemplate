import pyb
import _thread

from BNO055 import BNO055

# -----------------------------------------------------------------------------
# Global Objects
# -----------------------------------------------------------------------------

# BNO055
i2c = pyb.I2C(2, pyb.I2C.MASTER)
# I2C configured to use I2c driver 2 
#	SDA = pyb Y10
# 	SCL = pyb Y9
bno = BNO055(i2c)

blueLED = pyb.LED(4)

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def ledRunningFlash():
	'''
	toggles the blue LED to show pyb is running

	waits for 5 seconds then toggle LED indefinitely 
	'''
	pyb.delay(5000)
	while True:
		blueLED.toggle()
		pyb.delay(500)


def printOrientation(period_ms=1000):
	'''
	prints the orientation of the BNO055 at designated rate
	'''

	# bno operates at 100Hz in sensor fusion mode
	d = 10 if period_ms < 10 else period_ms

	while True:
		print(bno.quaternion())
		pyb.delay(d)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# detatch threads
_thread.start_new_thread(ledRunningFlash, [])
_thread.start_new_thread(printOrientation, [500])

# main ends, threads continue
