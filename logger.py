import csv
import json
import threading
import time

import keyboard
import matplotlib.pyplot as plt
import serial.tools.list_ports

val = 26.0


def console_handler():
    global val
    while True:
        val = input()
        val = round(float(val), 2)
        if val < 0.0:
            receiver.write(b'0000')
        elif val > 99.99:
            receiver.write(b'9999')
        else:
            receiver.write(str(val * 100).encode())


def plotting(time_plt, temperature_plt, ref_plt, u_plt, error_plt):
    plt.clf()
    plt.subplot(3, 1, 1)
    plt.plot(time_plt, temperature_plt, time_plt, ref_plt)
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


# input from console handler
print("If you would like to change reference temperature just type it BELOW")
print("Available range of temperatures [0; 99.98] AND 99.99 is CODE VALUE to change duty control source")
print("Required temperature =")

# thread initialization and start for console reference temperature control
thread = threading.Thread(target=console_handler)
thread.start()

# create a file
time_str = time.strftime("%Y%m%d-%H%M%S")
file = open("data_close_loop_object%s.csv" % time_str, "a", newline='')


# initialize columns and assign names to them
writer = csv.DictWriter(file, fieldnames=["temperature", "ref", "u", "error"])
writer.writeheader()


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

    # CSV file writer -- ALL data
    writer.writerow(sample)

    temperature.append(float(temp[0]))
    ref.append(float(temp[1]))
    u.append(float(temp[2]))
    error.append(float(temp[3]))
    t.append(t_max)
    t_max += 1

    plotting(t, temperature, ref, u, error)

    # exit using keyboard
    if keyboard.is_pressed('q') | keyboard.is_pressed('Q'):
        break


receiver.close()
file.close()

