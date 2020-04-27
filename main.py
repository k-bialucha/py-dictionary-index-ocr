'''
App's main module.
'''
import os
import cv2

from parse_arguments import parse_arguments
from preprocess_image import preprocess_image
from text_recognizer import TextRecognizer


def mark_word(image, word_data):
    y_level = word_data.top + word_data.height + 3
    x_start = word_data.left - 3
    x_end = word_data.left + word_data.width + 3

    start_point = (x_start, y_level)
    end_point = (x_end, y_level)

    line_color = (70, 70, 220)
    line_thickness = 2

    image_marked = cv2.line(image,
                            start_point, end_point, line_color, line_thickness)

    return image_marked


def main():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    original_image_path = args['image']
    preprocess_mode = args['preprocess']
    language = args['lang']

    # create filename for temporary file
    temp_filename = "{}.png".format(os.getpid())

    # preprocess image
    preprocess_result = preprocess_image(
        original_image_path, preprocess_mode, temp_filename)

    # recognize content
    recognizer = TextRecognizer(temp_filename, language)
    first_words = recognizer.get_offset_first_words()

    # delete the temporary file
    os.remove(temp_filename)

    # mark each word on the original image
    image_marked = preprocess_result[0]
    for i, row in first_words.iterrows():
        image_marked = mark_word(image_marked, row)

    # save first words to CSV
    first_words.to_csv('data.csv')

    # TODO: allow to disable image output
    # show the output images
    cv2.imshow("Found first words", image_marked)
    # cv2.imshow("Image", preprocess_result[0])
    # cv2.imshow("Output", preprocess_result[1])
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
