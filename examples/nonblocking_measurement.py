## @file: nonblocking_measurement.py
# @brief: This script shows how to operate the Stresing camera using the python module stresing.
# @details: This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board.
# @author: Florian Hahn
# @date: 13.10.2022
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import stresing
# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import time

# Initialize the driver.
number_of_boards = stresing.init_driver()
# Set all settings that are needed for the measurement in config.ini. The file config.ini is also compatible with the exported settings of Escam. Settings that are not found in the file, will be left as default. You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.load_config_file("config.ini")
# Initialize the measurement.
stresing.init_measurement()
# Start the measurement. This is the nonblocking call, which means it will return immediately. 
stresing.start_measurement_nonblocking()
cur_sample = -2
cur_block = -2
# Always use board 0. There is only one PCIe board in this example script.
drvno = 0
while cur_sample < stresing.settings.nos-1 or cur_block < stresing.settings.nob-1:
	(cur_sample, cur_block) = stresing.get_current_scan_number(drvno)
	print("sample: "+str(cur_sample)+" block: "+str(cur_block))
	time.sleep(1)
frame_buffer = stresing.copy_one_sample(drvno, 5, 0 ,0)
# Plot the frame
plt.plot(frame_buffer)
plt.show()
# Exit the driver
stresing.exit_driver()
