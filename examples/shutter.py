## @file: camera.py
# @brief: This script shows how to operate the Stresing camera using the DLL interface.
# @details: This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board. This python example was created with DLL version 4.18.0
# @author: Florian Hahn
# @date: 13.10.2022
# @copyright: Copyright (c) 2022, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import time
import stresing

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0

stresing.init_driver()

# Loop for closing and opening all shutters 10 times once per second
for i in range(10):
	print("Open")
	# Set all shutters to open
	stresing.set_shutter_states(drvno, 0)
	
	# Wait for 1 second
	time.sleep(1)

	print("Close")
	# Set all shutters to closed
	# 15 = 0b00001111, which means all shutters are set to open
	stresing.set_shutter_states(drvno, 15)

	# Wait for 1 second
	time.sleep(1)

# Exit the driver
stresing.exit_driver()