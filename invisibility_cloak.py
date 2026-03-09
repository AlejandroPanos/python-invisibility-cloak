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


def main():
    cap = cv.VideoCapture(1)

    if not cap.isOpened():
        print("Could not open camera.")
        return

    try:
        background = create_background(cap)
    except ValueError as err:
        print(f"Error: {err}")
        cap.release()
        return

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    print("Stating loop - press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Could not read frame.")
            time.sleep(1)
            continue
        mask = create_mask(frame, lower_yellow, upper_yellow)
        result = cloak_effect(frame, mask, background)

        cv.imshow("Invisible cloak", result)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
