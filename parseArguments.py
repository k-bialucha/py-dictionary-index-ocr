import argparse

ap = argparse.ArgumentParser()

def parseArguments():
  ap.add_argument("-i", "--image", required=True,
    help="path to input image to be OCR'd")

  ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="type of preprocessing to be done")

  args = vars(ap.parse_args())

  return args;