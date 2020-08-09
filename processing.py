'''
Module for transforming input image
to a final output.
'''
from enum import Enum
from os import path
from pathlib import Path

from debug import DebugHandler
from imaging import ImageManipulator
from recognition import TextRecognizer


class OutputFormat(Enum):
    '''
    Enumerates possible output formats for process_image function
    '''
    none = 0
    word_list = 1
    data_frame = 2
    data_frame_stripped = 3


def process_image(image_path: str, preprocess_mode: str, language: str, debug: bool, config_name: str = None, output_format=OutputFormat.data_frame):
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

    # get recognition data
    all_words = recognizer.get_data()
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

        # show image
        image_manipulator.show(show_marked=True)

        # save debug image
        image_manipulator.save_debug(
            './debug/{}_debug-image.jpg'.format(debug_tag))

        # export words to CSV
        debug_handler.export_df_to_csv(first_words, 'words')
        debug_handler.export_df_to_csv(all_words, 'all-words')

    result = None
    result_filename = path.basename(image_path).split('.')[0]

    if config_name is not None:
        Path("./results/{}".format(config_name)
             ).mkdir(parents=True, exist_ok=True)

        result_path = './results/{}/{}.csv'.format(
            config_name, result_filename)
    else:
        result_path = './results/{}.csv'.format(result_filename)

    if output_format == OutputFormat.word_list:
        # TODO: return a list of strings
        result = first_words

    if output_format == OutputFormat.data_frame:
        result = first_words
        result.to_csv(result_path, index=False)

    if output_format == OutputFormat.data_frame_stripped:
        result = first_words.drop(
            columns=['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num'])
        result.to_csv(result_path, index=False)

    return result


def get_page_index(image_name: str):
    '''
    Takes an image name and converts it to index
    using rules based on data structure.
    '''
    base_index = int(image_name[-7:-4])

    if base_index <= 22:
        return None

    if base_index <= 154:
        return base_index - 22

    if base_index == 155:
        return '132a'

    if base_index == 156:
        return '132b'

    return base_index - 24
