import cv2
import numpy as np
import imageio

inputgif = "street.gif"
frames = imageio.mimread(input_gif)

# Processed frames list
processed_frames = []

# Apply thresholding to each frame
for frame in frames:
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Convert back to RGB for GIF
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    
    # Add to processed frames list
    processed_frames.append(thresh_rgb)

# Save processed frames as a new GIF
output_gif = "Output.gif"
imageio.mimsave(output_gif, processed_frames, duration=0.1)  # Adjust duration as needed

print("Thresholded GIF saved as:", output_gif)

# Need to see Otsu Method to do Thresholding foe better work improvemt of image processing
