import argparse

ap = argparse.ArgumentParser()

def parseArguments():
  ap.add_argument("-i", "--image", required=True,
    help="path to input image to be recognized")

  ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="type of preprocessing to be done")
    
  ap.add_argument("-l", "--lang", type=str, default="eng+frk",
    help="set language of recognition")

  args = vars(ap.parse_args())

  return args;