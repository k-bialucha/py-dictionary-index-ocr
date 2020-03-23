import cv2
import os

def preprocessImage(imagePath, preprocessMode, tempFilename):
  image = cv2.imread(imagePath)
  grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # check to see if we should apply thresholding to preprocess the
  # image
  if preprocessMode == "thresh":
    grayImage = cv2.threshold(grayImage, 0, 255,
      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

  # make a check to see if median blurring should be done to remove
  # noise
  elif preprocessMode == "blur":
    grayImage = cv2.medianBlur(grayImage, 3)

  # write the grayscale image to disk as a temporary file so we can
  # apply OCR to it
  cv2.imwrite(tempFilename, grayImage)

  return (image, grayImage)