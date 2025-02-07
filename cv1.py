import cv2 as cv
import numpy as np

# Load and resize image
img = cv.imread("sexy.jpg")
img1 = cv.resize(img, (500, 500))

# Variables to store latest mouse position & color values
last_x, last_y = 0, 0
last_rgb = (0, 0, 0)
last_hsv = (0, 0, 0)

def mouse_callback(event, x, y, flags, param):
    global last_x, last_y, last_rgb, last_hsv

    if event == cv.EVENT_MOUSEMOVE:
        last_x, last_y = x, y
        b, g, r = map(int, img1[y, x])  # Ensure RGB values are integers
        last_rgb = (r, g, b)
        last_hsv = bgr_to_hsv(b, g, r)  # Convert using formula

# ✅ Manual formula for BGR to HSV
def bgr_to_hsv(b, g, r):
    # Normalize BGR values
    R, G, B = r / 255.0, g / 255.0, b / 255.0

    # Compute max, min, and delta
    C_max = max(R, G, B)
    C_min = min(R, G, B)
    delta = C_max - C_min

    # Compute Hue (H)
    if delta == 0:
        H = 0
    elif C_max == R:
        H = (60 * ((G - B) / delta) % 6) if delta != 0 else 0
    elif C_max == G:
        H = 60 * ((B - R) / delta + 2)
    elif C_max == B:
        H = 60 * ((R - G) / delta + 4)

    if H < 0:
        H += 360  # Ensure non-negative H

    # Compute Saturation (S)
    S = (delta / C_max) if C_max != 0 else 0

    # Compute Value (V)
    V = C_max

    # Scale to OpenCV HSV format (0-179, 0-255, 0-255)
    H = int(H / 2)  # Scale to [0,179] for OpenCV
    S = int(S * 255)
    V = int(V * 255)

    return H, S, V

cv.namedWindow("Image")
cv.setMouseCallback("Image", mouse_callback)

while True:
    img_display = img1.copy()  # **Use a fresh copy every frame to prevent stacking**

    # Text info
    text_rgb = f"RGB: {tuple(map(int, last_rgb))}"  # Ensure integer display
    text_hsv = f"HSV: {tuple(map(int, last_hsv))}"
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1

    # Text positions
    x_offset, y_offset = 15, 25
    text_pos = (last_x + x_offset, last_y + y_offset)
    text_pos2 = (last_x + x_offset, last_y + y_offset + 20)

    # Ensure text stays inside window
    img_height, img_width, _ = img1.shape
    if text_pos[0] + 150 > img_width:
        text_pos = (last_x - 150, last_y + y_offset)
        text_pos2 = (last_x - 150, last_y + y_offset + 20)
    if text_pos[1] + 20 > img_height:
        text_pos = (last_x + x_offset, last_y - y_offset)
        text_pos2 = (last_x + x_offset, last_y - y_offset + 20)

    # Draw a black rectangle as background
    (w1, h1), _ = cv.getTextSize(text_rgb, font, font_scale, thickness)
    (w2, h2), _ = cv.getTextSize(text_hsv, font, font_scale, thickness)
    cv.rectangle(img_display, (text_pos[0] - 5, text_pos[1] - h1 - 5),
                 (text_pos[0] + w1 + 5, text_pos[1] + 5), (0, 0, 0), -1)
    cv.rectangle(img_display, (text_pos2[0] - 5, text_pos2[1] - h2 - 5),
                 (text_pos2[0] + w2 + 5, text_pos2[1] + 5), (0, 0, 0), -1)

    # Draw text
    cv.putText(img_display, text_rgb, text_pos, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)
    cv.putText(img_display, text_hsv, text_pos2, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)

    cv.imshow("Image", img_display)  # Show updated frame
    
    if cv.waitKey(1) & 0xFF == 27:  # Exit on 'ESC'
        break

cv.destroyAllWindows()
