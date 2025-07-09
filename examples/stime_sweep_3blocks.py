## @file: camera_sweep.py
# @brief: This script does a sweep of the stime parameter.
# @details:
# @author: Florian Hahn
# @date: 07.01.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import stresing

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0
# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
stresing.init_driver()
# Set all settings that are needed for the measurement in config.ini. The file config.ini is also compatible with the exported settings of Escam. Settings that are not found in the file, will be left as default. You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.load_config_file("config.ini")
# create an empty list to store the data
list_x = []
list_y = []
# plot this pixel
pixel_plot = 363

measurement_cnt1 = 30
step_size1 = 100
for i in range(measurement_cnt1):
	print("Range 1: Measurement " + str(i + 1) + " of " + str(measurement_cnt1) + ", stime = " + str(stresing.settings.camera_settings[drvno].stime) + " µs")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	# Get the data of one frame. Sample settings.nos-1, block 0, camera 0
	frame_buffer = stresing.copy_one_sample(drvno, stresing.settings.nos-1, 0, 0)
	list_x.append(stresing.settings.camera_settings[drvno].stime)
	list_y.append(frame_buffer[pixel_plot])
	stresing.settings.camera_settings[drvno].stime += step_size1


measurement_cnt2 = 10 
step_size2= 200
for i in range(measurement_cnt2):
	print("Range 2: Measurement " + str(i + 1) + " of " + str(measurement_cnt2) + ", stime = " + str(stresing.settings.camera_settings[drvno].stime) + " µs")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	# Get the data of one frame. Sample settings.nos-1, block 0, camera 0
	frame_buffer = stresing.copy_one_sample(drvno, stresing.settings.nos-1, 0, 0)
	list_x.append(stresing.settings.camera_settings[drvno].stime)
	list_y.append(frame_buffer[pixel_plot])
	stresing.settings.camera_settings[drvno].stime += step_size2

measurement_cnt3= 25
step_size3 = 1000
for i in range(measurement_cnt3):
	print("Range 3: Measurement " + str(i + 1) + " of " + str(measurement_cnt3) + ", stime = " + str(stresing.settings.camera_settings[drvno].stime) + " µs")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	# Get the data of one frame. Sample settings.nos-1, block 0, camera 0
	frame_buffer = stresing.copy_one_sample(drvno, stresing.settings.nos-1, 0, 0)
	list_x.append(stresing.settings.camera_settings[drvno].stime)
	list_y.append(frame_buffer[pixel_plot])
	stresing.settings.camera_settings[drvno].stime += step_size3

# Plot
plt.figure(layout="constrained")
# ****************************************************************
plt.suptitle("FLCC3010-FFT S9037-0902 ")
plt.subplot(211)
plt.plot(list_x, list_y)
plt.xscale('linear')
plt.yscale('linear')
#plt.ylim(0, 20000) #14 bit
plt.ylim(0, 70000)  #16 bit
plt.xlabel('stime in µs')
plt.title('linear')
plt.grid(True)

plt.subplot(212)
plt.plot(list_x, list_y)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('stime in µs')
plt.title('log')
plt.grid(True)
plt.show()

# Exit the driver
stresing.exit_driver()
