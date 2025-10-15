import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)

keyboard = evdev.InputDevice('/dev/input/event20')
keyboard.active_keys(verbose=True)
for event in keyboard.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
