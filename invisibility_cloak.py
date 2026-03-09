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


def create_mask(frame, lower_color, upper_color):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv.morphologyEx(
        mask, cv.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1
    )
    return mask


def cloak_effect(frame, mask, background):
    mask_inv = cv.bitwise_not(mask)
    fg = cv.bitwise_and(frame, frame, mask=mask_inv)
    bg = cv.bitwise_and(background, background, mask=mask)
    return cv.add(fg, bg)
