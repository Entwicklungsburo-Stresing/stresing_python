## @file: core.py
# @brief: This module provides the core functionality for interacting with the Stresing camera system.
# @details: The python module workes as a wrapper for the ESLSCDLL library.
# @author: Florian Hahn
# @date: 25.06.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released under the LPGL-3.0.

import ctypes
from ctypes import c_uint8, POINTER, c_uint32, c_double, Structure, c_char, c_int, c_char_p, c_uint16, c_int64
import os

# Load ESLSCDLL.dll
if os.name == 'nt':
	from ctypes import WinDLL
	file_path = os.path.abspath(os.path.dirname(__file__))
	print(file_path)
	dll = WinDLL(file_path + "/ESLSCDLL")
else:
	from ctypes.util import find_library
	from ctypes import CDLL
	lib_path = find_library("ESLSCDLL")
	if not lib_path:
		raise ImportError("Could not find ESLSCDLL library")
	dll = CDLL(lib_path)

# These are the settings structs. It must be the same like in EBST_CAM/shared_src/struct.h regarding order, data formats and size.
# You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
class camera_settings(Structure):
	_fields_ = [("use_software_polling", c_uint32),
		("sti_mode", c_uint32),
		("bti_mode", c_uint32),
		("stime", c_uint32),
		("btime", c_uint32),
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
		("timer_resolution_mode", c_uint32),]

class measurement_settings(Structure):
	_fields_ = [("board_sel", c_uint32),
		("nos", c_uint32),
		("nob", c_uint32),
		("contiuous_measurement", c_uint32),
		("cont_pause_in_microseconds", c_uint32),
		("camera_settings", camera_settings * 5)]

def __convert_error_code_to_msg(status: c_int) -> str:
	"""
	Convert the error code returned by the DLL to a human-readable string message.

	Args:
		status (c_int): The error code returned by the DLL function.

	Returns:
		str: The corresponding error message as a string.
	"""
	dll.DLLConvertErrorCodeToMsg.argtypes = [c_int]
	dll.DLLConvertErrorCodeToMsg.restype = c_char_p
	return dll.DLLConvertErrorCodeToMsg(status).decode()

def init_settings_struct(ms: measurement_settings):
	"""
	Initialize the measurement_settings structure with default values using the DLL.

	Args:
		ms (measurement_settings): The measurement_settings structure to initialize.
	"""
	dll.DLLInitSettingsStruct.argtypes = [POINTER(measurement_settings)]
	dll.DLLInitSettingsStruct(ctypes.byref(ms))

settings = measurement_settings()
init_settings_struct(settings)

def init_driver() -> int:
	"""
	Initialize the driver and return the number of available boards.

	Returns:
		int: The number of available boards.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	_number_of_boards = c_uint8()
	status = dll.DLLInitDriver(ctypes.byref(_number_of_boards))
	# Check the status code after each DLL call. When it is not 0, which means there is no error, an exception is raised. The error message will be displayed and the script will stop.
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return _number_of_boards.value

def init_measurement():
	"""
	Initialize the measurement with the current settings.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLInitMeasurement.argtypes = [measurement_settings]
	status = dll.DLLInitMeasurement(settings)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def start_measurement_blocking():
	"""
	Start the measurement in blocking mode (waits until measurement is finished).

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	status = dll.DLLStartMeasurement_blocking()
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def start_measurement_nonblocking():
	"""
	Start the measurement in non-blocking mode (returns immediately).
	"""
	dll.DLLStartMeasurement_nonblocking()

def abort_measurement():
	"""
	Abort the current measurement.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	status = dll.DLLAbortMeasurement()
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_one_sample(drvno: int, sample: int, block: int, camera: int) -> list[int]:
	"""
	Copy one sample from the specified board, sample, block, and camera.

	Args:
		drvno (int): Board number.
		sample (int): Sample number.
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		list[int]: The frame buffer data as a list of integers.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer = (c_uint16 * settings.camera_settings[drvno].PIXEL)(0)
	dll.DLLCopyOneSample.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneSample(c_uint32(drvno), c_uint32(sample), c_uint32(block), c_uint16(camera), frame_buffer)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return list(frame_buffer)

def copy_one_sample_multiple_boards(sample: int, block: int, camera: int) -> list[list[int]]:
	"""
	Copy one sample from all boards for the specified sample, block, and camera.

	Args:
		sample (int): Sample number.
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		list[list[int]]: A list of frame buffers for each board.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * (settings.camera_settings[0].PIXEL))(0)
	frame_buffer1 = (c_uint16 * (settings.camera_settings[1].PIXEL))(0)
	frame_buffer2 = (c_uint16 * (settings.camera_settings[2].PIXEL))(0)
	frame_buffer3 = (c_uint16 * (settings.camera_settings[3].PIXEL))(0)
	frame_buffer4 = (c_uint16 * (settings.camera_settings[4].PIXEL))(0)
	dll.DLLCopyOneSample_multipleBoards.argtypes = [c_uint32, c_uint32, c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneSample_multipleBoards(c_uint32(sample), c_uint32(block), c_uint16(camera), frame_buffer0, frame_buffer1, frame_buffer2, frame_buffer3, frame_buffer4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	all_buffers = [
		list(frame_buffer0),
		list(frame_buffer1),
		list(frame_buffer2),
		list(frame_buffer3),
		list(frame_buffer4)
	]
	return all_buffers

def copy_one_block(drvno: int, block: int) -> list[int]:
	"""
	Copy one block from the specified board and block number.

	Args:
		drvno (int): Board number.
		block (int): Block number.

	Returns:
		list[int]: The frame buffer data as a list of integers.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * (settings.camera_settings[drvno].PIXEL * settings.nos * settings.camera_settings[drvno].CAMCNT))(0)
	dll.DLLCopyOneBlock.argtypes = [c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneBlock(c_uint32(drvno), c_uint16(block), frame_buffer0)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return list(frame_buffer0)

def copy_one_block_multiple_boards(block: int) -> list[list[int]]:
	"""
	Copy one block from all boards for the specified block number.

	Args:
		block (int): Block number.

	Returns:
		list[list[int]]: A list of frame buffers for each board.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * (settings.camera_settings[0].PIXEL * settings.nos * settings.camera_settings[0].CAMCNT))(0)
	frame_buffer1 = (c_uint16 * (settings.camera_settings[1].PIXEL * settings.nos * settings.camera_settings[1].CAMCNT))(0)
	frame_buffer2 = (c_uint16 * (settings.camera_settings[2].PIXEL * settings.nos * settings.camera_settings[2].CAMCNT))(0)
	frame_buffer3 = (c_uint16 * (settings.camera_settings[3].PIXEL * settings.nos * settings.camera_settings[3].CAMCNT))(0)
	frame_buffer4 = (c_uint16 * (settings.camera_settings[4].PIXEL * settings.nos * settings.camera_settings[4].CAMCNT))(0)
	dll.DLLCopyOneBlock_multipleBoards.argtypes = [c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneBlock_multipleBoards(c_uint16(block), frame_buffer0, frame_buffer1, frame_buffer2, frame_buffer3, frame_buffer4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	all_buffers = [
		list(frame_buffer0),
		list(frame_buffer1),
		list(frame_buffer2),
		list(frame_buffer3),
		list(frame_buffer4)
	]
	return all_buffers

def copy_one_block_of_one_camera(drvno: int, block: int, camera: int) -> list[int]:
	"""
	Copy one block for a specific camera from the specified board and block number.

	Args:
		drvno (int): Board number.
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		list[int]: The frame buffer data as a list of integers.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * settings.camera_settings[drvno].PIXEL * settings.nos)(0)
	dll.DLLCopyOneBlockOfOneCamera.argtypes = [c_uint32, c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneBlockOfOneCamera(c_uint32(drvno), c_uint32(block), c_uint16(camera), frame_buffer0)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return list(frame_buffer0)

def copy_one_block_of_one_camera_multiple_boards(block: int, camera: int) -> list[list[int]]:
	"""
	Copy one block for a specific camera from all boards for the specified block and camera number.

	Args:
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		list[list[int]]: A list of frame buffers for each board.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * (settings.camera_settings[0].PIXEL * settings.nos))(0)
	frame_buffer1 = (c_uint16 * (settings.camera_settings[1].PIXEL * settings.nos))(0)
	frame_buffer2 = (c_uint16 * (settings.camera_settings[2].PIXEL * settings.nos))(0)
	frame_buffer3 = (c_uint16 * (settings.camera_settings[3].PIXEL * settings.nos))(0)
	frame_buffer4 = (c_uint16 * (settings.camera_settings[4].PIXEL * settings.nos))(0)
	dll.DLLCopyOneBlockOfOneCamera_multipleBoards.argtypes = [c_uint16, c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneBlockOfOneCamera_multipleBoards(c_uint16(block), c_uint16(camera), frame_buffer0, frame_buffer1, frame_buffer2, frame_buffer3, frame_buffer4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	all_buffers = [
		list(frame_buffer0),
		list(frame_buffer1),
		list(frame_buffer2),
		list(frame_buffer3),
		list(frame_buffer4)
	]
	return all_buffers

def copy_all_data(drvno: int) -> list[int]:
	"""
	Copy all data from the specified board.

	Args:
		drvno (int): Board number.

	Returns:
		list[int]: The frame buffer data as a list of integers.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * (settings.camera_settings[drvno].PIXEL * settings.nos * settings.nob * settings.camera_settings[drvno].CAMCNT))(0)
	dll.DLLCopyAllData.argtypes = [c_uint32, POINTER(c_uint16)]
	status = dll.DLLCopyAllData(c_uint32(drvno), frame_buffer0)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return list(frame_buffer0)

def copy_all_data_2d(drvno: int) -> list[list[int]]:
	"""
	Copy all data from the specified board and return it as a 2D list.

	Args:
		drvno (int): Board number.

	Returns:
		list[list[int]]: The frame buffer data as a 2D list, where each inner list represents a row of pixel data.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer_1d = copy_all_data(drvno)
	pixel = settings.camera_settings[drvno].PIXEL
	nrows = len(frame_buffer_1d) // pixel
	frame_buffer_2d = [frame_buffer_1d[i*pixel:(i+1)*pixel] for i in range(nrows)]
	return frame_buffer_2d

def copy_all_data_multiple_boards() -> list[list[int]]:
	"""
	Copy all data from all boards.

	Returns:
		list[list[int]]: A list of frame buffers for each board.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * settings.camera_settings[0].PIXEL * settings.nos * settings.nob * settings.camera_settings[0].CAMCNT)(0)
	frame_buffer1 = (c_uint16 * settings.camera_settings[1].PIXEL * settings.nos * settings.nob * settings.camera_settings[1].CAMCNT)(0)
	frame_buffer2 = (c_uint16 * settings.camera_settings[2].PIXEL * settings.nos * settings.nob * settings.camera_settings[2].CAMCNT)(0)
	frame_buffer3 = (c_uint16 * settings.camera_settings[3].PIXEL * settings.nos * settings.nob * settings.camera_settings[3].CAMCNT)(0)
	frame_buffer4 = (c_uint16 * settings.camera_settings[4].PIXEL * settings.nos * settings.nob * settings.camera_settings[4].CAMCNT)(0)
	dll.DLLCopyAllData_multipleBoards.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyAllData_multipleBoards(frame_buffer0, frame_buffer1, frame_buffer2, frame_buffer3, frame_buffer4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	all_buffers = [
		list(frame_buffer0),
		list(frame_buffer1),
		list(frame_buffer2),
		list(frame_buffer3),
		list(frame_buffer4)
	]
	return all_buffers

def copy_data_arbitrary(drvno: int, sample: int, block: int, camera: int, pixel: int, length_in_pixel: int) -> list[int]:
	"""
	Copy an arbitrary region of data from the specified board, sample, block, camera, pixel, and length.

	Args:
		drvno (int): Board number.
		sample (int): Sample number.
		block (int): Block number.
		camera (int): Camera number.
		pixel (int): Pixel start index.
		length_in_pixel (int): Number of pixels to copy.

	Returns:
		list[int]: The frame buffer data as a list of integers.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	frame_buffer0 = (c_uint16 * length_in_pixel)(0)
	dll.DLLCopyDataArbitrary.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, c_uint32, c_uint32, POINTER(c_uint16)]
	status = dll.DLLCopyDataArbitrary(c_uint32(drvno), c_uint32(sample), c_uint32(block), c_uint16(camera), c_uint32(pixel), c_uint32(length_in_pixel), frame_buffer0)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return list(frame_buffer0)

def get_one_sample_pointer(drvno: int, sample: int, block: int, camera: int) -> tuple[POINTER(c_uint16), int]:
	"""
	Get a pointer to one sample for the specified board, sample, block, and camera.

	Args:
		drvno (int): Board number.
		sample (int): Sample number.
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		tuple[POINTER, int]: A tuple containing the data pointer and the number of bytes to the end of the buffer.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLGetOneSamplePointer.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	data_pointer = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetOneSamplePointer(c_uint32(drvno), c_uint32(sample), c_uint32(block), c_uint16(camera), ctypes.byref(data_pointer), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return data_pointer, bytes_to_end_of_buffer.value

def get_one_block_pointer(drvno: int, block: int) -> tuple[POINTER(c_uint16), int]:
	"""
	Get a pointer to one block for the specified board and block number.

	Args:
		drvno (int): Board number.
		block (int): Block number.

	Returns:
		tuple[POINTER, int]: A tuple containing the data pointer and the number of bytes to the end of the buffer.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLGetOneBlockPointer.argtypes = [c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	data_pointer = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetOneBlockPointer(c_uint32(drvno), c_uint16(block), ctypes.byref(data_pointer), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return data_pointer, bytes_to_end_of_buffer.value

def get_all_data_pointer(drvno: int) -> tuple[POINTER(c_uint16), int]:
	"""
	Get a pointer to all data for the specified board.

	Args:
		drvno (int): Board number.

	Returns:
		tuple[POINTER, int]: A tuple containing the data pointer and the number of bytes to the end of the buffer.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLGetAllDataPointer.argtypes = [c_uint32, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	data_pointer = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetAllDataPointer(c_uint32(drvno), ctypes.byref(data_pointer), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return data_pointer, bytes_to_end_of_buffer.value

def get_pixel_pointer(drvno: int, pixel: int, sample: int, block: int, camera: int) -> tuple[POINTER(c_uint16), int]:
	"""
	Get a pointer to a specific pixel for the specified board, pixel, sample, block, and camera.

	Args:
		drvno (int): Board number.
		pixel (int): Pixel index.
		sample (int): Sample number.
		block (int): Block number.
		camera (int): Camera number.

	Returns:
		tuple[POINTER, int]: A tuple containing the data pointer and the number of bytes to the end of the buffer.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLGetPixelPointer.argtypes = [c_uint32, c_uint16, c_uint32, c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	pdest = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetPixelPointer(c_uint32(drvno), c_uint16(pixel), c_uint32(sample), c_uint32(block), c_uint16(camera), ctypes.byref(pdest), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return pdest, bytes_to_end_of_buffer.value

def exit_driver():
	"""
	Exit and clean up the driver.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	status = dll.DLLExitDriver()
	if(status != 0):
		raise Exception(__convert_error_code_to_msg(status))
	
def get_current_scan_number(drvno: int) -> tuple[int, int]:
	"""
	Get the current scan number (sample and block) for the specified board.

	Args:
		drvno (int): The board number (driver number) to query.

	Returns:
		tuple[int, int]: A tuple containing the current sample number and block number.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	cur_sample = c_int64(-2)
	cur_block = c_int64(-2)
	dll.DLLGetCurrentScanNumber.argtypes = [c_uint32, POINTER(c_int64), POINTER(c_int64)]
	status = dll.DLLGetCurrentScanNumber(c_uint32(drvno), ctypes.byref(cur_sample), ctypes.byref(cur_block))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return cur_sample.value, cur_block.value

def set_shutter_states(drvno: int, states: int) -> None:
	"""
	Set the shutter states for the specified board.

	Args:
		drvno (int): The board number (driver number) to set the shutter states for.
		states (int): The shutter states are represented as bits in one integer. Bits 0 to 3 corresponds to the 4 shutters.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLSetShutterStates.argtypes = [c_uint32, c_uint16]
	status = dll.DLLSetShutterStates(c_uint32(drvno), c_uint16(states))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def calc_trms(drvno: int, first_sample: int, last_sample: int, tmrs_pixel: int, cam_pos: int) -> tuple[float, float]:
	"""
	Calculate the RMS (Root Mean Square) for a specific camera and pixel.

	Args:
		drvno (int): The board number (driver number).
		first_sample (int): The first sample index.
		last_sample (int): The last sample index.
		tmrs_pixel (int): The pixel index for which to calculate the RMS.
		cam_pos (int): The camera position.

	Returns:
		tuple(float, float): A tuple containing the mean value and the RMS.

	Raises:
		Exception: If the DLL call returns a non-zero status (error), an exception is raised with the error message.
	"""
	dll.DLLCalcTrms.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32, c_uint16, POINTER(c_double), POINTER(c_double)]
	mean = c_double(0.0)
	rms = c_double(0.0)
	status = dll.DLLCalcTrms(c_uint32(drvno), c_uint32(first_sample), c_uint32(last_sample), c_uint32(tmrs_pixel), c_uint16(cam_pos), ctypes.byref(mean), ctypes.byref(rms))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return mean.value, rms.value
