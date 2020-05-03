'''
Module for preprocessing provided image.
'''
import os
import cv2

COLOR_RED = (70, 70, 220)
COLOR_BLUE = (230, 70, 40)


class ImagePoint:
    '''
    Helper class for managing image points
    '''
    pos_x = None
    pos_y = None

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def change_x(self, change):
        '''
        Adds specified amount to X position

        Returns new ImagePoint instance
        '''
        return ImagePoint(self.pos_x + change, self.pos_y)

    def change_y(self, change):
        '''
        Adds specified amount to Y position

        Returns new ImagePoint instance
        '''
        return ImagePoint(self.pos_x, self.pos_y + change)

    def get_point(self):
        '''
        Returns (X,Y) point tuple required by OpenCV
        '''
        return (self.pos_x, self.pos_y)


def get_resized_window(input_image, max_height):
    '''
    Returns a new window size that fits image size
    '''
    original_height = input_image.shape[0]
    original_width = input_image.shape[1]

    resize_factor = max_height / original_height

    if resize_factor < 1:
        new_width = round(original_width * resize_factor)
        new_height = round(original_height * resize_factor)

        return (new_width, new_height)

    return (original_width, original_height)


class ImageManipulator:
    '''
    Manipulates the image
    '''
    image = None

    image_preprocessed = None
    image_preprocessed_filename = None

    image_marked = None

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

    def mark_word(self, word_data, line_color=COLOR_RED, line_thickness=3):
        '''
        Puts an underline to the word
        and prints the recognized word next to the actual
        '''
        if self.image_marked is None:
            self.image_marked = self.image

        y_level = word_data.top + word_data.height + 3
        x_start = word_data.left - 3
        x_end = word_data.left + word_data.width + 3

        start_point = ImagePoint(x_start, y_level)
        end_point = ImagePoint(x_end, y_level)

        self.image_marked = cv2.line(self.image,
                                     start_point.get_point(),
                                     end_point.get_point(),
                                     line_color,
                                     line_thickness)

        # draw rectangle
        rect_start_point = start_point.change_x(
            word_data.width + 5).change_y(-1*(word_data.height+3))
        rect_end_point = start_point.change_x(
            int(2.2 * word_data.width) + 10).change_y(3)

        self.image_marked = cv2.rectangle(self.image_marked,
                                          rect_start_point.get_point(),
                                          rect_end_point.get_point(),
                                          (150, 150, 200),
                                          -1)

        # draw word
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_start_point = start_point.change_x(
            word_data.width + 10).change_y(-5)

        font_scale = 0.7
        line_type = 2

        self.image_marked = cv2.putText(self.image_marked,
                                        word_data.text,
                                        text_start_point.get_point(),
                                        font,
                                        font_scale,
                                        (252, 252, 252),
                                        line_type)

    def mark_breakpoint(self, x_start, x_end, line_color=COLOR_BLUE, line_thickness=3):
        '''
        Marks a vertical line for breakpoint
        '''
        if self.image_marked is None:
            self.image_marked = self.image

        image_height = self.image.shape[0]
        x_start = int(round(x_start))
        x_end = int(round(x_end))

        # breakpoint start line points
        start_top = ImagePoint(x_start, 0)
        start_bottom = ImagePoint(x_start, image_height)

        # breakpoint end line points
        end_top = ImagePoint(x_end, 0)
        end_bottom = ImagePoint(x_end, image_height)

        self.image_marked = cv2.line(self.image_marked,
                                     start_top.get_point(),
                                     start_bottom.get_point(),
                                     line_color,
                                     line_thickness)
        self.image_marked = cv2.line(self.image_marked,
                                     end_top.get_point(),
                                     end_bottom.get_point(),
                                     line_color,
                                     line_thickness)

    def show(self, show_original=False, show_preprocessed=False, show_marked=False, max_height=960):
        '''
        Shows specified image(s)
        Allows to show original, preprocessed or marked image.
        '''
        base_name = "Image - {}"

        if show_original:
            window_name = base_name.format("original")
            cv2.namedWindow(window_name, flags=cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name,
                             get_resized_window(self.image, max_height))

            cv2.imshow(window_name,
                       self.image_marked)

        if show_preprocessed:
            window_name = base_name.format("preprocessed")
            cv2.namedWindow(window_name, flags=cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name,
                             get_resized_window(self.image, max_height))

            cv2.imshow(window_name,
                       self.image_preprocessed)

        if show_marked:
            window_name = base_name.format("marked")
            cv2.namedWindow(window_name, flags=cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name,
                             get_resized_window(self.image, max_height))

            cv2.imshow(window_name,
                       self.image_marked)

        cv2.waitKey(0)
