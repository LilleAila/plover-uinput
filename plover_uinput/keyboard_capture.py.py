# This is a very simple keyboard capture.
# For now, it only reads events and prints them, and is not integrated with the rest of the code
# TODO: do something using this, if possible: https://plover.readthedocs.io/en/latest/hardware_communication.html#capture
# https://python-evdev.readthedocs.io/en/latest/tutorial.html
from evdev import InputDevice, list_devices, ecodes, categorize
from select import select

devices = [InputDevice(path) for path in list_devices()]
devices = {dev.fd: dev for dev in devices}

while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            if event.type == ecodes.EV_KEY:
                print(event)
                print(categorize(event))
