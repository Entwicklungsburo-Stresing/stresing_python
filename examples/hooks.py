## @file: simple_blocking_measurement.py
# @brief: This script shows how to use hooks.
# @details:
# @author: Florian Hahn
# @date: 14.07.2025
# @copyright: Copyright (c) 2025, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.

import stresing

def measure_start_hook():
    print("Measurement started")

def measure_done_hook():
    print("Measurement done")

def block_start_hook():
    print("Block started")

def block_done_hook():
    print("Block done")

def all_blocks_done_hook():
    print("All blocks done")

# Initialize the driver.
number_of_boards = stresing.init_driver()
# Set all settings that are needed for the measurement in config.ini. The file config.ini is also compatible with the exported settings of Escam. Settings that are not found in the file, will be left as default. You can find a description of all settings here: https://entwicklungsburo-stresing.github.io/structmeasurement__settings.html
stresing.load_config_file("config.ini")
# Set all hooks
measure_started_ref = stresing.set_measure_start_hook(measure_start_hook)
measure_done_ref = stresing.set_measure_done_hook(measure_done_hook)
block_started_ref = stresing.set_block_start_hook(block_start_hook)
block_done_ref = stresing.set_block_done_hook(block_done_hook)
all_blocks_done_ref = stresing.set_all_blocks_done_hook(all_blocks_done_hook)
# Initialize the measurement.
stresing.init_measurement()
# Start the measurement. This is the blocking call, which means it will return when the measurement is finished. This is done to ensure that no data access happens before all data is collected.
stresing.start_measurement_blocking()
# Exit the driver
stresing.exit_driver()
