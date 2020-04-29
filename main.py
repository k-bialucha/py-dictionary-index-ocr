'''
App's main module.
'''
import cv2

from input import parse_arguments
from imaging import ImageManipulator
from recognition import TextRecognizer


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
    for i, row in first_words.iterrows():
        image_manipulator.mark_word(row)

    for bp in breakpoints:
        image_manipulator.mark_breakpoint(bp[1], bp[2])

    # save first words to CSV
    first_words.to_csv('data.csv')

    # TODO: allow to disable image output
    # show the output images
    cv2.imshow("Image - debug", image_manipulator.image_marked)
    # cv2.imshow("Image", image_manipulator.image)
    # cv2.imshow("Output", image_manipulator.image_preprocessed)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
