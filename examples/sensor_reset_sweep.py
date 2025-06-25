## @file: sensor_reset_sweep.py
# @brief: This script does a sweep of the parameter sensor reset.
# @details:
# @author: Florian Hahn
# @date: 25.06.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import stresing

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0

# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.settings.board_sel = 1
stresing.settings.nos = 1000
stresing.settings.nob = 1
stresing.settings.camera_settings[drvno].sti_mode = 4
stresing.settings.camera_settings[drvno].bti_mode = 4
stresing.settings.camera_settings[drvno].SENSOR_TYPE = 5
# 0=PDA , 1=IR, 2=FFT, 3=CMOS, 4=HSVIS, 5=HSIR
stresing.settings.camera_settings[drvno].CAMERA_SYSTEM = 2
#0=3001, 1=3010, 2=3030
stresing.settings.camera_settings[drvno].CAMCNT = 1
stresing.settings.camera_settings[drvno].PIXEL = 1024
stresing.settings.camera_settings[drvno].stime_in_microsec = 40
stresing.settings.camera_settings[drvno].btime_in_microsec = 10
stresing.settings.camera_settings[drvno].dac_output[0][0] = 55256
stresing.settings.camera_settings[drvno].dac_output[0][1] = 55291
stresing.settings.camera_settings[drvno].dac_output[0][2] = 55538
stresing.settings.camera_settings[drvno].dac_output[0][3] = 55335
stresing.settings.camera_settings[drvno].dac_output[0][4] = 55194
stresing.settings.camera_settings[drvno].dac_output[0][5] = 55364
stresing.settings.camera_settings[drvno].dac_output[0][6] = 55333
stresing.settings.camera_settings[drvno].dac_output[0][7] = 55248
stresing.settings.camera_settings[drvno].adc_gain = 6
stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec = 0

# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
stresing.init_driver()
# create an empty list to store the data
list_x = []
list_y = []
# plot this pixel
pixel_plot = 363
# this is the reset time at which the sweep starts
start_value = stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec
# this is the exposure time at which the sweep stops
stop_value = 8000
# this is the step size for the first measurements
step_size = 100
measurement_cnt = int((stop_value - start_value) / step_size)

for i in range(measurement_cnt):
	print("Measurement " + str(i + 1) + " of " + str(measurement_cnt) + ", sensor reset = " + str(stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec) + " (" + str(stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec * 4) +" ns)")
	# Initialize the measurement.
	stresing.init_measurement()
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	# Get the data of one frame. Sample settings.nos-1, block 0, camera 0
	frame_buffer = stresing.copy_one_sample(drvno, stresing.settings.nos-1, 0, 0)
	list_x.append(stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec)
	list_y.append(frame_buffer[pixel_plot])
	stresing.settings.camera_settings[drvno].sensor_reset_or_hsir_ec += step_size

# Plot
plt.figure(layout="constrained")
plt.subplot(211)
plt.plot(list_x, list_y)
plt.yscale('linear')
plt.xscale('linear')
plt.xlabel('sensor reset in ns')
plt.title('linear')
plt.grid(True)

plt.subplot(212)
plt.plot(list_x, list_y)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('sensor reset in ns')
plt.title('log')
plt.grid(True)
plt.show()

# Exit the driver
stresing.exit_driver()
