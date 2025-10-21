# OKey
## About

## Prerequisites
- As this uses evdev for detecting inputs, you need to be on a linux OS (sry windows/mac ono)
- You'll need to add your user to the "input" user group, else the "No devices are found :(" error shall remind you
    - `sudo usermod -a -G input USER_NAME`
- You'll need to install a PortAudio library on your machine if it displays an OS error. This is `libportaudio2` or something similar (future plans: make the library not needed if the mic is set as off)
- (Optional) It is prefered to use a nerd font for your terminal, so icons from the [nerd font cheat sheet](https://www.nerdfonts.com/cheat-sheet) are displayed correctly

## Installation
### Quick Install
<details>
<summary>bash</summary>
<br>

```bash
LATEST_VERSION=$(curl -s "https://api.github.com/repos/New9c/OKey/releases/latest" | grep -oP '"tag_name":\s*"\K(.*)(?=")')
# echo "Latest release version: $LATEST_VERSION"
sudo curl -L "https://github.com/New9c/OKey/releases/download/$LATEST_VERSION/OKey" -o /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
</details>

<details>
<summary>fish</summary>
<br>

```fish
set LATEST_VERSION $(curl -s "https://api.github.com/repos/New9c/OKey/releases/latest" | grep -oP '"tag_name":\s*"\K(.*)(?=")')
# echo "Latest release version: $LATEST_VERSION"
sudo curl -L "https://github.com/New9c/OKey/releases/download/$LATEST_VERSION/OKey" -o /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
</details>

### Manual Install
Running the code directly:
```sh
git clone https://github.com/New9c/OKey.git
cd OKey/
# make sure you are in a proper env
pip install -r requirements.txt
python OKey.py # run OKey
```

if this works, build it with pyinstaller
```sh
# make sure you are in the OKey/ directory
pyinstaller --onefile --add-data "basic.yaml:." --add-data "JetBrainsMonoNerdFont-Regular.ttf:." OKey.py
sudo cp dist/OKey /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
If running `OKey` doesn't lanuch the screen, probably one of the prerequisites aren't met.
Once you can see the OuO face (whether the keys are being correctly captured or not), start changing the config.
## Configuration
OKey works by having a config file at ~/.config/OKey/config.yaml, if not found it will create a basic one for you.
### Mandatory Config Changes
There are two configs you have to change: `keyboard_name` and `mouse_name`. 
If you don't want to capture mouse inputs, set `mouse_on` to `false`.
On startup, You'll see some info about your input settings, here is a bit of mine:
```
Logitech MX Master 3S
 Keyboard: RK61Plus5.0 Keyboard
WARNING: 'RK61Plus5.0 Keyboard' isn't 'keyboard', if this is the correct keyboard, set keyboard_name to 'RK61Plus5.0 Keyboard'.
keyd virtual pointer
keyd virtual keyboard
ASUE1407:00 04F3:310D Keyboard
ASUE1407:00 04F3:310D Touchpad
󰍽 Mouse: ASUE1407:00 04F3:310D Mouse
WARNING: 'ASUE1407:00 04F3:310D Mouse' isn't 'mouse', if this is the correct mouse, set mouse_name to 'ASUE1407:00 04F3:310D Mouse'.
```
In this case, both the mouse and the keyboard aren't correct, as in OKey isn't displaying any of my inputs.
Even if it does work, you should still set the names to be your exact devices, like the warnings say.
You can use `evtest` to check whether an option is the one you want.

I personally use [keyd]() to remap CapsLock to Ctrl when held like a modifier key and Esc when quickly pressed like a normal key, and I would recommend you to remap your CapsLock key too. For OKey's purposes though, `keyd monitor` gives the clearest showcase of what inputs are happening and where they are from.
```
keyd virtual keyboard	0fac:0ade:bea394c0	s down
keyd virtual keyboard	0fac:0ade:bea394c0	s up
ASUE1407:00 04F3:310D Touchpad	04f3:310d:beedd0e4	leftmouse down
ASUE1407:00 04F3:310D Touchpad	04f3:310d:beedd0e4	leftmouse up
```
With this it's clear that I should set "keyd virtual keyboard" as the keyboard and "ASUE1407:00 04F3:310D Touchpad" for the mouse
### Other Configs
**Please check out all the settings!** You never know if you can change something that you thought you couldn't change!
## Inspiration + More Keypress Displayers
(I'll call these pieces of software that show your key presses as keypress displayers, but I don't think there is a clear term made for this yet, despite the growing amount of them)

After seeing [ThePrimeagen]() use a keypress displayer, I wanted to have one myself.
Here are the main two I've tried using:
[screenkey](https://gitlab.com/screenkey/screenkey)
[showmethekey](https://github.com/AlynxZhou/showmethekey)

Both are pretty high quality I believe, but screenkey is not quite made for wayland, which I use.
I really liked showmethekey, so much so that I added [a bit of documentation](https://github.com/AlynxZhou/showmethekey/pull/84) for it. However, it didn't allow for better customization for how the keys are shown, and had a kind of annoying settings menu pop up every time I started it.

Therefore, I made my own keypress displayer, with as many customization options as I could. It's named OKey as I wondered if OuOKey was a bit odd, and shortened it cause of words and phrases like "okay" and "okey dokey". This wasn't quite at first made for the masses, which is why certain features (twitch) are so niche. I'll still add more options if I think some settings may be liked by certain people, or that the default behavior could be disliked.

## Future Plans
(None of these are guarentees, I may get busy or create a new project, these are just some ideas I have)
- [ ] Allow Mod keys to be shown side by side with the normal keys
- [ ] Add a pause keybind to allow pausing
- [ ] Make PortAudio not required when mic is off
- [ ] Make a more flexable face system allowing users to make animations
- [ ] Windows/Mac OS support?

