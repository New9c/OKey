import os, yaml, shutil

found_valid_config = False
try_setting = True
BASE_CONFIG = "basic.yaml"
CONFIG_DIR = os.path.expanduser('~/.config/OKey')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yaml')

if not os.path.isfile(CONFIG_FILE):
    print("~/.config/OKey/config.yaml not found. Making basic config...")
    os.makedirs(CONFIG_DIR, exist_ok=True)  # safely create directory if needed
    shutil.copyfile(BASE_CONFIG, CONFIG_FILE)

while try_setting:
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        MOUSE_ON = data['mouse_on']
        MIC_ON = data['mic_on']
        
        ACTION_INTERVAL = data['action_interval']
        
        TEXT_LEN = data['text_len']
        
        WINDOW_SIZE = tuple(data['window_size'])
        WINDOW_NAME = data['window_name']
        
        TEXT_COLOR = tuple(data['text_color'])
        BG_COLOR = tuple(data['bg_color'])
        TWITCH_COLOR = tuple(data['twitch_color'])
        
        TEXT_POS = tuple(data['text_pos'])
        
        KEYBOARD_NAME = data['keyboard_name']
        MOUSE_NAME = data['mouse_name']
        
        TEXT_ANTIALIAS = data['text_antialias']
        FPS = data['fps']
        CLEAR_SCREEN_FRAMES = data['clear_screen_frames']
        CLEAR_TWITCH_FRAMES = data['clear_twitch_frames']
        
        FONT_PATH = data['font_path']
        FONT_SIZE = data['font_size']
        
        CHANGE = data['change']
        SHIFT_CHANGE = data['shift_change']
        WORKFLOW_CHANGE = data['workflow_change']
        found_valid_config = True
        try_setting = False
    except AttributeError and KeyError:
        ans = input("Found invalid config file, remake default config file(y/n)? ")
        while ans.lower() not in ['yes', 'no', 'y', 'n']:
            print("Please input y/n/yes/no")
            ans = input("Found invalid config file, remake default config file(y/n)? ")
        if 'y' in ans.lower():
            print("Making basic config...")
            shutil.copyfile(BASE_CONFIG, CONFIG_FILE)
        else:
            try_setting = False
