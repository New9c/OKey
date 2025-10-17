import os
import evdev
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import threading
import sounddevice as sd

from consts import SETTINGS, CONFIG_FILE
import face
import mic
import twitch
ctrl, mod, alt, shift = False, False, False, False
mouse_clicked = False
specials = False
frames_left_to_show_text = 0
frame_time = 0
events = ""
specials = False
stream = None

def display(text: str):
    global frames_left_to_show_text, ctrl, alt, mod, shift, events, specials
    if "ctrl" in text.lower():
        if text.endswith("down"):
            ctrl = True
        elif text.endswith("up"):
            ctrl = False
        return
    elif "shift" in text.lower():
        if text.endswith("down"):
            shift = True
        elif text.endswith("up"):
            shift = False
        return
    elif "alt" in text.lower():
        if text.endswith("down"):
            alt = True
        elif text.endswith("up"):
            alt = False
        return
    elif "meta" in text.lower():
        if text.endswith("down"):
            mod = True
        elif text.endswith("up"):
            mod = False
        return

    if not text.endswith("down"):
        return
    frames_left_to_show_text = SETTINGS["clear_text_frames"]
    text = text[text.index("(")+1:text.index(")")].removeprefix("KEY_").lower()
    if text in SETTINGS["change"]:
        text = SETTINGS["change"][text]
    if shift:
        if text in SETTINGS["shift_change"]:
            text = SETTINGS["shift_change"][text]
        else:
            text = text.upper()
    was_special = specials
    specials = ctrl or mod or alt
    if specials: 
        text = f"{"Ctrl+" if ctrl else ""}{"Mod+" if mod else ""}{"Alt+" if alt else ""}{text}"
        events = text
    else:
        if was_special:
            events = ""
        events += text
    if len(events)>SETTINGS["text_len"]:
        events = events[-SETTINGS["text_len"]:]
    if events in SETTINGS["workflow_change"]:
        events = SETTINGS["workflow_change"][events]

def render(text):
    global frames_left_to_show_text
    if twitch.message_frames>0:
        return twitch.twitch_msg.center(SETTINGS["text_len"]) 
    elif frames_left_to_show_text>0:
        return text.center(SETTINGS["text_len"]) 
    return face.face(frame_time+1, mouse_clicked, mic.talking_frames>0)

pygame.init()
screen = pygame.display.set_mode(SETTINGS["window_size"])
pygame.display.set_caption(SETTINGS["window_name"])
if SETTINGS["mic_on"]:
    stream = sd.InputStream(callback=mic.callback)

PYGAME_FONT = pygame.font.Font(SETTINGS["font_path"], SETTINGS["font_size"])

clock = pygame.time.Clock()


keyboard = mouse = None
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
if SETTINGS["show_basic_settings_on_start"]:
    print(f"Tracking mouse = {SETTINGS["mouse_on"]}")
    print(f"Tracking whether talking = {SETTINGS["mic_on"]}")
    print(f"Checking twitch chat with iirc = {SETTINGS["using_twitch"]}")
    print()
for device in devices:
    if SETTINGS["keyboard_name"].lower() in device.name.lower() and keyboard is None:
        keyboard = evdev.InputDevice(device.path)
        if SETTINGS["show_basic_settings_on_start"]:
            print("    Keyboard: ", end="")
    elif SETTINGS["mouse_name"].lower() in device.name.lower() and mouse is None:
        mouse = evdev.InputDevice(device.path)
        if SETTINGS["show_basic_settings_on_start"]:
            print("   󰍽 Mouse: ", end="")
    if SETTINGS["show_basic_settings_on_start"]:
        print(device.name)

def listen_keyboard():
    global events
    if keyboard is None:
        raise ValueError(f"Couldn't find keyboard input :c Try setting the keyboard_name in {CONFIG_FILE} to one of the printed devices on startup")
    for event in keyboard.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            display(key_event)
def listen_mouse():
    global events, mouse_clicked
    if mouse is None:
        raise ValueError(f"Couldn't find mouse input :c Try setting the mouse_name in {CONFIG_FILE} to one of the printed devices on startup, or have mouse_on set to false")
    for event in mouse.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            if key_event.endswith("down"):
                mouse_clicked = True
            elif key_event.endswith("up"):
                mouse_clicked = False

# Start threads to listen on keyboard and mouse
threading.Thread(target=listen_keyboard, daemon=True).start()
if SETTINGS["mouse_on"]:
    threading.Thread(target=listen_mouse, daemon=True).start()
if SETTINGS["using_twitch"]:
    threading.Thread(target=twitch.start, daemon=True).start()

running = True
if stream is not None:
    stream.start()
while running:
    if twitch.message_frames>0:
        screen.fill(SETTINGS["twitch_color"])
    else:
        screen.fill(SETTINGS["bg_color"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text_surface = PYGAME_FONT.render(render(events), SETTINGS["text_antialias"], SETTINGS["text_color"])
    screen.blit(text_surface, SETTINGS["text_pos"])

    pygame.display.flip()
    if frames_left_to_show_text>0:
        frames_left_to_show_text -= 1
    else:
        events = ""

    if mic.talking_frames>0:
        mic.talking_frames -= 1
    if twitch.message_frames>0:
        twitch.message_frames -= 1

    frame_time = (frame_time+1)%face.FRAMES_FOR_ONE_MOVE
    clock.tick(SETTINGS["fps"])

pygame.quit()
if stream is not None:
    stream.stop()
    stream.close()
