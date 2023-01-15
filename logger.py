import numpy as np
import serial.tools.list_ports
import time
from time import sleep
import json
import matplotlib.pyplot as plt
import keyboard
import csv


def plotting(time_plt, temperature_plt, ref_plt, u_plt, error_plt):
    plt.clf()
    plt.subplot(3, 1, 1)
    plt.plot(time_plt, temperature_plt, time, ref_plt)
    plt.title("BMP280 logger")
    plt.ylabel("Temperature [C]")
    plt.legend(["Current", "Reference point"])
    plt.xticks([])

    plt.subplot(3, 1, 2)
    plt.plot(time_plt, u_plt)
    plt.legend('Control signal')
    plt.ylabel("PWM Duty [%]")
    plt.xticks([])

    plt.subplot(3, 1, 3)
    plt.plot(time_plt, error_plt)
    plt.legend('Error')
    plt.ylabel("Temperature [C]")
    plt.xlabel("Time [s]")

    plt.show()
    plt.pause(0.0001)


port = serial.tools.list_ports.comports()
serial_init = serial.Serial()
ports = []
for i in port:
    ports.append(str(i))
    print(str(i))

# create a file
# time_str = time.strftime("%Y%m%d-%H%M%S")
# file = with open("data_open_loop_object%s.csv" % time_str, "w")

# file_csv = csv.DictWriter(file, fieldnames=name)
# receiver assigment
receiver = serial.Serial('COM6', 115200, timeout=1, parity=serial.PARITY_NONE)

# enable plot update
plt.ion()

# time declaration
t = []
t_max = 0

# JSON data properties assigment
temperature = []
u = []
ref = []
error = []
sample = []
u_prev = 10000
while True:
    text = receiver.readline()
    temp = [0, 0, 0, 0]

    try:
        sample = json.loads(text)
        temp = [sample["temperature"], sample["ref"], sample["u"], sample["error"]]
        if temp[2] == '':
            temp[2] = u_prev
        else:
            u_prev = temp[2]
    except ValueError:
        print("Bad JSON\n")
        print(temp)
        receiver.flush()
        receiver.reset_input_buffer()
    # file.write("%.2f," % float(temp[0]))
    file.writeheader
    temperature.append(temp[0])
    ref.append(temp[1])
    u.append(temp[2])
    error.append(temp[3])
    t.append(t_max)
    t_max += 1

    plotting(t, temperature, ref, u, error)

    if keyboard.is_pressed('q') | keyboard.is_pressed('Q'):
        break

receiver.close()
file.close()
