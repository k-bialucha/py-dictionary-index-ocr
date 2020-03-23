import pytesseract
from PIL import Image

class TextRecognizer:
    image = None
    language = None

    def __init__(self, imagePath, language):
      self.image = Image.open(imagePath)
      self.language = language

    def getText(self):
      text = pytesseract.image_to_string(self.image, lang=self.language)
      return text

