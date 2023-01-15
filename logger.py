import numpy as np
import serial.tools.list_ports
from time import sleep
import json
import matplotlib.pyplot as plt
import keyboard


def plotting(time, temperature_plt, ref_plt, u_plt, error_plt):

    plt.clf()
    plt.subplot(3, 1, 1)
    plt.plot(time, temperature_plt, time, ref_plt)
    plt.title("BMP280 logger")
    plt.ylabel("Temperature [C]")
    plt.legend(["Current", "Reference point"])
    # plt.ylim([min(temperature_plt) - 1, max(temperature_plt) + 1])
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(time, u_plt)
    plt.legend('Control signal')
    plt.ylabel("PWM Duty [%]")
    plt.ylim([-1, 101])
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(time, error_plt)
    plt.legend('Error')
    plt.ylabel("Temperature [C]")
    plt.xlabel("Time [s]")
    # plt.ylim([0.1, max(error_plt)])
    plt.grid()

    plt.show()
    plt.pause(0.0001)


port = serial.tools.list_ports.comports()
serial_init = serial.Serial()
ports = []
for i in port:
    ports.append(str(i))
    print(str(i))

plt.ion()

# receiver assigment
receiver = serial.Serial('COM6', 115200, timeout=1, parity=serial.PARITY_NONE)

# time declaration
t = []
t_max = 0

# JSON data properties assigment
temperature = []
u = []
ref = []
error = []
sample = []

while True:
    text = receiver.readline()
    temp = [0, 0, 0, 0]
    u_prev = 10000
    try:
        sample = json.loads(text)
        temp = [sample["temperature"], sample["ref"], sample["u"], sample["error"]]
        if temp[2] == '':
            temp[2] = u_prev
        else:
            u_prev = temp[2]
    except ValueError:
        print("Bad JSON\n")
        # print(temp)
        receiver.flush()
        receiver.reset_input_buffer()
    temperature.append(temp[0])
    u.append(temp[1])
    ref.append(temp[2])
    error.append(temp[3])
    t.append(t_max)
    t_max += 1

    plotting(t, temperature, ref, u, error)

    if keyboard.is_pressed('q') | keyboard.is_pressed('Q'):
        break

receiver.close()

