import numpy as np

THRESHOLD = 3  # Set your volume threshold here
talking_frames = 0

def callback(indata, frames, time, status):
    global talking_frames
    volume_norm = np.linalg.norm(indata) * 10  # Calculate volume level
    if volume_norm > THRESHOLD:
        talking_frames = 15
