'''
Module for preprocessing provided image.
'''
import os
import cv2


class ImageManipulator:
    '''
    Manipulates the image
    '''
    image = None
    image_preprocessed = None
    image_preprocessed_filename = None

    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.image_preprocessed_filename = "{}.png".format(os.getpid())

    def __del__(self):
        os.remove(self.image_preprocessed_filename)

    def preprocess_image(self, preprocess_mode):
        '''
        Applies image processing.
        Aims for recognition quality improvement.
        '''
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # check to see if we should apply thresholding to preprocess the image
        if preprocess_mode == "thresh":
            image_gray = cv2.threshold(image_gray, 0, 255,
                                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # make a check to see if median blurring should be done to remove noise
        elif preprocess_mode == "blur":
            image_gray = cv2.medianBlur(image_gray, 3)

        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        cv2.imwrite(self.image_preprocessed_filename, image_gray)

        self.image_preprocessed = image_gray

    def get_image_preprocessed_filename(self):
        '''
        Returns the preprocessed image file name
        '''
        return self.image_preprocessed_filename
