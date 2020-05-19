'''
Module that wraps pytesseract recognition process
in the TextRecognizer class.
'''
import pytesseract
from PIL import Image
import pandas as pd

class TextRecognizer:
    '''
    A class which allows to convert image object to text.
    Allows to customize language
    '''
    image = None
    language = None

    __text = None
    __boxes = None
    __data = None

    def __init__(self, imagePath, language):
        self.image = Image.open(imagePath)
        self.language = language

    def __extract_text(self):
        '''
        Extracts the text from image.
        '''
        self.__text = pytesseract.image_to_string(self.image, lang=self.language)

    def get_text(self):
        '''
        Returns the text from image.
        '''
        if self.__text is None:
            self.__extract_text()

        return self.__text

    def __extract_boxes(self):
        '''
        Extracts boxes from image.
        (needs more exploration)
        '''
        self.__boxes = pytesseract.image_to_boxes(self.image, lang=self.language)

    def get_boxes(self):
        '''
        Returns boxes from image.
        (needs more exploration)
        '''
        if self.__boxes is None:
            self.__extract_text()

        return self.__boxes

    def __extract_data(self):
        '''
        Extracts data from image and sets data property.
        '''
        self.__data = pytesseract.image_to_data(
            self.image, lang=self.language, output_type="data.frame")

    def get_data(self):
        '''
        Returns pandas DataFrame of all data from the image.
        '''
        if self.__data is None:
            self.__extract_data()

        return self.__data

    def get_block_offset_breakpoints(self):
        '''
        Calculates breakpoints for detecting offset words in 2 main blocks.
        '''
        if self.__data is None:
            self.__extract_data()

        # filter in only words from 2 main blocks
        top_num_words_blocks = self.__data.block_num.value_counts().nlargest(n=2)

        block_offset_breakpoints = list()
        for block in top_num_words_blocks.index:
            top_block_df = self.__data[(self.__data.block_num == block)]

            left_min = top_block_df["left"].min()
            left_max = top_block_df["left"].max()
            offset_breakpoint_start = left_min + (left_max - left_min) * 0.05
            offset_breakpoint_end = left_min + (left_max - left_min) * 0.1

            block_offset_breakpoints.append(
                (block, offset_breakpoint_start, offset_breakpoint_end))

        return block_offset_breakpoints

    def get_offset_first_words(self):
        '''
        Extracts first word data for each offset line in image

        Returns:
        object: pandas.DataFrame of Tesseract data
        '''
        if self.__data is None:
            self.__extract_data()

        block_offset_breakpoints = self.get_block_offset_breakpoints()

        block_1 = block_offset_breakpoints[0][0]
        block_1_breakpoint_start = block_offset_breakpoints[0][1]
        block_1_breakpoint_end = block_offset_breakpoints[0][2]
        block_2 = block_offset_breakpoints[1][0]
        block_2_breakpoint_start = block_offset_breakpoints[1][1]
        block_2_breakpoint_end = block_offset_breakpoints[1][2]

        block_query = 'block_num ==  {} and left >= {} and left <= {}'
        first_block = self.__data.query(block_query.format(
            block_1, block_1_breakpoint_start, block_1_breakpoint_end))
        second_block = self.__data.query(block_query.format(
            block_2, block_2_breakpoint_start, block_2_breakpoint_end))

        offset_first_words_df = pd.concat([first_block, second_block])

        offset_first_words_without_short = offset_first_words_df.query(
            'text.str.len() > 2 and word_num == 1')
        return offset_first_words_without_short

    def get_offset_first_words_alt(self):
        '''
        Extracts first word data for each offset line in image (alternative method)

        Returns:
        object: pandas.DataFrame of Tesseract data
        '''
        if self.__data is None:
            self.__extract_data()

        block_offset_breakpoints = self.get_block_offset_breakpoints()

        block_1 = block_offset_breakpoints[0][0]
        block_2 = block_offset_breakpoints[1][0]

        block_query = 'block_num ==  {}'
        first_block = self.__data.query(block_query.format(block_1))
        second_block = self.__data.query(block_query.format(block_2))

        offset_first_words_df = pd.concat([first_block, second_block])

        offset_first_words_without_short = offset_first_words_df.query(
            'text.str.len() > 2 and word_num == 1 and line_num == 1')

        return offset_first_words_without_short

    def get_word_list(self):
        '''
        Extracts dictionary words as a simple list.

        Returns:
        list of words (string)
        '''
        if self.__data is None:
            self.__extract_data()

        offset_first_words_df = self.get_offset_first_words()[0]

        return offset_first_words_df['text'].tolist()
