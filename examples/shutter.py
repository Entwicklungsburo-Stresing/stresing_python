## @file: shutter.py
# @brief: This script is closing and opening all shutters 10 times once per second.
# @details:
# @author: Florian Hahn
# @date: 19.06.2025
# @copyright: Copyright (c) 202, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

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