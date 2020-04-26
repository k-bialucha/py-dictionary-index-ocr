'''
Allows to use TextRecognizer.
'''
import pytesseract
from PIL import Image


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

    def get_column_offset_boundaries(self, data_frame):
        # filter in only words from 2 main blocks
        top_blocks = data_frame.block_num.value_counts().nlargest(n=2)
        top_block_1 = top_blocks.index[1]

        top_block_1_df = data_frame[(data_frame.block_num ==
                                     top_block_1)]

        left_min = top_block_1_df["left"].min()
        left_max = top_block_1_df["left"].max()
        offset_breakpoint = left_min + (left_max - left_min) * 0.03

        return (offset_breakpoint, top_block_1)

    def get_offset_first_words(self):
        """ Extracts first word data for each offset line in image
        uses get_data function

        Returns:
        object: pandas.DataFrame of Tesseract data

        """
        data_frame = self.get_data()

        max_value, block_num = self.get_column_offset_boundaries(data_frame)

        block_offset_words_df = data_frame[(data_frame.block_num == block_num) & (
            data_frame.word_num == 1) & (max_value <= data_frame.left)]

        return block_offset_words_df
