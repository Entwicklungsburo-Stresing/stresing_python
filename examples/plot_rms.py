## @file: plot_rms.py
# @brief: This script does a sweep of the stime parameter.
# @details:
# @author: Florian Hahn
# @date: 25.02.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import stresing

# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
stresing.init_driver()
# Set all settings that are needed for the measurement in config.ini. The file config.ini is also compatible with the exported settings of Escam. Settings that are not found in the file, will be left as default. You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.load_config_file("config.ini")
# Initialize the measurement.
stresing.init_measurement()
# Number of data points of RMS values
measurement_cnt = 100
rms_pixel = 100
rms_list: list[float] = []
# Always use board 0. There is only one PCIe board in this example script.
drvno = 0
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
