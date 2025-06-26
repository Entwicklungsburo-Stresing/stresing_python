## @file: simple_blocking_measurement.py
# @brief: This script shows how to operate the Stresing camera using the python module stresing.
# @details: This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board.
# @author: Florian Hahn
# @date: 13.10.2022
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import stresing
# matplotlib is used for the data plot
import matplotlib.pyplot as plt

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
stresing.settings.camera_settings[drvno].PIXEL = 1024
stresing.settings.camera_settings[drvno].stime_in_microsec = 10
stresing.settings.camera_settings[drvno].btime_in_microsec = 100000
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
# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
stresing.start_measurement_blocking()
frame_buffer = stresing.copy_one_sample(drvno, 5, 0 ,0)
# Plot the frame
plt.plot(frame_buffer)
plt.show()
# Exit the driver
status = stresing.exit_driver()
