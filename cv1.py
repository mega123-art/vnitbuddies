import cv2 as cv
import numpy as np

# Load and resize image
img = cv.imread("sexy.jpg")
img1 = cv.resize(img, (500, 500))

display_img = img1.copy()  # This will store the modified image with persistent pixelation

# Variables to store latest mouse position & color values
last_x, last_y = 0, 0
last_rgb = (0, 0, 0)
last_hsv = (0, 0, 0)
pixelate_mode = False
pixel_size = 10  # Initial pixelation size

def mouse_callback(event, x, y, flags, param):
    global last_x, last_y, last_rgb, last_hsv
    
    if event == cv.EVENT_MOUSEMOVE:
        last_x, last_y = x, y
        b, g, r = map(int, display_img[y, x])  # Ensure RGB values are integers
        last_rgb = (r, g, b)
        last_hsv = bgr_to_hsv(b, g, r)  # Convert using formula

# ✅ Manual formula for BGR to HSV
def bgr_to_hsv(b, g, r):
    R, G, B = r / 255.0, g / 255.0, b / 255.0
    C_max = max(R, G, B)
    C_min = min(R, G, B)
    delta = C_max - C_min

    if delta == 0:
        H = 0
    elif C_max == R:
        H = (60 * ((G - B) / delta) % 6) if delta != 0 else 0
    elif C_max == G:
        H = 60 * ((B - R) / delta + 2)
    elif C_max == B:
        H = 60 * ((R - G) / delta + 4)
    if H < 0:
        H += 360

    S = (delta / C_max) if C_max != 0 else 0
    V = C_max
    
    H = int(H / 2)
    S = int(S * 255)
    V = int(V * 255)
    
    return H, S, V

def pixelate_region(image, center, size):
    x, y = center
    half_size = size // 2
    x1, y1 = max(0, x - half_size), max(0, y - half_size)
    x2, y2 = min(image.shape[1], x + half_size), min(image.shape[0], y + half_size)
    
    if x2 - x1 <= 0 or y2 - y1 <= 0:
        return image
    
    # Compute mean color for the region
    roi = image[y1:y2, x1:x2]
    avg_color = np.mean(roi, axis=(0, 1), dtype=int)
    
    # Assign mean color to entire region
    image[y1:y2, x1:x2] = avg_color
    return image

cv.namedWindow("Image")
cv.setMouseCallback("Image", mouse_callback)

while True:
    img_display = display_img.copy()
    
    if pixelate_mode:
        display_img = pixelate_region(display_img, (last_x, last_y), pixel_size)
    
    text_rgb = f"RGB: {tuple(map(int, last_rgb))}"
    text_hsv = f"HSV: {tuple(map(int, last_hsv))}"
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    x_offset, y_offset = 15, 25
    text_pos = (last_x + x_offset, last_y + y_offset)
    text_pos2 = (last_x + x_offset, last_y + y_offset + 20)
    
    img_height, img_width, _ = display_img.shape
    if text_pos[0] + 150 > img_width:
        text_pos = (last_x - 150, last_y + y_offset)
        text_pos2 = (last_x - 150, last_y + y_offset + 20)
    if text_pos[1] + 20 > img_height:
        text_pos = (last_x + x_offset, last_y - y_offset)
        text_pos2 = (last_x + x_offset, last_y - y_offset + 20)
    
    (w1, h1), _ = cv.getTextSize(text_rgb, font, font_scale, thickness)
    (w2, h2), _ = cv.getTextSize(text_hsv, font, font_scale, thickness)
    cv.rectangle(img_display, (text_pos[0] - 5, text_pos[1] - h1 - 5),
                 (text_pos[0] + w1 + 5, text_pos[1] + 5), (0, 0, 0), -1)
    cv.rectangle(img_display, (text_pos2[0] - 5, text_pos2[1] - h2 - 5),
                 (text_pos2[0] + w2 + 5, text_pos2[1] + 5), (0, 0, 0), -1)
    
    cv.putText(img_display, text_rgb, text_pos, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)
    cv.putText(img_display, text_hsv, text_pos2, font, font_scale, (255, 255, 255), thickness, cv.LINE_AA)
    
    cv.imshow("Image", img_display)
    key = cv.waitKey(1) & 0xFF
    
    if key == 27:
        break
    elif key == ord('r'):
        pixelate_mode = not pixelate_mode
        print(f"Pixelation mode: {'ON' if pixelate_mode else 'OFF'}")
    elif key == ord('+') and pixelate_mode:
        pixel_size = min(50, pixel_size + 5)
        print(f"Pixelation size: {pixel_size}")
    elif key == ord('-') and pixelate_mode:
        pixel_size = max(5, pixel_size - 5)
        print(f"Pixelation size: {pixel_size}")
    
cv.destroyAllWindows()
