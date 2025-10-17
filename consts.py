from platformdirs import user_config_dir
import os, yaml, shutil

found_valid_config = False
try_setting = True
BASE_CONFIG = "basic.yaml"
BASE_FONT = "JetBrainsMonoNerdFont-Regular.ttf"
CONFIG_DIR = user_config_dir("OKey")
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yaml')
MAIN_FONT = os.path.join(CONFIG_DIR, 'JetBrainsMonoNerdFont-Regular.ttf')

with open(BASE_CONFIG, 'r') as file:
    BASE_SETTINGS = yaml.load(file, Loader=yaml.SafeLoader)
# Replace FONT_PATH with real path
with open(CONFIG_FILE, 'r') as file:
    content = file.read()
new_content = content.replace("FONT_PATH", MAIN_FONT)
with open(CONFIG_FILE, 'w') as file:
    file.write(new_content)

if not os.path.isfile(CONFIG_FILE):
    print(f"{CONFIG_FILE} not found. Making basic config...")
    os.makedirs(CONFIG_DIR, exist_ok=True)  # safely create directory if needed
    shutil.copyfile(BASE_CONFIG, CONFIG_FILE)
    shutil.copyfile(BASE_FONT, MAIN_FONT)

with open(CONFIG_FILE, 'r') as file:
    SETTINGS = yaml.load(file, Loader=yaml.SafeLoader)
for setting in BASE_SETTINGS:
    if setting not in SETTINGS:
        ans = input(f"{setting} not found in config file, reset to default config (y/n)? ")
        while ans.lower() not in ['yes', 'no', 'y', 'n']:
            print("Please input y/n/yes/no")
            ans = input(f"{setting} not found in config file, reset to default config (y/n)? ")
        if 'y' in ans.lower():
            print("Resetting config...")
            shutil.copyfile(BASE_CONFIG, CONFIG_FILE)
            shutil.copyfile(BASE_FONT, MAIN_FONT)
            break
with open(CONFIG_FILE, 'r') as file:
    SETTINGS = yaml.load(file, Loader=yaml.SafeLoader)
for setting in BASE_SETTINGS:
    if setting not in SETTINGS:
        print("Invalid config file found, using defaults for now")
        SETTINGS = BASE_SETTINGS
        SETTINGS["font_path"] = BASE_FONT
