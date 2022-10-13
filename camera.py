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
	_fields_ = [("software_polling", c_uint32),
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
		("sensor_type", c_uint32),
		("camera_system", c_uint32),
		("camcnt", c_uint32),
		("pixel", c_uint32),
		("mshut", c_uint32),
		("led_off", c_uint32),
		("sensor_gain", c_uint32),
		("adc_gain", c_uint32),
		("Temp_level", c_uint32),
		("dac", c_uint32),
		("enable_gpx", c_uint32),
		("gpx_offset", c_uint32),
		("FFTLines", c_uint32),
		("Vfreq", c_uint32),
		("FFTMode", c_uint32),
		("lines_binning", c_uint32),
		("number_of_regions", c_uint32),
		("keep", c_uint32),
		("region_size", c_uint32 * 8),
		("dac_output", c_uint32 * 8 * 5),
		("TORmodus", c_uint32),
		("ADC_Mode", c_uint32),
		("ADC_custom_pattern", c_uint32),
		("bec_in_10ns", c_uint32),
		("cont_pause_in_microsecnods", c_uint32),
		("is_Ir", c_uint32),
		("IOCtrl_impact_start_pixel", c_uint32),
		("IOCtrl_output_width_in_5ns", c_uint32 * 8),
		("IOCtrl_output_delay_in_5ns", c_uint32 * 8),
		("IOCtrl_T0_period_in_10ns", c_uint32),
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
settings.sensor_type = 1
settings.camera_system = 0
settings.camcnt = 1
settings.pixel = 1088
settings.FFTLines = 128
settings.Vfreq = 7
settings.FFTmode = 0
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
frame_buffer = (c_uint16 * settings.pixel)(0)
ptr_frame_buffer = pointer(frame_buffer)
# Get the data of one frame. Sample 10, block 0, camera 0
status = dll.DLLReturnFrame(drvno, 10, 0, 0, ptr_frame_buffer, settings.pixel)
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
# Convert the c-style array to a python list
list_frame_buffer = [frame_buffer[i] for i in range(settings.pixel)]
# Plot the frame
plt.plot(list_frame_buffer)
plt.show()

# This block is showing you how to get all data of one frame with one DLL call
# block_buffer = (c_uint16 * (settings.pixel * settings.nos * settings.camcnt))(0)
# ptr_block_buffer = pointer(block_buffer)
# status = dll.DLLCopyOneBlock(drvno, 0, ptr_block_buffer)
# if(status != 0):
# 	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

# This block is showing you how to get all data of the whole measurement with one DLL call
# data_buffer = (c_uint16 * (settings.pixel * settings.nos * settings.camcnt * settings.nob))(0)
# ptr_data_buffer = pointer(data_buffer)
# status = dll.DLLCopyAllData(drvno, ptr_data_buffer)
# if(status != 0):
# 	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

# Exit the driver
status = dll.DLLExitDriver()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))