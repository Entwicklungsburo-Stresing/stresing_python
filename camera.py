## @file: camera.py
# @brief: This script shows how to operate the Stresing camera using the DLL interface.
# @details: This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board. This python example was created with DLL version 4.18.0
# @author: Florian Hahn
# @date: 13.10.2022
# @copyright: Copyright (c) 2022, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

# ctypes is used for communication with the DLL 
from ctypes import *
from ctypes.util import find_library
# matplotlib is used for the data plot
import matplotlib.pyplot as plt
import os

use_blocking_call = True

# These are the settings structs. It must be the same like in EBST_CAM/shared_src/struct.h regarding order, data formats and size.
class camera_settings(Structure):
	_fields_ = [("use_software_polling", c_uint32),
		("sti_mode", c_uint32),
		("bti_mode", c_uint32),
		("stime_in_microsec", c_uint32),
		("btime_in_microsec", c_uint32),
		("sdat_in_10ns", c_uint32),
		("bdat_in_10ns", c_uint32),
		("sslope", c_uint32),
		("bslope", c_uint32),
		("xckdelay_in_10ns", c_uint32),
		("sec_in_10ns", c_uint32),
		("trigger_mode_integrator", c_uint32),
		("SENSOR_TYPE", c_uint32),
		("CAMERA_SYSTEM", c_uint32),
		("CAMCNT", c_uint32),
		("PIXEL", c_uint32),
		("is_fft_legacy", c_uint32),
		("led_off", c_uint32),
		("sensor_gain", c_uint32),
		("adc_gain", c_uint32),
		("temp_level", c_uint32),
		("bticnt", c_uint32),
		("gpx_offset", c_uint32),
		("FFT_LINES", c_uint32),
		("VFREQ", c_uint32),
		("fft_mode", c_uint32),
		("lines_binning", c_uint32),
		("number_of_regions", c_uint32),
		("s1s2_read_delay_in_10ns", c_uint32),
		("region_size", c_uint32 * 8),
		("dac_output", c_uint32 * 8 * 8), # 8 channels for 8 possible cameras in line
		("tor", c_uint32),
		("adc_mode", c_uint32),
		("adc_custom_pattern", c_uint32),
		("bec_in_10ns", c_uint32),
		("channel_select", c_uint32),
		("ioctrl_impact_start_pixel", c_uint32),
		("ioctrl_output_width_in_5ns", c_uint32 * 8),
		("ioctrl_output_delay_in_5ns", c_uint32 * 8),
		("ictrl_T0_period_in_10ns", c_uint32),
		("dma_buffer_size_in_scans", c_uint32),
		("tocnt", c_uint32),
		("sticnt", c_uint32),
		("sensor_reset_or_hsir_ec", c_uint32),
		("write_to_disc", c_uint32),
		("file_path", c_char * 256),
		("shift_s1s2_to_next_scan", c_uint32),
		("is_cooled_camera_legacy_mode", c_uint32),
		("monitor", c_uint32),
		("manipulate_data_mode", c_uint32),
		("manipulate_data_custom_factor", c_double),
		("ec_legacy_mode", c_uint32),
		("stime_resolution_mode", c_uint32),]

class measurement_settings(Structure):
	_fields_ = [("board_sel", c_uint32),
	("nos", c_uint32),
	("nob", c_uint32),
	("contiuous_measurement", c_uint32),
	("cont_pause_in_microseconds", c_uint32),
	("camera_settings", camera_settings * 5)]

# Always use board 0. There is only one PCIe board in this example script.
drvno = 0
# Create an instance of the settings struct
settings = measurement_settings()
# Load ESLSCDLL.dll
if os.name == 'nt':
	file_path = os.path.abspath(os.path.dirname(__file__))
	print(file_path)
	dll = WinDLL(file_path + "/ESLSCDLL")
else:
	dll = find_library("ESLSCDLL")
	dll = CDLL(dll)
# Set the return type of DLLConvertErrorCodeToMsg to c-string pointer
dll.DLLConvertErrorCodeToMsg.restype = c_char_p
# Get a pointer to the settings
ptr_settings = pointer(settings)
# Init all settings to its default value
dll.DLLInitSettingsStruct(ptr_settings)

# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
settings.board_sel = 1
settings.nos = 1000
settings.nob = 1
settings.camera_settings[drvno].sti_mode = 4
settings.camera_settings[drvno].bti_mode = 4
settings.camera_settings[drvno].SENSOR_TYPE = 4
settings.camera_settings[drvno].CAMERA_SYSTEM = 2
settings.camera_settings[drvno].CAMCNT = 1
settings.camera_settings[drvno].PIXEL = 1088
settings.camera_settings[drvno].stime_in_microsec = 1000
settings.camera_settings[drvno].btime_in_microsec = 100000
settings.camera_settings[drvno].fft_mode = 1
settings.camera_settings[drvno].FFT_LINES = 128
settings.camera_settings[drvno].lines_binning = 1
settings.camera_settings[drvno].number_of_regions = 5
settings.camera_settings[drvno].region_size[0] = 10
settings.camera_settings[drvno].region_size[1] = 50
settings.camera_settings[drvno].region_size[2] = 10
settings.camera_settings[drvno].region_size[3] = 50
settings.camera_settings[drvno].region_size[4] = 8
settings.camera_settings[drvno].use_software_polling = 0
settings.camera_settings[drvno].VFREQ = 7
settings.camera_settings[drvno].dac_output[0][0] = 55000
settings.camera_settings[drvno].dac_output[0][1] = 55000
settings.camera_settings[drvno].dac_output[0][2] = 55000
settings.camera_settings[drvno].dac_output[0][3] = 55000
settings.camera_settings[drvno].dac_output[0][4] = 55000
settings.camera_settings[drvno].dac_output[0][5] = 55000
settings.camera_settings[drvno].dac_output[0][6] = 55000
settings.camera_settings[drvno].dac_output[0][7] = 55000


# Create a variable of type uint8_t
number_of_boards = c_uint8(0)
# Get the pointer the variable
ptr_number_of_boards = pointer(number_of_boards)
# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
status = dll.DLLInitDriver(ptr_number_of_boards)
# Check the status code after each DLL call. When it is not 0, which means there is no error, an exception is raised. The error message will be displayed and the script will stop.
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Initialize the measurement.
status = dll.DLLInitMeasurement(settings)
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

if use_blocking_call:
	# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
	status = dll.DLLStartMeasurement_blocking()
	if(status != 0):
		raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
else:
	# Start the measurement. This is the nonblocking call, which means it will return immediately. 
	dll.DLLStartMeasurement_nonblocking()

	cur_sample = c_int64(-2)
	ptr_cur_sample = pointer(cur_sample)
	cur_block = c_int64(-2)
	ptr_cur_block = pointer(cur_block)

	while cur_sample.value < settings.nos-1 or cur_block.value < settings.nob-1:
		dll.DLLGetCurrentScanNumber(drvno, ptr_cur_sample, ptr_cur_block)
		print("sample: "+str(cur_sample.value)+" block: "+str(cur_block.value))

# Create an c-style uint16 array of size pixel which is initialized to 0
frame_buffer = (c_uint16 * settings.camera_settings[0].PIXEL)(0)
ptr_frame_buffer = pointer(frame_buffer)
# Get the data of one frame. Sample 5, block 0, camera 0
status = dll.DLLCopyOneSample(drvno, 5, 0, 0, ptr_frame_buffer)
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Convert the c-style array to a python list
list_frame_buffer = [frame_buffer[i] for i in range(settings.camera_settings[0].PIXEL)]
# Plot the frame
plt.plot(list_frame_buffer)
plt.show()

# This block is showing you how to get all data of one frame with one DLL call
# block_buffer = (c_uint16 * (settings.PIXEL * settings.nos * settings.CAMCNT))(0)
# ptr_block_buffer = pointer(block_buffer)
# status = dll.DLLCopyOneBlock(drvno, 0, ptr_block_buffer)
# if(status != 0):
# 	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

# This block is showing you how to get all data of the whole measurement with one DLL call
# data_buffer = (c_uint16 * (settings.PIXEL * settings.nos * settings.CAMCNT * settings.nob))(0)
# ptr_data_buffer = pointer(data_buffer)
# status = dll.DLLCopyAllData(drvno, ptr_data_buffer)
# if(status != 0):
# 	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

# Exit the driver
status = dll.DLLExitDriver()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))