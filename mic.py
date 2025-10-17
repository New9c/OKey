import consts
import numpy as np

talking_frames = 0

def callback(indata, frames, time, status):
    global talking_frames
    volume_norm = np.linalg.norm(indata) * 10
    if consts.OUTPUT_LOUDNESS:
        print(f"Loudness: {round(volume_norm*1000)/1000}, Talking: {volume_norm > consts.MIC_THRESHOLD}")
    if volume_norm > consts.MIC_THRESHOLD:
        talking_frames = 15
