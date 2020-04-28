'''
App's main module.
'''
import cv2

from parse_arguments import parse_arguments
from imaging import ImageManipulator
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

    # draw rectangle

    rect_start_point = (
        start_point[0] + word_data.width + 5, start_point[1] - word_data.height - 3)
    rect_end_point = (
        start_point[0] + int(2.2 * word_data.width) + 10, start_point[1] + 3)
    image_marked = cv2.rectangle(
        image_marked, rect_start_point, rect_end_point, (150, 150, 200), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    text_start_point = (
        start_point[0] + word_data.width + 10, start_point[1] - 5)
    font_scale = 0.7
    line_type = 2

    image_marked = cv2.putText(image_marked,
                               word_data.text,
                               text_start_point,
                               font,
                               font_scale,
                               (252, 252, 252),
                               line_type)

    return image_marked


def mark_breakpoint(image, x_start, x_end):
    image_height = image.shape[0]
    x_start = int(round(x_start))
    x_end = int(round(x_end))

    # breakpoint start line points
    start_top = (x_start, 0)
    start_bottom = (x_start, image_height)

    # breakpoint end line points
    end_top = (x_end, 0)
    end_bottom = (x_end, image_height)

    line_color = (230, 70, 40)
    line_thickness = 1

    image_marked = image
    image_marked = cv2.line(image_marked,
                            start_top, start_bottom, line_color, line_thickness)
    image_marked = cv2.line(image_marked,
                            end_top, end_bottom, line_color, line_thickness)

    return image_marked


def main():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    original_image_path = args['image']
    preprocess_mode = args['preprocess']
    language = args['lang']

    image_manipulator = ImageManipulator(original_image_path)

    # preprocess image
    image_manipulator.preprocess_image(preprocess_mode)

    # recognize content
    recognizer = TextRecognizer(
        image_manipulator.get_image_preprocessed_filename(), language)
    first_words, breakpoints = recognizer.get_offset_first_words()

    # mark each word on the original image
    image_marked = image_manipulator.image
    for i, row in first_words.iterrows():
        image_marked = mark_word(image_marked, row)

    for bp in breakpoints:
        image_marked = mark_breakpoint(
            image_marked, bp[1], bp[2])

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
