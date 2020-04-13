'''
App's main module.
'''
import os
import cv2

from parseArguments import parseArguments
from preprocessImage import preprocessImage
from text_recognizer import TextRecognizer

args = parseArguments()

originalImagePath = args['image']
preprocessMode = args['preprocess']
language = args['lang']

# create filename for temporary file
tempFilename = "{}.png".format(os.getpid())

# preprocess image
preprocessResult = preprocessImage(
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
