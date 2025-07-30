## @file: sec_sweep.py
# @brief: This script does a sweep of the parameter SEC.
# @details:
# @author: Florian Hahn
# @date: 30.07.2025
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
stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec = 0
stresing.settings.camera_settings[drvno].sec_in_10ns = 0
# create an empty list to store the data
list_x = []
list_y1 = []
list_y2 = []
list_y3 = []
list_y4 = []
# plot this pixel
pixel_plot = 588
# this is the reset time at which the sweep starts
start_value = stresing.settings.camera_settings[drvno].sec_in_10ns
# this is the exposure time at which the sweep stops
stop_value = 400
# this is the step size for the first measurements
step_size = 10
measurement_cnt = int((stop_value - start_value) / step_size)

print("Create a measurement with reset time 0")
# Initialize the measurement.
stresing.init_measurement()
# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
stresing.start_measurement_blocking()
# Get all the data in a 2D list
frame_buffer_2d = stresing.copy_all_data_2d(drvno)
# Drop the first 200 samples
frame_buffer_2d = frame_buffer_2d[200:]
# Calculate the 4 averages of every 4th row of frame_buffer_2d
import numpy as np
avg0 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 0], axis=0)
avg1 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 1], axis=0)
avg2 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 2], axis=0)
avg3 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 3], axis=0)
# plot the 4 averages
plt.figure(figsize=(10, 8))
plt.plot(avg0, label='On 1')
plt.plot(avg1, label='On 2')
plt.plot(avg2, label='Off 1')
plt.plot(avg3, label='Off 2')
plt.xlabel('Pixel')
plt.ylabel('Intensity')
plt.title('Average Intensity for each sample type for SEC time 0')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

for i in range(measurement_cnt):
	print("Measurement " + str(i + 1) + " of " + str(measurement_cnt) + ", sensor reset = " + str(stresing.settings.camera_settings[drvno].sec_in_10ns) + " (" + str(stresing.settings.camera_settings[drvno].sec_in_10ns * 10) +" ns)")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	list_x.append(stresing.settings.camera_settings[drvno].sec_in_10ns * 10)
	# Get all the data in a 2D list
	frame_buffer_2d = stresing.copy_all_data_2d(drvno)
	# Drop the first 200 samples
	frame_buffer_2d = frame_buffer_2d[200:]
	# Calculate the 4 averages of every 4th row of frame_buffer_2d
	import numpy as np
	avg0 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 0], axis=0)
	avg1 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 1], axis=0)
	avg2 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 2], axis=0)
	avg3 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 3], axis=0)
	list_y1.append(avg0[pixel_plot])
	list_y2.append(avg1[pixel_plot])
	list_y3.append(avg2[pixel_plot])
	list_y4.append(avg3[pixel_plot])
	stresing.settings.camera_settings[drvno].sec_in_10ns += step_size

# Plot all four lists as separate graphs in one figure
plt.figure(figsize=(10, 8))
plt.plot(list_x, list_y1, label='On 1')
plt.plot(list_x, list_y2, label='On 2')
plt.plot(list_x, list_y3, label='Off 1')
plt.plot(list_x, list_y4, label='Off 2')
plt.xlabel('sec in ns')
plt.ylabel('Intensity at pixel ' + str(pixel_plot))
plt.title('SEC Sweep - Pixel ' + str(pixel_plot))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print("Create a measurement with SEC time " + str(stresing.settings.camera_settings[drvno].sec_in_10ns * 10) + " ns")
# Initialize the measurement.
stresing.init_measurement()
# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
stresing.start_measurement_blocking()
# Get all the data in a 2D list
frame_buffer_2d = stresing.copy_all_data_2d(drvno)
# Drop the first 200 samples
frame_buffer_2d = frame_buffer_2d[200:]
# Calculate the 4 averages of every 4th row of frame_buffer_2d
import numpy as np
avg0 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 0], axis=0)
avg1 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 1], axis=0)
avg2 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 2], axis=0)
avg3 = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 4 == 3], axis=0)
# plot the 4 averages
plt.figure(figsize=(10, 8))
plt.plot(avg0, label='On 1')
plt.plot(avg1, label='On 2')
plt.plot(avg2, label='Off 1')
plt.plot(avg3, label='Off 2')
plt.xlabel('Pixel')
plt.ylabel('Intensity')
plt.title('Average Intensity for each sample type for SEC time ' + str(stresing.settings.camera_settings[drvno].sec_in_10ns * 10) + ' ns')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Exit the driver
stresing.exit_driver()
