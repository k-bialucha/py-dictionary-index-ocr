'''
Module that wraps pytesseract recognition process
in the TextRecognizer class.
'''
import pytesseract
from PIL import Image
import pandas as pd


def clean_word(word: str):
    '''
    Takes recognized word and cleans trailing comma sign if exists.
    '''
    if not isinstance(word, str):
        return word

    if word[-1] == ',':
        cleaned_word = word[0:-1]
        return cleaned_word

    return word


class TextRecognizer:
    '''
    A class which allows to convert image object to text.
    Allows to customize language and recognition method.
    '''
    image = None
    language = None
    method = None

    __text = None
    __boxes = None
    __data = None
    __osd = None

    def __init__(self, imagePath: str, language: str, method: int = 1):
        self.image = Image.open(imagePath)
        self.language = language
        self.method = method

    def __extract_text(self):
        '''
        Extracts the text from image.
        '''
        self.__text = pytesseract.image_to_string(
            self.image, lang=self.language)

    def get_text(self):
        '''
        Returns the text from image.
        '''
        if self.__text is None:
            self.__extract_text()

        return self.__text

    def __extract_boxes(self):
        '''
        Extracts boxes data from image.
        '''
        self.__boxes = pytesseract.image_to_boxes(
            self.image, lang=self.language, output_type="dict")

    def get_boxes(self):
        '''
        Returns boxes data from image.
        '''
        if self.__boxes is None:
            self.__extract_boxes()

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

    def __extract_osd(self):
        '''
        Extracts a dict containing OSD (screen and dimensions) data for the image.
        '''
        self.__osd = pytesseract.image_to_osd(
            self.image, lang=self.language, output_type="dict")

    def get_osd(self):
        '''
        Returns a dict containing OSD (screen and dimensions) data for the image.
        '''
        if self.__osd is None:
            self.__extract_osd()

        return self.__osd

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
        Extracts first word data using one of two methods.
        '''
        if self.method == 2:
            data = self.__get_offset_first_words_alt()
        else:
            data = self.__get_offset_first_words_default()

        data['text'] = data['text'].map(clean_word)

        return data

    def __get_offset_first_words_default(self):
        '''
        Extracts first word data for each offset line in image
        '''
        if self.__data is None:
            self.__extract_data()

        (block1_bp_data, block2_bp_data) = self.get_block_offset_breakpoints()

        block_query = 'block_num ==  {} and left >= {} and left <= {}'
        first_block_words = self.__data.query(block_query.format(
            block1_bp_data[0], block1_bp_data[1], block1_bp_data[2]))
        second_block_words = self.__data.query(block_query.format(
            block2_bp_data[0], block2_bp_data[1], block2_bp_data[2]))

        top_block_words = pd.concat([first_block_words, second_block_words])

        offset_first_words = top_block_words.query(
            'text.str.len() > 2 and word_num == 1')

        return offset_first_words.sort_index()

    def __get_offset_first_words_alt(self):
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
