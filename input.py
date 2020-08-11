'''
Module for parsing app entry arguments.
'''
import argparse


def parse_main_arguments():
    '''
    Parses provided arguments.

    Returns object:
    names: image names
    config_name: name prefix
    preprocess: type of preprocessing
    lang: recognition language
    method: method for dictionary word selection
    debug: whether to display debug data
    '''
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('names', metavar='name', type=str, nargs='+',
                            help='a list of names for input')

    arg_parser.add_argument("-cn", "--config-name", type=str, default=None,
                            help="a config name for saving results")

    arg_parser.add_argument("-p", "--preprocess", type=str, default="thresh",
                            help="type of preprocessing to be done")

    arg_parser.add_argument("-l", "--lang", type=str, default="deu+frk",
                            help="set language of recognition")

    arg_parser.add_argument("-m", "--method", type=int, default=1,
                            help="set method for dictionary word selection")

    arg_parser.add_argument('--no-debug', dest='debug', action='store_false')
    arg_parser.set_defaults(debug=True)

    args = vars(arg_parser.parse_args())

    return args


def parse_evaluation_arguments():
    '''
    Parses provided arguments.

    Returns object:
    names: list of names
    config_name: name prefix
    debug: whether to display debug data
    '''
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('names', metavar='name', type=str, nargs='+',
                            help='a list of names for evaluation')

    arg_parser.add_argument("-cn", "--config-name", type=str, default=None,
                            help="a config name for saving results")

    arg_parser.add_argument('--no-debug', dest='debug', action='store_false')
    arg_parser.set_defaults(debug=True)

    args = vars(arg_parser.parse_args())

    return args
