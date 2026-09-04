## @file: nonblocking_multiple_measurements.py
# @brief: This script shows how to operate the Stresing camera using the python module stresing.
# @details: This script initializes the camera, performs multiple measurements, reads the data and
#           lets the user step through the individual measurement plots using on-screen buttons. 
#           This example is written for 1 camera on 1 PCIe board.
# @author: Dennis Vollenweider
# @date: 13.10.2022
# @copyright: Copyright (c) 2026, Entwicklungsbüro Stresing. Released as public domain under the Unlicense.
import stresing
# matplotlib is used for the data plot
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
# time is used to wait for the measurement to finish
import time

# Initialize the driver.
number_of_boards = stresing.init_driver()

# Load the config file
stresing.load_config_file("config.ini")
stresing.init_measurement()
measurements = 10
frame_buffers = []  # one frame buffer per measurement is collected here

for measurement in range(measurements):
    # Wait until the previous measurement is done before starting a new one
    while (stresing.get_measure_on(drvno=0)):
        time.sleep(0.001)

    # Start the measurement. This is the nonblocking call, which means it will return immediately.
    stresing.start_measurement_nonblocking()
    cur_sample, cur_block = -2, -2

    # Wait until the block on bit is set. Ensure that the data collection is set up correctly before proceeding to read the data.
    while (not stresing.get_block_on(drvno=0)):
        time.sleep(0.001)

    drvno = 0
    while cur_sample < stresing.settings.nos - 1 or cur_block < stresing.settings.nob - 1:
        (cur_sample, cur_block) = stresing.get_current_scan_number(drvno)
        print("sample: " + str(cur_sample) + " block: " + str(cur_block))

    # Copy the 5th sample of each measurement to the frame_buffers list for later plotting.
    frame_buffer = stresing.copy_one_sample(drvno, 5, 0, 0)
    frame_buffers.append(frame_buffer)
    print("Measurement " + str(measurement) + " done.")

# ---------------------------------------------------------------------------
# Viewer: step through the recorded measurements with Previous/Next buttons
# (or the left/right arrow keys on the keyboard)
# ---------------------------------------------------------------------------
current_index = 0

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # leave room at the bottom for the buttons

line, = ax.plot(frame_buffers[current_index])
ax.set_xlabel("Pixel")
ax.set_ylabel("Intensity")
ax.set_title(f"Measurement {current_index + 1}/{len(frame_buffers)}")


def update_plot():
    data = frame_buffers[current_index]
    line.set_xdata(range(len(data)))
    line.set_ydata(data)
    ax.relim()
    ax.autoscale_view()
    ax.set_title(f"Measurement {current_index + 1}/{len(frame_buffers)}")
    fig.canvas.draw_idle()


def show_next(event):
    global current_index
    current_index = (current_index + 1) % len(frame_buffers)
    update_plot()


def show_previous(event):
    global current_index
    current_index = (current_index - 1) % len(frame_buffers)
    update_plot()


def on_key(event):
    if event.key == "right":
        show_next(event)
    elif event.key == "left":
        show_previous(event)


ax_prev = plt.axes([0.3, 0.05, 0.15, 0.075])
ax_next = plt.axes([0.55, 0.05, 0.15, 0.075])
btn_prev = Button(ax_prev, "\u2190 Previous")
btn_next = Button(ax_next, "Next \u2192")
btn_prev.on_clicked(show_previous)
btn_next.on_clicked(show_next)
fig.canvas.mpl_connect("key_press_event", on_key)

plt.show()