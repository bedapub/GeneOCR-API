import cv2


def detect_text_areas(image):
    bordersize = 50
    image = cv2.copyMakeBorder(
        image,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (8, 8))
    dilated = cv2.dilate(thresh, kernel, iterations=5)  # dilate
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        # discard areas that are too large
        if h > 500 and w > 500:
            continue
        # discard areas that are too small
        if h < 20 or w < 20:
            continue
        # draw rectangle around contour on original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)

    # write original image with added contours to disk
    return image
