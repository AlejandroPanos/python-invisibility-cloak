import time
import cv2 as cv
import numpy as np


def create_background(cap, num_frames=30):
    print("Capturing your background, please move out the way.")
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print("Could not read frame {i+1}/{num-frames}")
        time.sleep(0.1)
        if backgrounds:
            return np.median(backgrounds, axis=0).astype(np.uint8)
        else:
            return ValueError("Could not capture frames for the background")
