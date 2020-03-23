import pytesseract
from PIL import Image

class TextRecognizer:
    image = None

    def __init__(self, imagePath):
      self.image = Image.open(imagePath)

    def getText(self):
      text = pytesseract.image_to_string(self.image, lang="eng+frk")
      return text

