'''
App's main module.
'''
import os
import cv2

from parse_arguments import parse_arguments
from preprocess_image import preprocess_image
from text_recognizer import TextRecognizer


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
    text = recognizer.get_text()

    # delete the temporary file
    os.remove(temp_filename)

    print(text)

    # show the output images
    cv2.imshow("Image", preprocess_result[0])
    cv2.imshow("Output", preprocess_result[1])
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
