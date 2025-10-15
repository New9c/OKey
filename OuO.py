import evdev
import pygame
import threading

# Initialize pygame
ctrl, mod, alt, shift = False, False, False, False
specials = False
FPS = 30
CLEAR_SCREEN_FRAMES = 60
display_text = 0
frame_time = 0
change = {
    "e": "f",
    "r": "p",
    "t": "g",
    "y": "j",
    "u": "k",
    "i": "u",
    "o": "y",
    "p": ";",
    "s": "r",
    "d": "s",
    "f": "t",
    "g": "d",
    "j": "n",
    "k": "e",
    "l": "i",
    "semicolon": "o",
    "n": "k",
    "comma": ",",
    "dot": ".",
    "slash": "/",
    "apostrophe": "'",
    "leftbrace": "[",
    "rightbrace": "]",
    "backslash": "\\",
    "minus": "-",
    "equal": "=",
}
shift_change = {
    "1": "!",
    "2": "@",
    "3": "#",
    "4": "$",
    "5": "%",
    "6": "^",
    "7": "&",
    "8": "*",
    "9": "(",
    "0": ")",
    "-": "_",
    "=": "+",
    "\\": "|",
    "[": "{",
    "]": "}",
    ";": ":",
    "'": '"',
    ",": '<',
    ".": '>',
    "/": '?',
}
events = ""
specials = False

def display(text: str):
    global display_text, change, ctrl, alt, mod, shift, events, specials
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
    elif "esc" in text.lower() and text.endswith("down"):
        display_text = CLEAR_SCREEN_FRAMES
        events = "Esc"
        return
    elif "enter" in text.lower() and text.endswith("down"):
        specials = True
        display_text = CLEAR_SCREEN_FRAMES
        events = "Enter"
        return
    elif "backspace" in text.lower() and text.endswith("down"):
        specials = True
        display_text = CLEAR_SCREEN_FRAMES
        events = "Backspace"
        return

    if not text.endswith("down"):
        return
    display_text = CLEAR_SCREEN_FRAMES
    text = text[text.index("(")+1:text.index(")")].removeprefix("KEY_").lower()
    if text in change:
        text = change[text]
    if shift:
        if text in shift_change:
            text = shift_change[text]
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
    if len(events)>64:
        events = events[-64:]

def render(text):
    global display_text
    if display_text:
        return text.center(64) 
    elif frame_time<BLINK_FRAME-15:
        return "O u O".center(64)
    return "1 u 1".center(64)

pygame.init()
screen = pygame.display.set_mode((1870, 80))

FONT_PATH = "/home/ninc/.local/share/fonts/JetBrains/JetBrainsMonoNerdFont-Regular.ttf"
FONT_SIZE = 50
COVE_FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
BLINK_FRAME = 150

WHITE = (255, 255, 255)

clock = pygame.time.Clock()


keyboard = evdev.InputDevice('/dev/input/event10')
mouse = evdev.InputDevice('/dev/input/event11')

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    if device.name == "keyd virtual keyboard":
        keyboard = evdev.InputDevice(device.path)
        print(device.name)
    elif "Logitech" in device.name:
        mouse = evdev.InputDevice(device.path)
        print(device.name)

def listen_keyboard():
    global events
    for event in keyboard.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            display(key_event)
def listen_mouse():
    global events
    for event in mouse.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = str(evdev.categorize(event))
            print(key_event)

# Start threads to listen on keyboard and mouse
threading.Thread(target=listen_keyboard, daemon=True).start()
threading.Thread(target=listen_mouse, daemon=True).start()

running = True
while running:
    screen.fill((18, 16, 32))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text_surface = COVE_FONT.render(render(events), True, WHITE)
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()
    if display_text:
        display_text -= 1
    else:
        events = ""
    frame_time = (frame_time+1)%BLINK_FRAME
    clock.tick(FPS)

pygame.quit()
