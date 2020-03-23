import cv2
import os

from parseArguments import parseArguments
from preprocessImage import preprocessImage
from TextRecognizer import TextRecognizer

args = parseArguments();

# create filename for temporary file
tempFilename = "{}.png".format(os.getpid())

# preprocess image
preprocessResult = preprocessImage(args['image'], args['preprocess'], tempFilename)

# recognize content
recognizer = TextRecognizer(tempFilename)
text = recognizer.getText()

# delete the temporary file
os.remove(tempFilename)

print(text)

# show the output images
cv2.imshow("Image", preprocessResult[0])
cv2.imshow("Output", preprocessResult[1])
cv2.waitKey(0)