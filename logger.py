import numpy as np
import serial.tools.list_ports
from time import sleep
import json
import matplotlib.pyplot as plt
import keyboard


def port_checker():
    port = serial.tools.list_ports.comports()
    serial_init = serial.Serial()
    ports = []
    for i in port:
        ports.append(str(i))
        print(str(i))


def serial_config():
    serial_port = serial.Serial('COM6', 115200, timeout=1, parity=serial.PARITY_NONE)


def log_run():
    t = []
    temperature = []
    u =[]


if __name__ == "main":
    port_checker()
