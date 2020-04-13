'''
App's main module.
'''
import os
import cv2

from parse_arguments import parse_arguments
from preprocess_image import preprocess_image
from text_recognizer import TextRecognizer

args = parse_arguments()

originalImagePath = args['image']
preprocessMode = args['preprocess']
language = args['lang']

# create filename for temporary file
tempFilename = "{}.png".format(os.getpid())

# preprocess image
preprocessResult = preprocess_image(
    originalImagePath, preprocessMode, tempFilename)

# recognize content
recognizer = TextRecognizer(tempFilename, language)
text = recognizer.get_text()

# delete the temporary file
os.remove(tempFilename)

print(text)

# show the output images
cv2.imshow("Image", preprocessResult[0])
cv2.imshow("Output", preprocessResult[1])
cv2.waitKey(0)
