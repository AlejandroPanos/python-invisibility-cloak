# Invisibility Cloak

A Python implementation of an invisibility cloak effect using computer vision. This project uses OpenCV and NumPy to create a Harry Potter-style invisibility effect by detecting a colored cloth and replacing it with the background in real-time.

## How It Works

The program captures a static background, then continuously detects a specific color (bright yellow) in the video feed and replaces those pixels with the corresponding background pixels, creating the illusion of invisibility.

### Technical Approach

1. **Background Capture**: Takes 30 frames and calculates the median to create a clean background image
2. **Color Detection**: Converts frames to HSV color space and detects yellow-colored objects
3. **Mask Creation**: Uses morphological operations to clean up the detection mask
4. **Invisibility Effect**: Combines the current frame with the background using bitwise operations

## Features

- Real-time video processing
- HSV color space for robust color detection
- Morphological operations to reduce noise
- Median-based background capture to handle movement
- Simple keyboard controls

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/invisibility-cloak.git
   cd invisibility-cloak
   ```

2. Create a virtual environment

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

Create a `requirements.txt` file with:

```
opencv-python==4.8.0.76
numpy==1.24.3
```

## Usage

1. Run the program

   ```bash
   python invisibility_cloak.py
   ```

2. When prompted, **move out of the camera frame** for about 3 seconds while the background is captured

3. Step back into the frame with a **bright yellow cloth** (shirt, scarf, blanket, etc.)

4. The yellow cloth will appear invisible, showing the background instead

5. Press **'q'** to quit

## Camera Selection

If the wrong camera opens (e.g., OBS Virtual Camera instead of your webcam), change the camera index in the code:

```python
# In main() function, try different numbers:
cap = cv.VideoCapture(0)  # Try 0, 1, 2, etc.
```

## Color Customization

To use a different color for the cloak, adjust the HSV values in the `main()` function:

```python
# Current values (bright yellow):
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# For red:
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# For blue:
lower_blue = np.array([100, 150, 50])
upper_blue = np.array([130, 255, 255])
```

## Troubleshooting

**Camera won't open**

- Make sure no other applications are using the webcam
- Try changing the camera index: `cv.VideoCapture(0)`, `cv.VideoCapture(1)`, `cv.VideoCapture(2)`, etc.

**Cloak not detected**

- Ensure you're using a bright, solid-colored cloth
- Adjust the HSV color range values
- Check that lighting is adequate

**Background has ghosting**

- Make sure you completely move out of frame during background capture
- Stay still for the 3 seconds while background is being captured

## How It Works (Technical Details)

### Background Capture

```python
# Captures 30 frames and takes the median
# This removes any transient objects (like you walking through)
background = np.median(frames, axis=0)
```

### Color Detection

```python
# Converts to HSV for better color isolation
hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
# Creates mask where yellow is detected
mask = cv.inRange(hsv, lower_yellow, upper_yellow)
```

### Invisibility Effect

```python
# Extract everything except the cloak
foreground = frame AND (NOT mask)
# Extract background only where cloak is
background_section = background AND mask
# Combine them
result = foreground + background_section
```

## Project Structure

```
invisibility-cloak/
├── invisibility_cloak.py    # Main program
├── requirements.txt          # Dependencies
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Future Enhancements

- Support for multiple colors simultaneously
- Automatic color calibration
- Video recording of the effect
- Adjustable detection sensitivity via GUI
- Support for different cloak shapes/sizes
