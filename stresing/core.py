import ctypes
from ctypes import c_uint8, POINTER, c_uint32, c_double, Structure, c_char, c_int, c_char_p, c_uint16
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

def __convert_error_code_to_msg(status: c_int) -> str:
	"""Convert the error code to a c string."""
	dll.DLLConvertErrorCodeToMsg.argtypes = [c_int]
	dll.DLLConvertErrorCodeToMsg.restype = c_char_p
	return dll.DLLConvertErrorCodeToMsg(status).decode()

def init_settings_struct(ms: measurement_settings):
	dll.DLLInitSettingsStruct.argtypes = [POINTER(measurement_settings)]
	dll.DLLInitSettingsStruct(ctypes.byref(ms))

settings = measurement_settings()
init_settings_struct(settings)

def init_driver() -> int:
	_number_of_boards = c_uint8()
	status = dll.DLLInitDriver(ctypes.byref(_number_of_boards))
	# Check the status code after each DLL call. When it is not 0, which means there is no error, an exception is raised. The error message will be displayed and the script will stop.
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return _number_of_boards.value

def init_measurement():
	dll.DLLInitMeasurement.argtypes = [measurement_settings]
	status = dll.DLLInitMeasurement(settings)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def start_measurement_blocking():
	status = dll.DLLStartMeasurement_blocking()
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def start_measurement_nonblocking():
	dll.DLLStartMeasurement_nonblocking()

def abort_measurement():
	status = dll.DLLAbortMeasurement()
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_one_sample(drvno: int, sample: int, block: int, camera: int) -> list[int]:
	# Ensure all arguments are c_uint32/c_uint16
	_drvno = c_uint32(drvno)
	_sample = c_uint32(sample)
	_block = c_uint32(block)
	_camera = c_uint16(camera)
	frame_buffer = (c_uint16 * settings.camera_settings[_drvno.value].PIXEL)(0)
	dll.DLLCopyOneSample.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneSample(_drvno, _sample, _block, _camera, ctypes.byref(frame_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return [frame_buffer[i] for i in range(settings.camera_settings[_drvno.value].PIXEL)]

def copy_one_sample_multiple_boards(sample: int, block: int, camera: int) -> list[list[int]]:
	_sample = c_uint32(sample)
	_block = c_uint32(block)
	_camera = c_uint16(camera)
	frame_buffer0 = (c_uint16 * settings.camera_settings[0].PIXEL)(0)
	frame_buffer1 = (c_uint16 * settings.camera_settings[1].PIXEL)(0)
	frame_buffer2 = (c_uint16 * settings.camera_settings[2].PIXEL)(0)
	frame_buffer3 = (c_uint16 * settings.camera_settings[3].PIXEL)(0)
	frame_buffer4 = (c_uint16 * settings.camera_settings[4].PIXEL)(0)
	dll.DLLCopyOneSample_multipleBoards.argtypes = [c_uint32, c_uint32, c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneSample_multipleBoards(_sample, _block, _camera, ctypes.byref(frame_buffer0), ctypes.byref(frame_buffer1), ctypes.byref(frame_buffer2), ctypes.byref(frame_buffer3), ctypes.byref(frame_buffer4))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	all_buffers = [
		[frame_buffer0[i] for i in range(settings.camera_settings[0].PIXEL)],
		[frame_buffer1[i] for i in range(settings.camera_settings[1].PIXEL)],
		[frame_buffer2[i] for i in range(settings.camera_settings[2].PIXEL)],
		[frame_buffer3[i] for i in range(settings.camera_settings[3].PIXEL)],
		[frame_buffer4[i] for i in range(settings.camera_settings[4].PIXEL)]
	]
	return all_buffers

def copy_one_block(drvno: int, block: int) -> list[int]:
	_drvno = c_uint32(drvno)
	_block = c_uint16(block)
	frame_buffer0 = (c_uint16 * settings.camera_settings[0].PIXEL)(0)
	dll.DLLCopyOneBlock.argtypes = [c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneBlock(_drvno, _block, frame_buffer0)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return [frame_buffer0[i] for i in range(settings.camera_settings[_drvno.value].PIXEL)]

def copy_one_block_multiple_boards(block, pdest0, pdest1, pdest2, pdest3, pdest4):
	block = c_uint16(block)
	dll.DLLCopyOneBlock_multipleBoards.argtypes = [c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneBlock_multipleBoards(block, pdest0, pdest1, pdest2, pdest3, pdest4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_one_block_of_one_camera(drvno, block, camera, pdest):
	drvno = c_uint32(drvno)
	block = c_uint32(block)
	camera = c_uint16(camera)
	dll.DLLCopyOneBlockOfOneCamera.argtypes = [c_uint32, c_uint32, c_uint16, POINTER(c_uint16)]
	status = dll.DLLCopyOneBlockOfOneCamera(drvno, block, camera, pdest)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_one_block_of_one_camera_multiple_boards(block, camera, pdest0, pdest1, pdest2, pdest3, pdest4):
	block = c_uint16(block)
	camera = c_uint16(camera)
	dll.DLLCopyOneBlockOfOneCamera_multipleBoards.argtypes = [c_uint16, c_uint16, POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyOneBlockOfOneCamera_multipleBoards(block, camera, pdest0, pdest1, pdest2, pdest3, pdest4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_all_data(drvno, pdest):
	drvno = c_uint32(drvno)
	dll.DLLCopyAllData.argtypes = [c_uint32, POINTER(c_uint16)]
	status = dll.DLLCopyAllData(drvno, pdest)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_all_data_multiple_boards(pdest0, pdest1, pdest2, pdest3, pdest4):
	dll.DLLCopyAllData_multipleBoards.argtypes = [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16)]
	status = dll.DLLCopyAllData_multipleBoards(pdest0, pdest1, pdest2, pdest3, pdest4)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def copy_data_arbitrary(drvno, sample, block, camera, pixel, length_in_pixel, pdest):
	drvno = c_uint32(drvno)
	sample = c_uint32(sample)
	block = c_uint32(block)
	camera = c_uint16(camera)
	pixel = c_uint32(pixel)
	length_in_pixel = c_uint32(length_in_pixel)
	dll.DLLCopyDataArbitrary.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, c_uint32, c_uint32, POINTER(c_uint16)]
	status = dll.DLLCopyDataArbitrary(drvno, sample, block, camera, pixel, length_in_pixel, pdest)
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def get_one_sample_pointer(drvno, sample, block, camera):
	drvno = c_uint32(drvno)
	sample = c_uint32(sample)
	block = c_uint32(block)
	camera = c_uint16(camera)
	dll.DLLGetOneSamplePointer.argtypes = [c_uint32, c_uint32, c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	pdest = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetOneSamplePointer(drvno, sample, block, camera, ctypes.byref(pdest), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return pdest, bytes_to_end_of_buffer.value

def get_one_block_pointer(drvno, block):
	drvno = c_uint32(drvno)
	block = c_uint16(block)
	dll.DLLGetOneBlockPointer.argtypes = [c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	pdest = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetOneBlockPointer(drvno, block, ctypes.byref(pdest), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return pdest, bytes_to_end_of_buffer.value

def get_all_data_pointer(drvno):
	drvno = c_uint32(drvno)
	dll.DLLGetAllDataPointer.argtypes = [c_uint32, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	pdest = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetAllDataPointer(drvno, ctypes.byref(pdest), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))
	return pdest, bytes_to_end_of_buffer.value

def get_pixel_pointer(drvno, pixel, sample, block, camera):
	drvno = c_uint32(drvno)
	pixel = c_uint16(pixel)
	sample = c_uint32(sample)
	block = c_uint32(block)
	camera = c_uint16(camera)
	dll.DLLGetPixelPointer.argtypes = [c_uint32, c_uint16, c_uint32, c_uint32, c_uint16, POINTER(POINTER(c_uint16)), POINTER(ctypes.c_size_t)]
	pdest = POINTER(c_uint16)()
	bytes_to_end_of_buffer = ctypes.c_size_t()
	status = dll.DLLGetPixelPointer(drvno, pixel, sample, block, camera, ctypes.byref(pdest), ctypes.byref(bytes_to_end_of_buffer))
	if status != 0:
		raise Exception(__convert_error_code_to_msg(status))

def exit_driver():
	status = dll.DLLExitDriver()
	if(status != 0):
		raise Exception(__convert_error_code_to_msg(status))
