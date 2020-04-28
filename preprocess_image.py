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
    image_processed = None
    temp_filename = None

    def __init__(self, image_path):  # language
        self.image = cv2.imread(image_path)
        self.temp_filename = "{}.png".format(os.getpid())

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
        cv2.imwrite(self.temp_filename, image_gray)

        self.image_processed = image_gray
        cv2.imwrite(self.temp_filename, image_gray)

    def get_image_filename(self):
        '''
        Returns the temporary file name
        '''
        return self.temp_filename

    def clean(self):
        '''
        Cleans the temporary file
        '''
        os.remove(self.temp_filename)
