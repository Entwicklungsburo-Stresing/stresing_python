## @file: camera.py
# @brief: This script shows how to operate the Stresing camera using the DLL interface.
# @details: This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board. This python example was created with DLL version 4.18.0
# @author: Florian Hahn
# @date: 13.10.2022
# @copyright: Copyright (c) 2022, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import stresing
# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import time

# Initialize the driver.
number_of_boards = stresing.init_driver()

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0

# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.settings.board_sel = 1
stresing.settings.nos = 1000
stresing.settings.nob = 1
stresing.settings.camera_settings[drvno].sti_mode = 4
stresing.settings.camera_settings[drvno].bti_mode = 4
stresing.settings.camera_settings[drvno].SENSOR_TYPE = 4
stresing.settings.camera_settings[drvno].CAMERA_SYSTEM = 2
stresing.settings.camera_settings[drvno].CAMCNT = 1
stresing.settings.camera_settings[drvno].PIXEL = 1088
stresing.settings.camera_settings[drvno].stime_in_microsec = 1000
stresing.settings.camera_settings[drvno].btime_in_microsec = 100000
stresing.settings.camera_settings[drvno].fft_mode = 1
stresing.settings.camera_settings[drvno].FFT_LINES = 128
stresing.settings.camera_settings[drvno].lines_binning = 1
stresing.settings.camera_settings[drvno].number_of_regions = 5
stresing.settings.camera_settings[drvno].region_size[0] = 10
stresing.settings.camera_settings[drvno].region_size[1] = 50
stresing.settings.camera_settings[drvno].region_size[2] = 10
stresing.settings.camera_settings[drvno].region_size[3] = 50
stresing.settings.camera_settings[drvno].region_size[4] = 8
stresing.settings.camera_settings[drvno].use_software_polling = 0
stresing.settings.camera_settings[drvno].VFREQ = 7
stresing.settings.camera_settings[drvno].dac_output[0][0] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][1] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][2] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][3] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][4] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][5] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][6] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][7] = 55000

# Initialize the measurement.
stresing.init_measurement()
# Start the measurement. This is the nonblocking call, which means it will return immediately. 
stresing.start_measurement_nonblocking()

cur_sample = -2
cur_block = -2

while cur_sample < stresing.settings.nos-1 or cur_block < stresing.settings.nob-1:
	(cur_sample, cur_block) = stresing.get_current_scan_number(drvno)
	print("sample: "+str(cur_sample)+" block: "+str(cur_block))
	time.sleep(1)
	

frame_buffer = stresing.copy_one_sample(drvno, 5, 0 ,0)
# Plot the frame
plt.plot(frame_buffer)
plt.show()

# Exit the driver
status = stresing.exit_driver()