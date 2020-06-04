'''
Main module for app's performance evaluation.
'''
import pandas as pd
from os import path

from input import parse_arguments
from processing import process_image, OutputFormat


def evaluate():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    image_path = args['image'][0]

    base_name = path.basename(image_path).split('.')[0]

    processing_result = pd.read_csv("./results/{}.csv".format(base_name))
    reference_data = pd.read_csv("./reference_data/{}.csv".format(base_name))

    compare(processing_result, reference_data)


def compare(actual_data, reference_data):
    '''
    Performs comparison between actual and reference data.
    '''
    print('comapre')
    print(actual_data)
    print(reference_data)


if __name__ == "__main__":
    evaluate()
