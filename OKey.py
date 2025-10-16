import evdev
import pygame
import threading
import sounddevice as sd

import consts
import face
import mic

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
    frames_left_to_show_text = consts.CLEAR_SCREEN_FRAMES
    text = text[text.index("(")+1:text.index(")")].removeprefix("KEY_").lower()
    if text in consts.CHANGE:
        text = consts.CHANGE[text]
    if shift:
        if text in consts.SHIFT_CHANGE:
            text = consts.SHIFT_CHANGE[text]
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
    if len(events)>consts.TEXT_LEN:
        events = events[-consts.TEXT_LEN:]
    if events in consts.WORKFLOW_CHANGE:
        events = consts.WORKFLOW_CHANGE[events]

def render(text):
    global frames_left_to_show_text
    if frames_left_to_show_text>0:
        return text.center(consts.TEXT_LEN) 
    return face.face(frame_time+1, mouse_clicked, mic.talking_frames>0)

pygame.init()
screen = pygame.display.set_mode(consts.WINDOW_SIZE)
pygame.display.set_caption(consts.WINDOW_NAME)
if consts.MIC_ON:
    stream = sd.InputStream(callback=mic.callback)

PYGAME_FONT = pygame.font.Font(consts.FONT_PATH, consts.FONT_SIZE)

clock = pygame.time.Clock()


keyboard = mouse = None
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if consts.KEYBOARD_NAME in device.name:
        keyboard = evdev.InputDevice(device.path)
    elif consts.MOUSE_NAME in device.name:
        mouse = evdev.InputDevice(device.path)

def listen_keyboard():
    global events
    if keyboard is None:
        raise ValueError("Couldn't find keyboard input :c")
    for event in keyboard.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            display(key_event)
def listen_mouse():
    global events, mouse_clicked
    if mouse is None:
        raise ValueError("Couldn't find mouse input :c")
    for event in mouse.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            if key_event.endswith("down"):
                mouse_clicked = True
            elif key_event.endswith("up"):
                mouse_clicked = False

# Start threads to listen on keyboard and mouse
threading.Thread(target=listen_keyboard, daemon=True).start()
if consts.MOUSE_ON:
    threading.Thread(target=listen_mouse, daemon=True).start()

running = True
if stream is not None:
    stream.start()
while running:
    screen.fill(consts.BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text_surface = PYGAME_FONT.render(render(events), consts.ANTIALIAS_ENABLED, consts.WHITE)
    screen.blit(text_surface, consts.TEXT_POS)

    pygame.display.flip()
    if frames_left_to_show_text>0:
        frames_left_to_show_text -= 1
    else:
        events = ""

    if mic.talking_frames>0:
        mic.talking_frames -= 1

    frame_time = (frame_time+1)%face.FRAMES_FOR_ONE_MOVE
    mic.talking_frames
    clock.tick(consts.FPS)

pygame.quit()
if stream is not None:
    stream.stop()
    stream.close()
