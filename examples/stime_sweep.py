## @file: stime_sweep.py
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
# this is the exposure time at which the sweep starts
start_value = stresing.settings.camera_settings[drvno].stime
# do the first measurements with step_size
step_size1_measurement_cnt = 200
# this is the exposure time at which the step size changes
value_step2 = start_value + step_size1_measurement_cnt
# this is the exposure time at which the sweep stops
stop_value = 21000
# this is the step size for the first measurements
step_size = 1
# after the count of measurements of step_size1_measurement_cnt are done change the step size to step_size2
step_size2 = 10
measurement_cnt = int((value_step2 - start_value) / step_size) + int((stop_value - value_step2) / step_size2)

for i in range(measurement_cnt):
	print("Measurement " + str(i + 1) + " of " + str(measurement_cnt) + ", stime = " + str(stresing.settings.camera_settings[drvno].stime) + " µs")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	# Get the data of one frame. Sample settings.nos-1, block 0, camera 0
	frame_buffer = stresing.copy_one_sample(drvno, stresing.settings.nos-1, 0, 0)
	list_x.append(stresing.settings.camera_settings[drvno].stime)
	list_y.append(frame_buffer[pixel_plot])
	if i < step_size1_measurement_cnt:
		stresing.settings.camera_settings[drvno].stime += step_size
	else:
		stresing.settings.camera_settings[drvno].stime += step_size2

# Plot
plt.figure(layout="constrained")
plt.subplot(211)
plt.plot(list_x, list_y)
plt.yscale('linear')
plt.xscale('linear')
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
