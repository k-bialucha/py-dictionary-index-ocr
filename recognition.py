'''
Module that wraps pytesseract recognition process
in the TextRecognizer class.
'''
import pytesseract
from PIL import Image


def are_rows_matching(df, block_num, breakpoint_start, breakpoint_end):
    # TODO: filter out short words
    block_matching = df.block_num == block_num
    is_first_word = df.word_num == 1

    is_after_breakpoint_start = breakpoint_start <= df.left
    is_before_breakpoint_end = df.left <= breakpoint_end

    return (block_matching) & (is_first_word) & (is_after_breakpoint_start) & (is_before_breakpoint_end)


class TextRecognizer:
    '''
    A class which allows to convert image object to text.
    Allows to customize language
    '''
    image = None
    language = None

    def __init__(self, imagePath, language):
        self.image = Image.open(imagePath)
        self.language = language

    def get_text(self):
        """ Extracts the text from image

        Returns:
        string: Extracted text

        """
        text = pytesseract.image_to_string(self.image, lang=self.language)
        return text

    def get_boxes(self):
        """ Extracts boxes from image
        needs more exploration

        Returns:
        object: some object of boxes

        """
        boxes = pytesseract.image_to_boxes(self.image, lang=self.language)
        return boxes

    def get_data(self):
        """ Extracts data from image
        needs more exploration

        Returns:
        object: pandas.DataFrame of Tesseract data

        """
        data = pytesseract.image_to_data(
            self.image, lang=self.language, output_type="data.frame")
        return data

    def get_block_offset_breakpoints(self, data_frame):
        # filter in only words from 2 main blocks
        top_num_words_blocks = data_frame.block_num.value_counts().nlargest(n=2)

        block_offset_breakpoints = list()
        for block in top_num_words_blocks.index:
            top_block_df = data_frame[(data_frame.block_num ==
                                       block)]

            left_min = top_block_df["left"].min()
            left_max = top_block_df["left"].max()
            offset_breakpoint_start = left_min + (left_max - left_min) * 0.05
            offset_breakpoint_end = left_min + (left_max - left_min) * 0.1

            block_offset_breakpoints.append(
                (block, offset_breakpoint_start, offset_breakpoint_end))

        return block_offset_breakpoints

    def get_offset_first_words(self):
        """ Extracts first word data for each offset line in image
        uses get_data function

        Returns:
        object: pandas.DataFrame of Tesseract data

        """
        data_frame = self.get_data()

        block_offset_breakpoints = self.get_block_offset_breakpoints(
            data_frame)

        block_1 = block_offset_breakpoints[0][0]
        block_1_breakpoint_start = block_offset_breakpoints[0][1]
        block_1_breakpoint_end = block_offset_breakpoints[0][2]
        block_2 = block_offset_breakpoints[1][0]
        block_2_breakpoint_start = block_offset_breakpoints[1][1]
        block_2_breakpoint_end = block_offset_breakpoints[1][2]

        offset_first_words_df = data_frame[(are_rows_matching(
            data_frame, block_1, block_1_breakpoint_start, block_1_breakpoint_end)) | (are_rows_matching(
                data_frame, block_2, block_2_breakpoint_start, block_2_breakpoint_end))]

        return offset_first_words_df, block_offset_breakpoints

    def get_word_list(self):
        ''' Extracts dictionary words as a simple list.

        Returns a list words (string).
        '''
        offset_first_words_df = self.get_offset_first_words()[0]

        print(offset_first_words_df)

        return offset_first_words_df['text'].tolist()
