'''
Module for parsing app entry arguments.
'''
import argparse


def parse_arguments():
    '''
    Parses provided arguments.

    Returns object:
    image: image path
    preprocess: type of preprocessing
    lang: recognition language
    '''
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-i", "--image", required=True,
                            help="path to input image to be recognized")

    arg_parser.add_argument("-p", "--preprocess", type=str, default="thresh",
                            help="type of preprocessing to be done")

    arg_parser.add_argument("-l", "--lang", type=str, default="eng+frk",
                            help="set language of recognition")

    args = vars(arg_parser.parse_args())

    return args
