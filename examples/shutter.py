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
import time


# Always use board 0. There is only one PCIe board in this example script.
drvno = 0

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

# Create a variable of type uint8_t
number_of_boards = c_uint8(0)
# Get the pointer the variable
ptr_number_of_boards = pointer(number_of_boards)
# Initialize the driver and pass the created pointer to it. number_of_boards should show the number of detected PCIe boards after the next call.
status = dll.DLLInitDriver(ptr_number_of_boards)
# Check the status code after each DLL call. When it is not 0, which means there is no error, an exception is raised. The error message will be displayed and the script will stop.
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))


# Loop for closing and opening all shutters 10 times once per second
for i in range(10):
	print("Open")
	# Set all shutters to open
	status = dll.DLLSetShutterStates(drvno, 0)
	if(status != 0):
		raise BaseException(dll.DLLConvertErrorCodeToMsg(status))
	
	# Wait for 1 second
	time.sleep(1)

	print("Close")
	# Set all shutters to closed
	# 15 = 0b00001111, which means all shutters are set to open
	status = dll.DLLSetShutterStates(drvno, 15)
	if(status != 0):
		raise BaseException(dll.DLLConvertErrorCodeToMsg(status))

	# Wait for 1 second
	time.sleep(1)

# Exit the driver
status = dll.DLLExitDriver()
if(status != 0):
	raise BaseException(dll.DLLConvertErrorCodeToMsg(status))