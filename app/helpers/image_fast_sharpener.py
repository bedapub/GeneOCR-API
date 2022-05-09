from PIL import Image, ImageEnhance
import io
import numpy as np
import cv2


def pil_fast_sharpener(file):
    image = Image.open(io.BytesIO(file))
    enhancer = ImageEnhance.Sharpness(image)
    factor = 3
    img = enhancer.enhance(factor)
    return img


def cv2_kernel_fast_sharpener(file):
    image = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    image_sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return image_sharp
