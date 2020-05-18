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

    arg_parser.add_argument("-i", "--image", required=True, nargs="+",
                            help="path to input image to be recognized")

    arg_parser.add_argument("-p", "--preprocess", type=str, default="thresh",
                            help="type of preprocessing to be done")

    arg_parser.add_argument("-l", "--lang", type=str, default="deu+frk",
                            help="set language of recognition")

    arg_parser.add_argument('--default', dest='debug', action='store_true')
    arg_parser.add_argument('--no-debug', dest='debug', action='store_false')
    arg_parser.set_defaults(debug=True)

    args = vars(arg_parser.parse_args())

    return args
