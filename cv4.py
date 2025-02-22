import cv2
import numpy as np

def load_image(image_path):
    """Loads an image from the given path."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image. Please check the path.")
        return None
    return image

def crop_image(image, x1, y1, x2, y2):
    """Crops the image based on the provided coordinates."""
    return image[y1:y2, x1:x2]

def rotate_image(image, angle):
    """Rotates the image by a given angle while keeping it properly centered."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated

def mean_filter(image, kernel_size=3):
    """Applies a mean filter to remove noise from the grayscale image."""
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
    filtered = cv2.filter2D(image, -1, kernel)
    return filtered

def edge_detection(image):
    """Detects edges in the image using a custom Sobel operator."""
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    edge_x = cv2.filter2D(image, -1, sobel_x)
    edge_y = cv2.filter2D(image, -1, sobel_y)
    edges = cv2.addWeighted(edge_x, 0.5, edge_y, 0.5, 0)
    return edges

def pencil_sketch(image):
    """Converts an image into a pencil sketch effect."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv_gray = 255 - gray
    blurred = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    return sketch

def morphological_operations(image, kernel_size=3):
    """Applies dilation and erosion to a binary image."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilation = cv2.dilate(image, kernel, iterations=1)
    erosion = cv2.erode(image, kernel, iterations=1)
    return dilation, erosion

if __name__ == "__main__":
    image_path = input("Enter the path of the image: ")
    image = load_image(image_path)
    
    if image is not None:
        cropped = crop_image(image, 50, 50, 200, 200)
        rotated = rotate_image(image, 45)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = mean_filter(grayscale)
        edges = edge_detection(grayscale)
        sketch = pencil_sketch(image)
        dilation, erosion = morphological_operations(grayscale)
        
        cv2.imshow("Original", image)
        cv2.imshow("Cropped", cropped)
        cv2.imshow("Rotated", rotated)
        cv2.imshow("Denoised", denoised)
        cv2.imshow("Edges", edges)
        cv2.imshow("Pencil Sketch", sketch)
        cv2.imshow("Dilation", dilation)
        cv2.imshow("Erosion", erosion)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
