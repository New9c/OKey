from consts import SETTINGS
import numpy as np

talking_frames = 0

def callback(indata, frames, time, status):
    global talking_frames
    volume_norm = np.linalg.norm(indata) * 10
    if SETTINGS["print_loudness"]:
        print(f"Loudness: {round(volume_norm*1000)/1000}, Talking: {volume_norm > SETTINGS["mic_threshold"]}")
    if volume_norm > SETTINGS["mic_threshold"]:
        talking_frames = SETTINGS["clear_talking_frames"]
