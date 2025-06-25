## @file: camera_plot_rms.py
# @brief: This script does a sweep of the stime parameter.
# @details: This python example was created with DLL version 4.18.0
# @author: Florian Hahn
# @date: 25.02.2025
# @copyright: Copyright (c) 2022, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import stresing

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0

# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.settings.board_sel = 1
stresing.settings.nos = 10000
stresing.settings.nob = 1
stresing.settings.camera_settings[drvno].sti_mode = 4
stresing.settings.camera_settings[drvno].bti_mode = 4
stresing.settings.camera_settings[drvno].SENSOR_TYPE = 4
stresing.settings.camera_settings[drvno].CAMERA_SYSTEM = 2
stresing.settings.camera_settings[drvno].CAMCNT = 1
stresing.settings.camera_settings[drvno].PIXEL = 1024
stresing.settings.camera_settings[drvno].stime_in_microsec = 10
stresing.settings.camera_settings[drvno].btime_in_microsec = 100000
stresing.settings.camera_settings[drvno].use_software_polling = 0
stresing.settings.camera_settings[drvno].dac_output[0][0] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][1] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][2] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][3] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][4] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][5] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][6] = 55000
stresing.settings.camera_settings[drvno].dac_output[0][7] = 55000

# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
stresing.init_driver()
# Initialize the measurement.
stresing.init_measurement()

# Number of data points of RMS values
measurement_cnt = 100
rms_pixel = 100
rms_list = []

for i in range(measurement_cnt):
	print("Measurement " + str(i+1) + " of " + str(measurement_cnt))
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	stresing.start_measurement_blocking()
	(mean, trms) = stresing.calc_trms(drvno, 10, stresing.settings.nos - 1, rms_pixel, 0)
	rms_list.append(trms)

# Plot the frame
plt.plot(rms_list)
plt.show()
# Exit the driver
stresing.exit_driver()
