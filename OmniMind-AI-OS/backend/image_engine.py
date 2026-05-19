from PIL import Image
import cv2

def analyze_image(path):
    image = cv2.imread(path)
    height, width, channels = image.shape
    return {
        "width": width,
        "height": height,
        "channels": channels
    }
