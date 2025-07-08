## @file: raw_dll_call.py
# @brief: This script shows how to directly call the DLL functions of ESLSCDLL.dll using the python module stresing.
# @author: Florian Hahn
# @date: 08.07.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import stresing
import ctypes
from ctypes import c_uint32, POINTER

# Initialize the driver.
stresing.init_driver()
# Read the register S0Addr_EBST
# You can use every call you can find here in the documentation: https://entwicklungsburo-stresing.github.io/_e_s_l_s_c_d_l_l_8h.html
# Use board 0
drvno = 0
# data buffer
data = c_uint32(0)
# Address of the register S0Addr_EBST. You can find addresses of the PCIe card registers here: https://entwicklungsburo-stresing.github.io/enum__hardware_8h.html#a1532e8504727e103db7ec69af3330f15
address = 0x1C
stresing.dll.DLLreadRegisterS0_32.argtypes = [c_uint32, POINTER(c_uint32), c_uint32]
status = stresing.dll.DLLreadRegisterS0_32(c_uint32(0), ctypes.byref(data), c_uint32(address))
# Check the return status
if status != 0:
	raise Exception(stresing.convert_error_code_to_msg(status))
# Print the read value
print(f"Value of S0Addr_EBST: {data.value}")
# Interprete the value as 4 charaters of ASCII
ascii_value = ''.join(chr((data.value >> (i * 8)) & 0xFF) for i in range(4))
print(f"Interpreted as ASCII: {ascii_value}")
# Exit the driver
stresing.exit_driver()
