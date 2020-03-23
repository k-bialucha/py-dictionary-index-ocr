# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os

from parseArguments import parseArguments
from preprocessImage import preprocessImage

args = parseArguments();

# create filename for temporary file
tempFilename = "{}.png".format(os.getpid())

preprocessResult = preprocessImage(args['image'], args['preprocess'], tempFilename)

text = pytesseract.image_to_string(Image.open(tempFilename), lang="eng+frk")

# delete the temporary file
os.remove(tempFilename)

print(text)

# show the output images
cv2.imshow("Image", preprocessResult[0])
cv2.imshow("Output", preprocessResult[1])
cv2.waitKey(0)