# Micropython Template Repo

Template for using the micropython pyboard with the BNO055 over I2C.
This project uses a pyb with theadding enabled. 

## Within the Repo

* `main.py`  -> example main 
* `_drivers/` -> dir of common files 
* `flash.sh` -> script to flash pyb

## Use

Create a top level file.
An example of main.py has been included.
Then use the `flash.sh` script 

```
	./flash.sh <TopLevelFile.py> [-u]
```
To use the script, pass the top level file as the first arguement.
This will save a copy of the top level to the pyb as `main.py` and also flash the contence of `_drivers`. 
`-u` is used for automatically unmounting the SD card.

Once flashed, the pyb requires restarting. 
To do this, boot.py defines `reset()`. 
This allows for the REPL to restart the board without closing screen or unmounting the SD card. 
Upon rebooting, the pyb uses the updated files and runs the top level file. 

## To access REPL 

REPL is Read Evaluate Print Loop, i.e. a live terminal on the pyb. 
To access, plug in the pyb over usb and...

for mac:
```
	screen /dev/tty.usbmodem*
```

for linux:
```
	screen /dev/ttyACM0
```
