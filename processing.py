'''
Module for transforming input image
to a final output.
'''
from os import path
from imaging import ImageManipulator
from recognition import TextRecognizer

from debug import DebugHandler

def process_image(image_path, preprocess_mode, language, debug):
    '''
    Function that handles processing of a single image

    Takes image path and other parameters as input
    and returns a list of recognized dictionary words.
    '''
    image_manipulator = ImageManipulator(image_path)

    # preprocess image
    image_manipulator.preprocess_image(preprocess_mode)

    # recognize content
    recognizer = TextRecognizer(
        image_manipulator.get_image_preprocessed_filename(), language)
    first_words = recognizer.get_offset_first_words()
    breakpoints = recognizer.get_block_offset_breakpoints()

    if debug:
        filename = path.basename(image_path)
        debug_handler = DebugHandler(filename)

        debug_tag = debug_handler.get_debug_tag()
        # mark each word on the original image
        for _, row in first_words.iterrows():
            image_manipulator.mark_word(row)

        for bp in breakpoints:
            image_manipulator.mark_breakpoint(bp[1], bp[2])

        # save first words to CSV
        first_words.to_csv('./debug/{}_words.csv'.format(debug_tag))

        # show image
        image_manipulator.show(show_marked=True)

        # save debug image
        image_manipulator.save_debug('./debug/{}_debug-image.jpg'.format(debug_tag))

    return first_words
    