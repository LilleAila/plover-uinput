# This is a very simple keyboard capture.
# For now, it only reads events and prints them, and is not integrated with the rest of the code
# TODO: do something using this, if possible: https://plover.readthedocs.io/en/latest/hardware_communication.html#capture
# https://python-evdev.readthedocs.io/en/latest/tutorial.html
from evdev import InputDevice, list_devices, ecodes as e, categorize, util, UInput
from select import select

res = util.find_ecodes_by_regex(r"KEY_.*")
ui = UInput(res)
ui2 = UInput(res)
ui3 = UInput(res)

print(ui.name, ui.phys)
print(ui2.name, ui2.phys)
print(ui3.name, ui3.phys)


def is_mouse(device):
    capabilities = device.capabilities()
    return e.EV_REL in capabilities or e.EV_ABS in capabilities


def is_uinput(device):
    return device.name == "py-evdev-uinput" or device.phys == "py-evdev-uinput"


def filter_devices(device):
    return not is_mouse(device) and not is_uinput(device)


def get_devices():
    input_devices = [InputDevice(path) for path in list_devices()]
    print(input_devices)
    keyboard_devices = [dev for dev in input_devices if filter_devices(dev)]
    return {dev.fd: dev for dev in keyboard_devices}


devices = get_devices()

import time

start_time = time.time()

[dev.grab() for dev in devices.values()]

ui.write(e.EV_KEY, e.KEY_A, 1)
ui.write(e.EV_KEY, e.KEY_A, 0)
ui.syn()


ui2.write(e.EV_KEY, e.KEY_A, 1)
ui2.write(e.EV_KEY, e.KEY_A, 0)
ui2.syn()


ui3.write(e.EV_KEY, e.KEY_A, 1)
ui3.write(e.EV_KEY, e.KEY_A, 0)
ui3.syn()

while True:
    r, _, _ = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            print(categorize(event))
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > 3:
        break

[dev.ungrab() for dev in devices.values()]
