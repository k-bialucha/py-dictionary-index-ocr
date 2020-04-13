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
