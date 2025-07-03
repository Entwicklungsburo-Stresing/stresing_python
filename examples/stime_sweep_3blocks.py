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

# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.settings.board_sel = 1
stresing.settings.nos = 10
stresing.settings.nob = 1
stresing.settings.camera_settings[drvno].sti_mode = 4
stresing.settings.camera_settings[drvno].bti_mode = 4
stresing.settings.camera_settings[drvno].SENSOR_TYPE = 3
# 0=PDA , 1=IR, 2=FFT, 3=CMOS, 4=HSVIS, 5=HSIR
stresing.settings.camera_settings[drvno].CAMERA_SYSTEM = 1
#0=3001, 1=3010, 2=3030
stresing.settings.camera_settings[drvno].CAMCNT = 2
stresing.settings.camera_settings[drvno].PIXEL = 1088
stresing.settings.camera_settings[drvno].stime = 541
stresing.settings.camera_settings[drvno].btime = 10
stresing.settings.camera_settings[drvno].fft_mode = 0
stresing.settings.camera_settings[drvno].FFT_LINES = 64
stresing.settings.camera_settings[drvno].lines_binning = 1
stresing.settings.camera_settings[drvno].number_of_regions = 5
stresing.settings.camera_settings[drvno].region_size[0] = 10
stresing.settings.camera_settings[drvno].region_size[1] = 50
stresing.settings.camera_settings[drvno].region_size[2] = 10
stresing.settings.camera_settings[drvno].region_size[3] = 50
stresing.settings.camera_settings[drvno].region_size[4] = 8
stresing.settings.camera_settings[drvno].use_software_polling = 0
stresing.settings.camera_settings[drvno].VFREQ = 3
stresing.settings.camera_settings[drvno].dac_output[0][0] = 53256
stresing.settings.camera_settings[drvno].dac_output[0][1] = 53291
stresing.settings.camera_settings[drvno].dac_output[0][2] = 53538
stresing.settings.camera_settings[drvno].dac_output[0][3] = 53335
stresing.settings.camera_settings[drvno].dac_output[0][4] = 53194
stresing.settings.camera_settings[drvno].dac_output[0][5] = 53364
stresing.settings.camera_settings[drvno].dac_output[0][6] = 53333
stresing.settings.camera_settings[drvno].dac_output[0][7] = 53248
stresing.settings.camera_settings[drvno].adc_gain = 6

# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
stresing.init_driver()
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
