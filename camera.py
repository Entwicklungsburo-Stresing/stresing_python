# This python example was created with DLL version 3.24.3
# This script initializes the camera, does one measurement, reads the data and plots the data. The data access happens after the complete measurement is done. This example is written for 1 camera on 1 PCIe board.

# ctypes is used for communication with the DLL 
from ctypes import *
# matplotlib is used for the data plot
import matplotlib.pyplot as plt

# drvno selects the PCIe board. While there is only 1 PCIe board in this exmaple, it is always 1.
drvno = 1

# This is the settings stuct. It must be the same like in EBST_CAM/shared_src/struct.h regarding order, data formates and size.
class settings_struct(Structure):
	_fields_ = [("use_software_polling", c_uint32),
		("nos", c_uint32),
		("nob", c_uint32),
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
		("trigger_mode_cc", c_uint32),
		("board_sel", c_uint32),
		("SENSOR_TYPE", c_uint32),
		("CAMERA_SYSTEM", c_uint32),
		("CAMCNT", c_uint32),
		("PIXEL", c_uint32),
		("mshut", c_uint32),
		("led_off", c_uint32),
		("sensor_gain", c_uint32),
		("adc_gain", c_uint32),
		("temp_level", c_uint32),
		("DAC", c_uint32),
		("unused", c_uint32),
		("gpx_offset", c_uint32),
		("FFT_LINES", c_uint32),
		("VFREQ", c_uint32),
		("fft_mode", c_uint32),
		("lines_binning", c_uint32),
		("number_of_regions", c_uint32),
		("keep", c_uint32),
		("region_size", c_uint32 * 8),
		("dac_output", c_uint32 * 8 * 5),
		("tor", c_uint32),
		("adc_mode", c_uint32),
		("adc_custom_pattern", c_uint32),
		("bec_in_10ns", c_uint32),
		("cont_pause_in_microsecnods", c_uint32),
		("IS_HS_IR", c_uint32),
		("ioctrl_impact_start_pixel", c_uint32),
		("ioctrl_output_width_in_5ns", c_uint32 * 8),
		("ioctrl_output_delay_in_5ns", c_uint32 * 8),
		("ictrl_T0_period_in_10ns", c_uint32),
		("dma_buffer_size_in_scans", c_uint32),
		("tocnt", c_uint32),
		("ticnt", c_uint32),
		("use_ec", c_uint32)]

# Create an instance of the settings struct
settings = settings_struct()
# Set all settings that are needed for the measurement. See EBST_CAM/shared_src/struct.h for details.
settings.nos = 1000
settings.nob = 2
settings.sti_mode = 4
settings.bti_mode = 4
settings.board_sel = 1
settings.SENSOR_TYPE = 1
settings.CAMERA_SYSTEM = 0
settings.CAMCNT = 1
settings.PIXEL = 1088
settings.FFT_LINES = 128
settings.VFREQ = 7
settings.fft_mode = 0
settings.lines_binning = 1
settings.dma_buffer_size_in_scans = 1000
settings.stime_in_microsec = 1000
settings.btime_in_microsec = 1000000

# Load ESLSCDLL.dll
dll = WinDLL("./ESLSCDLL")
# Set the return type of DLLConvertErrorCodeToMsg to c-string pointer
dll.DLLConvertErrorCodeToMsg.restype = c_char_p

# Create a variable of type uint8_t
number_of_boards = c_uint8(0)
# Get the pointer the variable
ptr_number_of_boards = pointer(number_of_boards)
# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
status = dll.DLLInitDriver(ptr_number_of_boards)
# Check the status code after each DLL call. When it is not 0, which means there is no error, an exception is raised. The error message will be displayed and the script will stop.
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Initialize the PCIe board.
status = dll.DLLInitBoard()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Set all settings with the earlier created settings struct
status = dll.DLLSetGlobalSettings(settings)
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Initialize the measurement. The settings from the step before will be used for this.
status = dll.DLLInitMeasurement()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Start the measurement. In this example the blocking call is used, which means this call will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
status = dll.DLLStartMeasurement_blocking()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

# Create an c-style uint16 array of size pixel which is initialized to 0
frame_buffer = (c_uint16 * settings.PIXEL)(0)
ptr_frame_buffer = pointer(frame_buffer)
# Get the data of one frame. Sample 10, block 0, camera 0
status = dll.DLLReturnFrame(drvno, 10, 0, 0, ptr_frame_buffer, settings.PIXEL)
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Convert the c-style array to a python list
list_frame_buffer = [frame_buffer[i] for i in range(settings.PIXEL)]
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