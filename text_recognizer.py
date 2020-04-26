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

    def get_first_words(self):
        """ Extracts first word data for each line in image
        uses get_data function

        Returns:
        object: pandas.DataFrame of Tesseract data

        """
        data_frame = self.get_data()

        # filter in only words from 2 main blocks
        top_rows = data_frame.block_num.value_counts().nlargest(n=2)
        top_row_1 = top_rows.index[0]
        top_row_2 = top_rows.index[1]

        first_words_df = data_frame[data_frame.word_num == 1]
        top_block_first_words_df = first_words_df[(first_words_df.block_num ==
                                                   top_row_1) | (first_words_df.block_num == top_row_2)]

        return top_block_first_words_df
