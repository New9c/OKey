<h1 align="center">OKey</h1>
<p align="center">Shows your key presses, with a cute face! OuO</p>
<p align="center">

https://github.com/user-attachments/assets/461d676e-772c-45ca-a12d-d9c537c5abbb

</p>

## Features
- As configurable as it gets: [Full list of configs](https://github.com/New9c/OKey?tab=readme-ov-file#all-configs)
- A cute face! OuO
- Mouse click displays
- Sound detection (make the face talk O>O)
- Twitch chat reader (good for if you're streaming)

## Prerequisites
- As this uses evdev for detecting inputs, you need to be on a linux OS. (sry windows/mac ono)
- You'll need to add your user to the "input" user group, else the "No devices are found :(" error shall remind you.
    - `sudo usermod -a -G input USER_NAME`
- You'll need to install a PortAudio library on your machine if it displays an OS error. This is `libportaudio2` or something similar. (future plans: make the library not needed if the mic is set as off)
- (Optional) It is prefered to use a nerd font for your terminal, so icons from the [nerd font cheat sheet](https://www.nerdfonts.com/cheat-sheet) are displayed correctly.

## Installation
### Quick Install
<details>
<summary>AUR package: okey-git</summary>
<br>

```sh
# You may need to update your AUR helper, as I added this quite recently
# yay -Syu
yay -S okey-git
```
</details>
<details>
<summary>Bash</summary>
<br>

```bash
LATEST_VERSION=$(curl -s "https://api.github.com/repos/New9c/OKey/releases/latest" | grep -oP '"tag_name":\s*"\K(.*)(?=")')
# echo "Latest release version: $LATEST_VERSION"
sudo curl -L "https://github.com/New9c/OKey/releases/download/$LATEST_VERSION/OKey" -o /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
</details>

<details>
<summary>Fish</summary>
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

If this works, build it with pyinstaller:
```sh
# make sure you are in the OKey/ directory
pyinstaller --onefile --add-data "basic.yaml:." --add-data "JetBrainsMonoNerdFont-Regular.ttf:." OKey.py
sudo cp dist/OKey /usr/local/bin/OKey
sudo chmod +x /usr/local/bin/OKey
```
If running `OKey` doesn't lanuch the screen, probably one of the prerequisites aren't met.
Once you can see the OuO face (whether the keys are being correctly captured or not), start changing the config.
## Configuration
OKey works by having a config file at `~/.config/OKey/config.yaml`, if it's not found one will be created for you.
### Mandatory Config Changes
There are two configs you have to change: `keyboard_name` and `mouse_name`. <br>
If you don't want to capture mouse inputs, set `mouse_on` to `false`.<br>
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
In this case, both the mouse and the keyboard aren't correct, as in OKey isn't displaying any of my inputs.<br>
Even if it does work, you should still set the names to be your exact devices, like the warnings say.<br><br>
You can use `evtest` to check whether an option is the one you want.<br>
If you've installed [keyd](https://github.com/rvaiya/keyd), you can use `keyd monitor` to see where inputs come from:
```
keyd virtual keyboard	0fac:0ade:bea394c0	s down
keyd virtual keyboard	0fac:0ade:bea394c0	s up
ASUE1407:00 04F3:310D Touchpad	04f3:310d:beedd0e4	leftmouse down
ASUE1407:00 04F3:310D Touchpad	04f3:310d:beedd0e4	leftmouse up
```
With this it's clear that I should set "keyd virtual keyboard" as the keyboard and "ASUE1407:00 04F3:310D Touchpad" for the mouse
### All Configs
**Please check out all the settings!** You never know if you can change something that you thought you couldn't change! <br>
I believe all of the settings should be easy to understand, but just in case, I made the full detailed explaination for every setting below.
<details>
<summary> Full List of Configs </summary>

```
show_basic_settings_on_start: In the terminal, shows whether your mouse is detected, mic is detected, and whether a twitch chat is checked, then shows the input devices. Good for trouble shooting at the start.

keyboard_name: Your keyboard's name. Set it to be exactly the same as the input device name.
mouse_name: Your keyboard's name. Set it to be exactly the same as the input device name.

mouse_on: Enable/Disable mouse displays
mic_on: Enable/Disable having the face talk

mic_threshold: How loud sounds have to be to make the face talk
print_loudness: Prints how loud it is currently to the terminal, made specifically for setting the mic_threshold

face_normal_eye: What string/char is used to represent the eye normally
face_click_eye: What string/char is used to represent the eye when a mouse button is pressed
face_normal_mouth: What string/char is used to represent the mouth normally
face_talking_mouth: What string/char is used to represent the mouth when talking
replace_char_as_eye: See face_animation
replace_char_as_mouth: See face_animation
face_animation: Where the animation is made, every block should be [last_frame, look]. 
For the look, every e will become an eye, reacting to mouse clicks, every m will become a mouth, reacting to sounds allowing talking.
If you need the letters e and m for something, you can choose other characters to symbolize eyes and mouths with the replace_char_as_eye/mouth setting.

text_len: How many characters can be shown together at once. You should change this if you adjusted the window size.

window_size: The window size, [width(px), height(px)]
window_name: The name of the window

text_color: RGB value of the text color
bg_color: RGB value of the background color
twitch_color: RGB value of the background color when a twitch chat message is displayed

text_pos: The offset of the text relative to the left top corner. Note that since text is centered, it may be helpful to type text_len (ex: 59) characters to see how far the most left character is from the left top corner.

text_antialias: TLDR, makes the text smoother. I don't know much about antialias, so a google search may help :3
fps: How often the display updates, setting it too high could eat up resources
clear_text_frames: How long it'll take for text on the screen to be removed (Do quick math for seconds, ex: 60/30 = 2 seconds)
clear_talking_frames: After becoming quiet, how long it'll take for the mouth to close, needs to be at least one for mouth to work
clear_twitch_frames: How long it'll take for twitch chat message on the screen to be removed

font_path: Where it'll find the font to use. Use absolute paths. A nerd font is highly recommended.
font_size: How large the font is, the bigger the number the bigger the size (c'mon you know this)

using_twitch: Whether or not you want to check twitch messages
print_twitch_msg: Print twitch messages to the terminal
which_chat_to_check: Which streamers chat to check, usually it's your own
twitch_ignore_names: Which names to ignore, usually your bots and yourself

ctrl_text: How ctrl will be displayed
mod_text: How mod will be displayed, this is called Windows or Command in some cases
alt_text: How alt will be displayed


change: Change how a character (or string) is shown. This is where you convert the qwerty layout to your own layout (ex: "e": "f" as I use colemak), or set an icon for special buttons (ex: F1 can be a mute button if that is what you use it for, or show both F1 and the icon, go nuts!)

shift_change: Change what shift does to a character, if not listed the string/char will just be capitalized

workflow_change: Final change: if you want something to look quite different, such as Alt+F4 to show a delete icon, this is where you do it! Great for showcasing your custom keybinds. Leave empty for no change.
```
</details>
The code trys to resolve errors such as missing config settings, but it currently still assumes the type of the config parameter (ex: int or str) to be correct and will have errors if it isn't. If the config isn't quite working, I'd recommend deleting the config file and starting over.

## Inspiration + More Keypress Displayers
(I'll call these pieces of software that show your key presses as keypress displayers, but I don't think there is a clear term made for this yet, despite the growing amount of them) <br>

After seeing [ThePrimeagen](https://www.youtube.com/@ThePrimeTimeagen) use a keypress displayer, I wanted to have one myself.<br>
Here are the main two I've tried using:<br>
- [screenkey](https://gitlab.com/screenkey/screenkey)
- [showmethekey](https://github.com/AlynxZhou/showmethekey)

Both are pretty high quality I believe, but screenkey is not quite made for wayland, which I use.<br>
I really liked showmethekey, so much so that I added [a bit of documentation](https://github.com/AlynxZhou/showmethekey/pull/84) for it. However, it didn't allow for better customization for how the keys are shown, and had a kind of annoying settings menu pop up every time I started it.

Therefore, I made my own keypress displayer, with as many customization options as I could. It's named OKey as I wondered if OuOKey was a bit odd, and shortened it cause of words and phrases like "okay" and "okey dokey".<br>
This wasn't quite at first made for the masses, which is why certain features (twitch) are so niche. I'll still add more options if I think some settings may be liked by certain people, or that the default behavior could be disliked.

## Future Ideas
- [ ] Allow Mod keys to be shown side by side with the normal keys
- [ ] Add a pause keybind to allow pausing
- [ ] Make PortAudio not required when mic is off
- [ ] Make a more flexable face system allowing users to make animations
- [ ] Windows/Mac OS support?

(I can't promise that any of this will be added in the future. I could get busy or create a new project, these are just some ideas I have)
