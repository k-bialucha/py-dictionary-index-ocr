'''
Module for preprocessing provided image.
'''
import cv2


def preprocess_image(image_path, preprocess_mode, temp_filename):
    '''
    Applies image preporcessing.
    Aims for improve recognition quality.
    '''
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess_mode == "thresh":
        gray_image = cv2.threshold(gray_image, 0, 255,
                                   cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess_mode == "blur":
        gray_image = cv2.medianBlur(gray_image, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    cv2.imwrite(temp_filename, gray_image)

    return (image, gray_image)
